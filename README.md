# alexcommons-autoreadme

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
