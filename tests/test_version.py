# -*- coding: utf-8 -*-
from __future__ import annotations

import packaging.version

import auld_autoreadme


def test_dunder_version():
    version = alexcommons_autoreadme.__version__
    assert isinstance(version, str)


def test_dunder_version_is_canonical_pep440():
    version = packaging.version.parse(alexcommons_autoreadme.__version__)

    # Check that it's a Version and isn't LegacyVersion
    # (removed in packaging v22) or InvalidVersion
    assert isinstance(version, packaging.version.Version)


def test_dunder_version_info():
    version_info = alexcommons_autoreadme.__version_info__
    assert isinstance(version_info, tuple)
    for n in version_info:
        assert isinstance(n, int)


def test_dunder_version_equals_dunder_version_info():
    version = alexcommons_autoreadme.__version__
    version_info = alexcommons_autoreadme.__version_info__

    assert version == ".".join(str(i) for i in version_info)
    assert version_info == tuple(int(s) for s in version.split("."))


if __name__ == "__main__":
    import pytest

    pytest.main()
