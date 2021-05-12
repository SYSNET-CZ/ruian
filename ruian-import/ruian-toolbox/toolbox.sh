#!/bin/bash

TOOLBOX_HOME="${RUIAN_TOOLBOX_HOME:-/opt/ruian/toolbox}"

cd "$TOOLBOX_HOME" || exit
python ruian_toolbox.py
cd "$TOOLBOX_HOME" || exit
