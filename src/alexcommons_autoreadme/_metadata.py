# -*- coding: utf-8 -*-
"""Contains app metadata, like program name and version."""
from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # Python < 3.8
    from importlib_metadata import PackageNotFoundError, version

__all__ = ["__version__", "__version_info__"]

# see https://milkr.io/kfei/5-common-patterns-to-version-your-Python-package

APP_NAME = "alexcommons-autoreadme"
VERSION_UNKNOWN = "version could not be detected"

try:
    __version__ = version(APP_NAME)
except (PackageNotFoundError, NameError):
    __version__ = VERSION_UNKNOWN

__version_info__ = (
    tuple(int(n) for n in __version__.split("."))
    if __version__ is not VERSION_UNKNOWN
    else (-1, -1)
)

if __name__ == "__main__":
    print(f"__version__: {__version__}")
    print(f"__version_info__: {__version_info__}")
