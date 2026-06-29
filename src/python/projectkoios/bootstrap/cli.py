import argparse
import sys

from projectkoios.bootstrap.commands import init, install, harnesses


def main() -> None:
    parser = argparse.ArgumentParser(prog="projectkoios", description="Project Koios bootstrap CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    boot = subparsers.add_parser("bootstrap", help="Bootstrap commands")
    boot_sub = boot.add_subparsers(dest="action")
    boot_sub.required = True

    init.register(boot_sub)
    install.register(boot_sub)
    harnesses.register(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
