from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from auld_autoreadme._metadata.version_pep440 import PEP440Version
from auld_autoreadme._utils import NoValueEnum


class Scm(NoValueEnum):
    UNKNOWN = "unknownSCM"
    GIT = "git"
    MERCURIAL = "hg"

    def __str__(self) -> str:
        return self.value


@dataclass
class LocalVersionScheme:
    latest_commit_id: str | None = None
    commits_since_tag: int = 0
    dirty: bool = False
    scm: Scm | None = None

    def __init__(
        self, local_version: str | None = None, dev_version: int | None = None
    ):
        if dev_version:
            self.commits_since_tag = dev_version
        if local_version:
            local_parts = local_version.split(".", maxsplit=1)

            for part in local_parts:
                if part[0] == "d":
                    self.dirty = True

                elif part[0] == "g":
                    self.scm = Scm.GIT
                    self.latest_commit_id = part[1:]
                elif part[0] == "h":
                    self.scm = Scm.MERCURIAL
                    self.latest_commit_id = part[1:]
                else:
                    self.scm = Scm.UNKNOWN
                    self.latest_commit_id = part

    def __str__(self) -> str:
        parts = []

        if self.commits_since_tag > 0:
            parts.append(self.scm)
            parts.append(self.commits_since_tag)
            parts.append(self.latest_commit_id)

        if self.dirty:
            parts.append("dirty")

        if len(parts) == 0:
            return ""
        elif len(parts) == 1:
            return str(parts[0])
        elif len(parts) >= 2:
            return ".".join([str(p) for p in parts])


class VersionFromFile(PEP440Version):
    def __init__(self):
        this_dir = Path(__file__).parent
        version_file = this_dir / "version.txt"
        with version_file.open(mode="r") as f:
            version = f.readlines()[0]
        super().__init__(version)


@dataclass
class AppVersion(PEP440Version):

    scm: Scm | None = None

    def __init__(self):
        this_dir = Path(__file__).parent
        version_file = this_dir / "version.txt"
        with version_file.open(mode="r") as f:
            self.embedded_version = f.readlines()[0]
        super().__init__(self.embedded_version)

    def __str__(self) -> str:
        parts = []

        # Epoch
        if self.epoch != 0:
            parts.append(f"{self.epoch}!")

        # Release segment
        parts.append(".".join(str(x) for x in self.release()))

        # Pre-release
        if self.pre is not None:
            parts.append("".join([str(x) for x in self.pre]))

        # Post-release
        if self.post is not None:
            parts.append(f".post{self.post}")

        # Development release or local version segment
        if self.custom_local is not None:
            parts.append(f"+{self.custom_local}")

        return "".join(parts)

    @property
    def in_dev_environment(self) -> bool:
        if self.scm is None:
            return False
        else:
            return True

    def release(self) -> tuple[int, ...]:
        return super().release

    @property
    def custom_local(self) -> str | None:

        # 0.1.3.dev0+g00bd5ef.d20220829
        if "+" not in self.embedded_version and self.dev is None:
            return None
        else:
            # g00bd5ef.d20220829
            local_part = self.embedded_version.split("+", maxsplit=1)[-1]

            local_version = LocalVersionScheme(
                local_version=local_part, dev_version=self.dev
            )
            local_version = str(local_version)
            return local_version


if __name__ == "__main__":
    version = AppVersion()
    print(version.embedded_version)

    print(version)
