# -*- coding: utf-8 -*-
"""High-level program functionality for alexcommons_autoreadme."""
from __future__ import annotations

from argparse import ArgumentParser
import sys

from auld_autoreadme import __version__
from auld_autoreadme._cli import detailed_version_output
from auld_autoreadme._metadata import APP_NAME

# from alexcommons_autoreadme._version import __version__


def parse():
    """Parse user input from the command line."""

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
        """Displays program version data, plus optional details."""
        lines_to_display = [version_display]
        if detailed:
            lines_to_display.append(f"    at {__file__}")
            # plus additional info...
            lines_to_display.extend(detailed_version_output())

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


def main():
    """Main app behavior.

    0. Find the project's root directory by looking for pyproject.toml.
    0. Create a set of the project's gitignore rules.
    0. Create a set of the project's directories, matching them against gitignore.
    0. For directory in project_directories, create a README if no README exists.
    Title the readme with the directory's relative path from the project root.
    0. In the README, create a 'tree' or a basic code-style list of the project's
    contents (matched against gitignore), with each Python file or module being
    followed by its docstrings. For non-Python files, have a list of common files
    and their descriptions (requirements.txt -> A project's Python dependencies,
    .pre-commit-config.yaml -> configuration for pre-commit, etc.).

    """
