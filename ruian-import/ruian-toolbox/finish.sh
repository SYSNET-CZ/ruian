#!/bin/bash

# Pokud nechcete cekat na odezvu, spustte skript na pozadi:
# nohup finish.sh &

TOOLBOX_HOME="${RUIAN_TOOLBOX_HOME:-/opt/ruian/toolbox}"
DOWNLOAD_DATA="${RUIAN_DOWNLOAD_DATA:-/opt/ruian/data}"
LOG_DIR="${RUIAN_LOG:-/var/log/ruian}"

echo "Tento skript provede zaverecne osetreni databaze."
echo "------------------------------------------------------"
echo "Odstrani se duplicitni zaznamy a ponechaji pouze aktualni."
echo "Vytvori se podpurne tabulky potrebne pro sluzby nad databazi."
echo ------------------------------------------------------
echo "!!!Nezavirejte toto okno do ukonceni skriptu!!!"

cd "$TOOLBOX_HOME" || exit
export DOWNLOAD_DATA
mkdir -p "$LOG_DIR"
python finish.py 2>>FinishRUIAN.log 3>>FinishRUIANErr.log
mv ./*.log "$LOG_DIR"
cd "$TOOLBOX_HOME" || exit
