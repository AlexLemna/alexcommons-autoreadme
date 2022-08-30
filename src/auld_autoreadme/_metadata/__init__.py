# -*- coding: utf-8 -*-
from __future__ import annotations

from auld_autoreadme._metadata.version import AppVersion, VersionFromFile

APP_NAME = "alexcommons-autoreadme"
__version__ = str(VersionFromFile())
__version_info__ = VersionFromFile().release
