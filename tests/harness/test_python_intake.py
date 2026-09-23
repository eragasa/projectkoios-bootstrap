from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from projectkoios.bootstrap.harness.python_intake import (
    IntakeAnalysisError,
    IntakeLimits,
    analyze_python_intake,
    compare_intake_to_git_patch,
    main,
    render_markdown,
)

_REPOSITORY = Path(__file__).parents[2]
_FIXTURES = Path(__file__).parents[1] / "fixtures" / "python-intake"


class PythonIntakeAnalysisTests(unittest.TestCase):
    def test__control_surfaces__exclude_raw_intake_from_tracking_and_package(
        self,
    ) -> None:
        ignore = (_REPOSITORY / ".gitignore").read_text(encoding="utf-8")
        configuration = tomllib.loads(
            (_REPOSITORY / "pyproject.toml").read_text(encoding="utf-8")
        )

        self.assertIn(
            "python/projectkoios/bootstrap/development/**/intake/",
            ignore.splitlines(),
        )
        self.assertIn(
            "projectkoios.bootstrap.development*",
            configuration["tool"]["setuptools"]["packages"]["find"]["exclude"],
        )

    def test__analyze__inventories_dependencies_tests_and_signals(self) -> None:
        report = analyze_python_intake(_FIXTURES / "complete")

        self.assertEqual(report["summary"]["file_count"], 3)
        self.assertEqual(report["summary"]["python_file_count"], 2)
        self.assertEqual(report["summary"]["test_function_count"], 1)
        self.assertEqual(report["summary"]["syntax_error_count"], 0)
        self.assertEqual(
            report["dependencies"]["external_imports"],
            ["optional_backend", "pytest", "requests"],
        )
        self.assertEqual(
            report["dependencies"]["external_imports_not_declared_in_intake"],
            ["optional_backend"],
        )
        self.assertEqual(
            report["dependencies"]["local_imports_not_present_in_intake"],
            [],
        )
        self.assertEqual(
            report["capability_signals"], ["network-capable-import"]
        )
        self.assertEqual(
            report["tests"]["targets"],
            [
                {
                    "definition_found": True,
                    "target": "ExampleTool",
                    "tests": [
                        "tests/test_tool.py::"
                        "test__ExampleTool__encodes_deterministically"
                    ],
                }
            ],
        )
        test_plan = next(
            item
            for item in report["validation_plan"]
            if item["name"] == "tests"
        )
        self.assertTrue(test_plan["executes_intake_code"])
        self.assertIn("pytest", test_plan["argv"])

    def test__analyze__plans_unittest_when_pytest_is_not_imported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root / "src/python/example/tool.py", "VALUE = 1\n")
            self._write(
                root / "tests/test_tool.py",
                "import unittest\n"
                "\n"
                "class ToolTests(unittest.TestCase):\n"
                "    def test_value(self):\n"
                "        self.assertEqual(1, 1)\n",
            )

            report = analyze_python_intake(root)

        test_plan = next(
            item
            for item in report["validation_plan"]
            if item["name"] == "tests"
        )
        self.assertIn("unittest", test_plan["argv"])
        self.assertNotIn("pytest", test_plan["argv"])

    def test__analyze__reports_effect_signals_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(
                root / "src/python/example/effects.py",
                "from pathlib import Path\n"
                "import subprocess\n"
                "\n"
                "def effects(value: str) -> object:\n"
                "    Path('result').write_text(value)\n"
                "    subprocess.run(['tool'], check=False)\n"
                "    return eval(value)\n",
            )

            report = analyze_python_intake(root)
            self.assertFalse((root / "result").exists())

        self.assertEqual(
            report["capability_signals"],
            [
                "dynamic-code-execution",
                "filesystem-mutation",
                "process-capable-import",
                "process-execution",
            ],
        )

    def test__analyze__reports_syntax_error_without_execution(self) -> None:
        report = analyze_python_intake(_FIXTURES / "malformed")

        self.assertEqual(report["summary"]["syntax_error_count"], 1)
        self.assertIn(
            "was never closed",
            report["python_files"][0]["syntax_error"],
        )

    def test__analyze__is_deterministic_and_omits_absolute_root(
        self,
    ) -> None:
        first = analyze_python_intake(_FIXTURES / "complete")
        second = analyze_python_intake(_FIXTURES / "complete")

        self.assertEqual(first, second)
        serialized = json.dumps(first, sort_keys=True)
        self.assertNotIn(str(_FIXTURES.resolve()), serialized)

    def test__analyze__rejects_file_outside_bound(self) -> None:
        with self.assertRaisesRegex(
            IntakeAnalysisError,
            "exceeds max_file_bytes",
        ):
            analyze_python_intake(
                _FIXTURES / "complete",
                limits=IntakeLimits(max_file_bytes=10),
            )

    def test__analyze__rejects_tree_outside_depth_bound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root / "one/two/example.py", "VALUE = 1\n")

            with self.assertRaisesRegex(
                IntakeAnalysisError,
                "exceeds max_depth",
            ):
                analyze_python_intake(
                    root,
                    limits=IntakeLimits(max_depth=1),
                )

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test__analyze__rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.py").write_text("value = 1\n", encoding="utf-8")
            os.symlink(root / "target.py", root / "alias.py")

            with self.assertRaisesRegex(
                IntakeAnalysisError,
                "contains a symlink",
            ):
                analyze_python_intake(root)

    def test__compare__finds_exact_file_and_absent_companions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            repository = temporary / "owner"
            intake = temporary / "intake"
            repository.mkdir()
            self._git(repository, "init", "-q")
            self._git(
                repository,
                "config",
                "user.email",
                "test@example.invalid",
            )
            self._git(repository, "config", "user.name", "Test User")
            self._write(repository / "pyproject.toml", "[project]\nname='x'\n")
            self._write(
                repository / "src/python/example/documents.py",
                "DOCUMENT_KIND = 'base'\n",
            )
            self._git(repository, "add", ".")
            self._git(repository, "commit", "-q", "-m", "base")
            base = self._git(repository, "rev-parse", "HEAD").strip()

            (repository / "src/python/example/documents").mkdir()
            self._git(
                repository,
                "mv",
                "src/python/example/documents.py",
                "src/python/example/documents/__init__.py",
            )
            self._write(
                repository / "src/python/example/new.py",
                "VALUE = 1\n",
            )
            self._write(
                repository / "pyproject.toml",
                "[project]\nname='x'\ndependencies=['example']\n",
            )
            self._git(repository, "add", ".")
            self._git(repository, "commit", "-q", "-m", "head")
            head = self._git(repository, "rev-parse", "HEAD").strip()

            source = repository / "src/python/example/new.py"
            target = intake / "src/python/example/new.py"
            target.parent.mkdir(parents=True)
            shutil.copyfile(source, target)

            report = compare_intake_to_git_patch(
                intake,
                repository=repository,
                base_ref=base,
                head_ref=head,
            )

        comparison = report["comparison"]
        self.assertEqual(comparison["summary"]["exact_match_count"], 1)
        companion_paths = {
            item["path"]
            for item in comparison["companion_changes_absent_from_intake"]
        }
        self.assertEqual(
            companion_paths,
            {
                "pyproject.toml",
                "src/python/example/documents/__init__.py",
            },
        )

    def test__render_markdown__shows_execution_boundaries(
        self,
    ) -> None:
        report = analyze_python_intake(_FIXTURES / "complete")

        rendered = render_markdown(report)

        self.assertIn("# Python intake analysis", rendered)
        self.assertIn("**lint** (static)", rendered)
        self.assertIn("**tests** (executes intake code)", rendered)

    def test__main__rejects_invalid_limits(self) -> None:
        errors = io.StringIO()
        with redirect_stderr(errors):
            exit_code = main(
                [
                    "--max-files",
                    "0",
                    "analyze",
                    str(_FIXTURES / "complete"),
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertIn("max_files must be positive", errors.getvalue())

    @staticmethod
    def _write(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @staticmethod
    def _git(repository: Path, *arguments: str) -> str:
        return subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
        ).stdout


if __name__ == "__main__":
    unittest.main()
