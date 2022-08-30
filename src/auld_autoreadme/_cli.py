# -*- coding: utf-8 -*-
"""Helper functions for the command-line interface."""
from __future__ import annotations

from pathlib import Path
import platform
import sys

try:
    from importlib.metadata import PackageNotFoundError, files
except ImportError:  # Python < 3.8
    try:
        from importlib_metadata import PackageNotFoundError, files
    except ImportError:
        pass

from auld_autoreadme._metadata import APP_NAME
from auld_autoreadme._utils import (
    clean_multiline_str,
    is_importlib_metadata_here,
    is_tomllib_here,
)


def detailed_version_output() -> list[str]:
    """Returns a list of details about dependencies, Python, and the operating system."""
    detailed_output = []
    if is_importlib_metadata_here():
        # 'via \foo\bar\Scripts\alexcommons-autoreadme.exe'
        detailed_output.append(f"        via {Path(files(APP_NAME)[0]).resolve()}")

    # check for tomllib (or tomli backport)
    tomllib = is_tomllib_here()
    if tomllib is False:
        detailed_output.append("    with tomllib missing")
    elif tomllib is not True:
        detailed_output.append(f"    with {tomllib}")

    # check for importlib.metadata (or importlib_metadata backport)
    implibmd = is_importlib_metadata_here()
    if implibmd is False:
        detailed_output.append("    with importlib.metadata missing")
    elif implibmd is not True:
        detailed_output.append(f"    with {implibmd}")

    # get system and platform information
    detailed_output.extend(
        [
            f"Python {sys.version}",  # Python x.y.z (git branch & commit info) (target platform info)
            platform.platform(aliased=True),  # Java, macOS/Darwin, Linux, Unix, Windows
        ]
    )
    if platform.system() == "Windows" and platform.release() == "10":
        detailed_output.append(
            clean_multiline_str(
                """    (Windows versions rarely match their marketing names.
Windows 11 may still appear as Windows 10.)"""
            )
        )

    return detailed_output
