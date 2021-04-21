#!/bin/bash

# Pokud nechcete cekat na odezvu, spustte skript na pozadi:
# nohup download.sh &

TOOLBOX_HOME="${RUIAN_TOOLBOX_HOME:-/opt/ruian/toolbox}"
DOWNLOAD_HOME="${RUIAN_DOWNLOAD_HOME:-/opt/ruian/toolbox/downloader}"
DOWNLOAD_DATA="${RUIAN_DOWNLOAD_DATA:-/opt/ruian/data}"

LOG_DIR="${RUIAN_LOG:-/var/log/ruian}"

echo "Tento skript stahuje data z VDP"
echo "-------------------------------"
echo "Pro informaci o prubehu stahovani, sledujte obsah souboru DownloadRUIAN.log"
echo "a DownloadRUIANErr.log, pripadne ostatni logovaci soubory v adresari se"
echo "stazenymi daty."
echo "Download muze trvat pri pomalem pripojeni k internetu nekolik desitek minut."
echo "Pokud je konfigurace nastavena tak, aby ihned po stazeni byla data importovana"
echo "do databaze, muze byt cely ukoncen az za nekolik hodin."
echo "-------------------------------"
echo "!!!Nezavirejte toto okno do ukonceni skriptu!!!"

cd "$TOOLBOX_HOME" || exit
export DOWNLOAD_DATA
mkdir -p "$LOG_DIR"
python download_ruian.py 2>>DownloadRUIAN.log 3>>DownloadRUIANErr.log
mv ./*.log "$LOG_DIR"
cd "$TOOLBOX_HOME" || exit
