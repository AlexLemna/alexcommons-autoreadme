from __future__ import annotations

from argparse import ArgumentParser
import sys

from alexcommons_autoreadme._cli import detailed_version_output
from alexcommons_autoreadme._metadata import APP_NAME, __version__


def parse():

    parser = ArgumentParser(prog=APP_NAME)

    # -v, --verbose
    valid_args = ("-v", "--verbose")
    help = f"display additional information while the app runs"
    parser.add_argument(*valid_args, action="store_true", help=help)

    # Informational commands
    # ----------------------
    version_cmds = parser.add_mutually_exclusive_group()
    # -V, --version
    valid_args = ("-V", "--version")
    help = f"""Display {APP_NAME}'s version, then exit. Can be called twice ('-VV')
for more information."""
    version_display = f"{APP_NAME} {__version__}"
    version_cmds.add_argument(*valid_args, action="count", help=help, default=0)

    def show_version(detailed: bool = False):
        lines_to_display = [version_display]
        if detailed:
            lines_to_display.append(f"     at {__file__}")
            # plus additional info...
            lines_to_display = detailed_version_output(lines_to_display)

        for line in lines_to_display:
            print(line)

    # --version-number
    valid_args = ("--version-number",)
    help = f"""Display {APP_NAME}'s version number only, then exit. Intended as a
convenience function for scripting purposes, etc."""
    version_cmds.add_argument(*valid_args, action="store_true", help=help)

    # ==============
    # Actual parsing
    # ==============
    args = parser.parse_args()
    if args.verbose:
        print(f"DEBUG parsing: sys.argv[1:]: {sys.argv[1:]}")
        print(f"DEBUG parsing: parsed: {args}")

    if args.version or args.version_number:
        if args.version_number:
            print(__version__)
        elif args.version == 1:
            show_version()
        elif args.version >= 2:
            show_version(detailed=True)
        return
