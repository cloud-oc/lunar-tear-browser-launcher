#!/bin/sh
set -eu
cd "$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
if [ ! -x .venv/bin/python ]; then
  printf 'Run sh setup.sh first.\n' >&2
  exit 1
fi
exec .venv/bin/python launcher.py "$@"
