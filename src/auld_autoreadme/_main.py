from __future__ import annotations

from dataclasses import asdict, dataclass, field
import fnmatch
from pathlib import Path
from pprint import pformat, pprint
import re
from typing import Any

try:  # Python >= 3.11
    import tomllib
except ImportError:  # Python < 3.11
    import tomli as tomllib

from gitignore_parser import parse_gitignore


def main_program(path: Path):
    if not isinstance(path, Path):
        return main_program(Path(path))
    if path.is_file():
        parent_dir = path.parent
        return main_program(path=parent_dir)

    @dataclass
    class Data:
        project_root: Path
        project_config: dict[str, Any] = field(init=False)
        project_config_file: Path = field(init=False)
        project_gitignore: Path = field(init=False)
        project_dirs: set[Path] = field(init=False)
        project_gitignore_dirs: set[str] = field(init=False)

        def __post_init__(self):

            self.project_config_file = self.project_root / "pyproject.toml"

            with self.project_config_file.open(mode="rb") as f:
                self.project_config = tomllib.load(f)

            self.project_gitignore = self.project_root / ".gitignore"

            with self.project_gitignore.open(mode="r") as f:
                lines = [line.strip() for line in f.readlines()]
            self.project_gitignore_dirs = set(
                [
                    re.compile(fnmatch.translate(line))
                    for line in lines
                    if (not line.startswith("#")) and (line != "")
                ]
            )

            self.project_dirs = set()
            for path in self.project_root.rglob("*"):
                path = path.relative_to(self.project_root)
                if path.is_dir():
                    if (
                        (path.name == ".git")
                        or (Path(".git") in path.parents)
                        or any(
                            pattern.search(str(path.resolve()))
                            for pattern in self.project_gitignore_dirs
                        )
                    ):
                        pass
                    else:
                        # print(f"{self.gitignore_contains(path)}   {path}")
                        self.project_dirs.add(path)

        def gitignore_contains(self, path: str | Path):
            path_to_check = str(path) if isinstance(path, Path) else path
            matches = parse_gitignore(self.project_gitignore)
            return matches(path_to_check)

    # Find the parent directory containing pyproject.toml
    directory_contents = [child.name for child in path.iterdir()]
    if "pyproject.toml" not in directory_contents:
        main_program(path=path.parent)

    #
    else:
        data = Data(project_root=path)
        with data.project_gitignore.open("r") as f:
            gitignore_patterns = [
                line.strip()
                for line in f.readlines()
                if (not line.startswith("#")) and (line != "")
            ]

        data = [str(p) for p in data.project_dirs]
        data = [p.replace("\\", "/") for p in data]
        gitignore_patterns = set(gitignore_patterns)

        _gitignore_extras = [
            f"{p}*" if p.endswith("/") else p.removesuffix("/")
            for p in gitignore_patterns
        ]
        gitignore_patterns.update(_gitignore_extras)
        gitignore_patterns.update(
            [f"{p}/" for p in gitignore_patterns if not p.endswith("/")]
        )

        # filenames = [
        #     n
        #     for n in data
        #     if not any(fnmatch.fnmatch(n, pattern) for pattern in gitignore_patterns)
        # ]

        for n in data:
            if not any(fnmatch.fnmatch(n, pattern) for pattern in gitignore_patterns):
                print(n)

        # with Path("DATA.txt").open(mode="w") as f:
        #     f.write(pformat(filenames))


if __name__ == "__main__":
    main_program(__file__)
