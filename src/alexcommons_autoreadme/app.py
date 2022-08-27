from __future__ import annotations

from argparse import ArgumentParser
import sys

from alexcommons_autoreadme._metadata import APP_NAME, __version__


def parse():
    parser = ArgumentParser(prog=APP_NAME)

    v_args = ("-V", "--version")
    v_help = f"display {APP_NAME}'s version"
    v_display = f"{APP_NAME} {__version__}"
    parser.add_argument(*v_args, action="version", help=v_help, version=v_display)

    parser.parse_args(sys.argv)
