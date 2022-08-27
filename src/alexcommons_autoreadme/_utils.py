# -*- coding: utf-8 -*-
"""Various program utilities."""
from __future__ import annotations


def clean_multiline_str(string: str) -> str:
    """Turns a multi-line string into a single-line string."""
    s = " ".join(string.splitlines())
    return s


def is_tomllib_here() -> bool | str:
    """Checks if tomllib can be imported.

    Returns:
    - `True` if `tomllib` can be imported
    - `f"tomli {VERSION}"` if `tomllib` cannot be imported but
    tomli can
    - `False` if neither `tomllib` nor `tomli` can be imported
    """
    try:
        import tomllib

        return True
    except ImportError:
        # Python < 3.11
        try:
            import tomli

            return f"tomli {tomli.__version__}"
        except ImportError:
            # Python < 3.11 and no backported tomllib
            return False


def is_importlib_metadata_here() -> bool | str:
    """Checks if importlib.metadata can be imported.

    Returns:
    - `True` if `importlib.metadata` can be imported
    - `f"importlib_metadata {VERSION}"` if `tomllib` cannot be imported but
    tomli can
    - `False` if neither `importlib.metadata` nor `importlib_metadata` can be imported
    """
    try:
        import importlib.metadata

        return True
    except ImportError:
        # Python < 3.8
        try:
            import importlib_metadata

            # Ironically, importlib_metadata doesn't have a __version__
            # exposed. Fortunately, we know a library that'll handle that,
            # and it's not just for our own metadata...
            implibmd_version = importlib_metadata.version("importlib_metadata")
            return f"importlib_metadata {implibmd_version}"
        except ImportError:
            # Python < 3.8 and no backported importlib.metadata
            return False
