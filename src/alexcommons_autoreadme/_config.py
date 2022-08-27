# -*- coding: utf-8 -*-
"""Application configuration data."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from alexcommons_autoreadme._metadata import APP_NAME
from alexcommons_autoreadme._utils import clean_multiline_str

try:
    import tomllib
    from tomllib import TOMLDecodeError
except ImportError:
    # Python < 3.11
    try:
        import tomli as tomllib
        from tomli import TOMLDecodeError
    except ImportError:
        print(
            clean_multiline_str(
                f"""{APP_NAME} failed to import tomllib and tomli, and so cannot
read settings in pyproject.toml."""
            )
        )
        tomllib = None


class TOMLHandler:
    """Loads a TOML file, and allows access to the contents."""

    def __init__(self, file: Path) -> None:
        """Initializes the TOML handler."""
        self.file = file
        with self.file.open("rb") as f:
            self.filedict = tomllib.load(f)
        try:
            self.config = self.filedict["tool"]["alexcommons-autoreadme"]
        except KeyError:
            self.config = None

    def get_value(self, key):
        """Access a value in the TOML file."""
        try:
            result = self.config[key]
        except KeyError:
            result = None
        return result


class Config:
    """The application configuration.

    Access individual settings via the attributes of `Config.settings`.
    """

    @dataclass(frozen=True)
    class ConfigData:
        """Data to be read from the config file."""

        config_file: Path
        root_dir: Path
        out_dir: Path

    def __init__(self, path: Path) -> None:
        """Initializes `ConfigData()` by recursively searching upwards from
        a given `path` for a file `pyproject.toml`.
        """
        self._settings = None

        for directory in path.parents:
            while self._settings is None:
                self._settings = self.__load_data(directory)

    def __load_data(self, path: Path) -> ConfigData | None:
        """Searches through all the items in a directory for a file named
        `pyproject.toml`. If found, reads that file for our conifiguration and
        returns it in a `ConfigData` object. If not found, returns `None`.
        """
        for childitem in path.iterdir():
            if childitem.name == "pyproject.toml":
                file = TOMLHandler(childitem)
                if file.config:
                    return self.ConfigData(
                        config_file=childitem,
                        root_dir=path,
                        temp_dir=file.get_value("temp_dir"),
                    )
        return None

    @property
    def settings(self) -> ConfigData | None:
        """Settings in the configuration file (`pyproject.toml`)."""
        return self._settings
