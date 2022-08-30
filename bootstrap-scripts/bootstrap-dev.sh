# This script should work for bash, zsh, etc. For other scripts,
# see the 'bootstrap-scripts' folder

python -m venv .venv --upgrade-deps
. /bin/activate
pre-commit install --install-hooks --overwrite
