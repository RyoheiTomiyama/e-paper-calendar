#!/bin/bash

SHELL=/bin/bash
PYENV_ROOT=$HOME/.anyenv/envs/pyenv
POETRY_ROOT=$HOME/.poetry
PATH=$PYENV_ROOT/bin:$PYENV_ROOT/shims:$POETRY_ROOT/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

if command -v pyenv 1>/dev/null 2>&1; then
	eval "$(pyenv init -)"
fi

cd ~/epaper/e-paper-calendar
poetry run python main.py

