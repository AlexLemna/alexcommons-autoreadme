# -*- coding: utf-8 -*-
"""`__main__.py` allows this program to run without being imported - for
instance, from the command line.
"""
from __future__ import annotations

import alexcommons_autoreadme.app


def run():
    """Run alexcommons-autoreadme."""
    alexcommons_autoreadme.app.parse()
