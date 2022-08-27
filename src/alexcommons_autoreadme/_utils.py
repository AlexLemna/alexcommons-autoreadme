from __future__ import annotations


def clean_multiline_str(string: str) -> str:
    s = " ".join(string.splitlines())
    return s


def is_tomllib_here() -> bool | str:
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
