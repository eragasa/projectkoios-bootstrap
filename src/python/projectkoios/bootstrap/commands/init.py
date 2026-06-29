import shutil

from projectkoios.bootstrap.models import HARNESSES, GLOBAL_DIR


def register(subparsers) -> None:
    parser = subparsers.add_parser("init", help="Copy agents/global/*.example → ~/.<harness>/")
    parser.set_defaults(func=run)


def run(args) -> None:
    if not GLOBAL_DIR.exists():
        print(f"error: global config directory not found: {GLOBAL_DIR}")
        return

    for harness in HARNESSES:
        src = GLOBAL_DIR / harness.name
        if not src.exists():
            print(f"skip: {harness.name} — no global config at {src}")
            continue

        dst = harness.config_dir
        dst.mkdir(parents=True, exist_ok=True)

        for item in src.iterdir():
            if item.is_dir():
                continue
            name = item.name
            if name.endswith(".example"):
                target_name = name.removesuffix(".example")
            else:
                target_name = name
            target = dst / target_name
            if target.exists():
                print(f"  exist: {target}")
            else:
                shutil.copy2(item, target)
                print(f"  wrote: {target}")

    print("done: init complete")
