"""Image-processing operations, one module per technique.

Each op module exposes:
    add_parser(subparsers)  # register its CLI subcommand
    run(args) -> int        # execute, return exit code
"""
