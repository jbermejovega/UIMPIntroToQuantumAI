#!/usr/bin/env sh
set -eu

PYTHON="${PYTHON:-python3}"

"$PYTHON" -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo
echo "Installed public QML codebook environment."
echo "Start with:"
echo "  jupyter lab ising_duality_codebook.ipynb"
echo
echo "Optional SIGIL4Py layer, when available from your configured public package source:"
echo "  python -m pip install sigil4py"
