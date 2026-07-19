"""image-wormhole CLI entry point.

Subcommands are registered as features land (threshold, extract, ...).
"""

from __future__ import annotations

import argparse

from image_wormhole import __version__
from image_wormhole.ops import adaptive as adaptive_op
from image_wormhole.ops import threshold as threshold_op


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="iw",
        description="Batch-process photos into graphic-art variants.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    # Each feature registers its own subcommand here.
    threshold_op.add_parser(subparsers)
    adaptive_op.add_parser(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    # Subcommands attach a callable via set_defaults(func=...).
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
