# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import SupportsInt

VERSION_PATTERN = r"""
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
"""
"""From https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions"""

VERSION_REGEX = re.compile(
    r"^\s*" + VERSION_PATTERN + r"\s*$",
    re.VERBOSE | re.IGNORECASE,
)
"""From https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions"""


def parse_letter_version(
    letter: str | None = None, number: str | SupportsInt | None = None
) -> tuple[str, int] | None:
    """Parses pre-release and post-release versions."""

    if letter:
        # If we aren't given a number for the pre- or post-release (i.e. 1.1a,
        # 4.4beta), then consider there to be an implicit 0 (i.e. 1.1a0, 4.4beta0)
        if number is None:
            number = 0

        # make everything lowercase
        letter = letter.lower()

        # PEP440 says 'a', 'b', 'rc', and 'post' are the canonical representations
        # of "alpha", "beta", prereleases and postreleases.
        if letter == "alpha":
            letter = "a"
        elif letter == "beta":
            letter = "b"
        elif letter in ["c", "pre", "preview", "releasecandidate", "release-candidate"]:
            letter = "rc"
        elif letter in ["rev", "r", "revision", "postrelease", "post-release"]:
            letter = "post"

        return letter, int(number)
    if not letter and number:
        # We assume if we are given a number but no letter, then we assume it's
        # a post release syntax (e.g. 1.0-1)
        letter = "post"

        return letter, int(number)

    return None


def parse_local_version(local: str):
    """Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve")."""
    _local_version_separators = re.compile(r"[\._-]")

    if local is not None:
        return tuple(
            part.lower() if not part.isdigit() else int(part)
            for part in _local_version_separators.split(local)
        )
    return None


class PEP440Version:
    """A simplified version of https://packaging.pypa.io/en/stable/_modules/packaging/version.html#Version.
    It doesn't need to be compared to other versions, but it does need to be able to parse PEP440-like strings.
    """

    @dataclass(frozen=True)
    class Data:
        epoch: int
        release: tuple[int, ...]
        pre: tuple[str, int]
        post: tuple[str, int]
        dev: tuple[str, int]
        local: tuple[str, int]

    def __init__(self, version: str):

        # validate 'version' and parse it into components
        match = VERSION_REGEX.search(version)
        if not match:
            raise ValueError(f"Invalid version: {version}")

        # store the parsed components
        self._data = self.Data(
            epoch=int(match.group("epoch")) if match.group("epoch") else 0,
            release=tuple(int(i) for i in match.group("release").split(".")),
            pre=parse_letter_version(
                letter=match.group("pre_l"),
                number=match.group("pre_n"),
            ),
            post=parse_letter_version(
                letter=match.group("post_l"),
                number=match.group("post_n1") or match.group("post_n2"),
            ),
            dev=parse_letter_version(
                letter=match.group("dev_l"),
                number=match.group("dev_n"),
            ),
            local=parse_local_version(match.group("local")),
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self}')>"

    def __str__(self) -> str:
        parts = []

        # Epoch
        if self.epoch != 0:
            parts.append(f"{self.epoch}!")

        # Release segment
        parts.append(".".join(str(x) for x in self.release))

        # Pre-release
        if self.pre is not None:
            parts.append("".join(str(x) for x in self.pre))

        # Post-release
        if self.post is not None:
            parts.append(f".post{self.post}")

        # Development release
        if self.dev is not None:
            parts.append(f".dev{self.dev}")

        # Local version segment
        if self.local is not None:
            parts.append(f"+{self.local}")

        return "".join(parts)

    @property
    def epoch(self) -> int:
        _epoch: int = self._data.epoch
        return _epoch

    @property
    def release(self) -> tuple[int, ...]:
        _release: tuple[int, ...] = self._data.release
        return _release

    @property
    def pre(self) -> tuple[str, int] | None:
        _pre: tuple[str, int] | None = self._data.pre
        return _pre

    @property
    def post(self) -> int | None:
        return self._data.post[1] if self._data.post else None

    @property
    def dev(self) -> int | None:
        return self._data.dev[1] if self._data.dev else None

    @property
    def local(self) -> str | None:
        if self._data.local:
            return ".".join(str(x) for x in self._data.local)
        else:
            return None

    @property
    def public(self) -> str:
        return str(self).split("+", 1)[0]

    @property
    def base_version(self) -> str:
        parts = []

        # Epoch
        if self.epoch != 0:
            parts.append(f"{self.epoch}!")

        # Release segment
        parts.append(".".join(str(x) for x in self.release))

        return "".join(parts)

    @property
    def is_prerelease(self) -> bool:
        return self.dev is not None or self.pre is not None

    @property
    def is_postrelease(self) -> bool:
        return self.post is not None

    @property
    def is_devrelease(self) -> bool:
        return self.dev is not None

    @property
    def major(self) -> int:
        return self.release[0] if len(self.release) >= 1 else 0

    @property
    def minor(self) -> int:
        return self.release[1] if len(self.release) >= 2 else 0

    @property
    def micro(self) -> int:
        return self.release[2] if len(self.release) >= 3 else 0


if __name__ == "__main__":
    # vs = [
    #     "10.5.2",
    #     "10.5.1+3.g00bd5ef.dirty",
    #     "10.5.1+3.g00bd5ef.clean",
    #     "10.5.1+0.dirty",
    #     "10.5.1",
    #     "10.5.1rc",
    #     "10.5.1b1",
    #     "10.5.1a7",
    #     "10.5.1a7dev7",
    #     "1.2022.8.28.1a",
    # ]
    # for v in vs:
    #     print(PEP440Version(v).micro)
    from pathlib import Path

    from auld_autoreadme._metadata import read_version

    v = PEP440Version(read_version())
    print(v)
