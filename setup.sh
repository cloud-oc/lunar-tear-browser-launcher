#!/bin/sh
set -eu
cd "$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
PYTHON=${PYTHON:-python3}
if [ ! -x .venv/bin/python ]; then
  "$PYTHON" -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ required"'
  "$PYTHON" -m venv .venv
fi
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python launcher.py init
printf '\nSetup complete. Edit config.json and follow README.md.\n'
