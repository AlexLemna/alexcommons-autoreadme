"""Various program utilities."""
from __future__ import annotations

from enum import Enum
from pathlib import Path


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


def any_tomllib():
    try:
        try:  # Python >= 3.11
            import tomllib
        except ImportError:  # Python < 3.11
            import tomli as tomllib

        return tomllib

    except ImportError:  # Python < 3.11 and no backported tomllib
        return None


def any_importlib_metadata():
    try:
        try:  # Python >= 3.8
            import importlib.metadata as implibmd
        except ImportError:  # Python < 3.8
            import importlib_metadata as implibmd

        return implibmd

    except ImportError:  # Python < 3.8 and no backported importlib.metadata
        return None


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


def setuptools_scm_or_nuthin():
    try:
        import setuptools_scm

        return setuptools_scm
    except ImportError:
        return None


def find_pyproject_toml_dir(start_path: Path) -> Path:
    if start_path.is_file():
        start_path = start_path.parent
    for child in start_path.iterdir():
        if child.is_file() and child.name("pyproject.toml"):
            return start_path
    return find_pyproject_toml_dir(start_path.parent)


def dir_readme(dir_path: Path) -> Path:
    if dir_path.is_dir() is False:
        result = dir_readme(dir_path=Path(__file__).parent)
        return result

    readme = dir_path / "README.md"
    if readme.exists():
        return readme
    elif readme.exists() is False:
        ...


# https://docs.python.org/3/library/enum.html#omitting-values
class NoValueEnum(Enum):
    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)
