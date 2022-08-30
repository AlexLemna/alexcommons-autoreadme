# auld_autoreadme / alexcommons-autoreadme

1. Find the project's root directory by looking for pyproject.toml.
   - see `auld_autoreadme._project_classes:Project`
2. Create a set of the project's gitignore rules.
   - see `auld_autoreadme._gitignore`
3. Create a set of the project's directories, matching them against gitignore.
   - see `auld_autoreadme._project_classes:ProjectDirectory`
4. For directory in project_directories, create a README if no README exists.
Title the readme with the directory's relative path from the project root.
   - see `auld_autoreadme._readme`
5. In the README, create a 'tree' or a basic code-style list of the project's
contents (matched against gitignore), with each Python file or module being
followed by its docstrings. For non-Python files, have a list of common files
and their descriptions (`requirements.txt` -> A project's Python dependencies,
`.pre-commit-config.yaml` -> configuration for pre-commit, etc.).
   - see `auld_autoreadme._tree`

## Dev notes to self

- Still feels like there's something about setuptools_scm/my environment that I'm not understanding. Occasionally getting unexpected results.

### Devops todo

- Update and add bootstrapping scripts
- What's up with CODEOWNERS? (I should read [this](https://medium.com/expedia-group-tech/owning-your-codeowners-file-332e288c1d12) article, looks like it covers common troubleshooting)
  - See also [GitHub blog post](https://github.blog/2017-07-06-introducing-code-owners/) and [official docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- Sphinx or some sort of autodocumentation
- PyTest
- Add licensing to each file via [reuse](https://reuse.readthedocs.io/en/stable/index.html) ([more info](https://reuse.software/tutorial/))
  - See [here](https://opensource.stackexchange.com/a/7685) for some reasoning
  - Or maybe use the [livenseheaders](https://pypi.org/project/licenseheaders/) package
- Add [pyupgrade](https://github.com/asottile/pyupgrade) as pre-commit hook

Also look into:

- [towncrier](https://github.com/twisted/towncrier) for Changelogs
- [Semantic Pull Requests](https://github.com/apps/semantic-pull-requests): See this [nice blog post](https://mestrak.com/blog/semantic-release-with-python-poetry-github-actions-20nn).
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): I want tool that will help me do this, that I can configure from `pyproject.toml`. Commitizen looks good.
  - [commitlint](https://commitlint.js.org/#/reference-configuration)
  - [commitizen](https://commitizen-tools.github.io/commitizen/config/)
- Automated pull requests (see [here](https://peterevans.dev/posts/github-actions-how-to-create-pull-requests-automatically/) for inspiration)

Eventually:

- CONTRIBUTING (or at least something like [this](https://gist.github.com/mherrmann/5ce21814789152c17abd91c0b3eaadca))
- spellcheck for documentation?
- [in-solidarity-bot](https://github.com/apps/in-solidarity) might open up a debate I'm not excited about, but I like consistent styles and [some of the suggested alternatives seem clearer and more precise than the original language](https://github.com/jpoehnelt/in-solidarity-bot/blob/main/src/rules.ts)

### Other tools to try to make

- auld-version: a python module with a class that models/parses my versioning schemes:
   - `MAJOR.YYYY0M0D[.MINOR][.MICRO][{a|b|rc}N][.postN][+LOCAL]`
   - `MAJOR.YYYY.MM.DD[.MINOR][.MICRO][{a|b|rc}N][.postN][+LOCAL]`
   - with the `LOCAL` section being displayed when Git or Mercurial is detected, and the rough logic being:
     - **no distance and clean**: `+clean.{git|hg}`
     - **distance and clean**: `+clean.{git|hg}.{branch name}.{distance}.{revision hash}`
     - **no distance and dirty**: `+dirty.{git|hg}`
     - **distance and dirty**: `+dirty.{git|hg}.{branch name}.{distance}.{revision hash}`
