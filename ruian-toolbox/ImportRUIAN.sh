#!/bin/bash

TOOLBOX_HOME="${RUIAN_TOOLBOX_HOME:-/opt/ruian/toolbox/downloader}"
IMPORT_HOME="${RUIAN_IMPORT_HOME:-/opt/ruian/toolbox/importer}"
LOG_DIR=="${RUIAN_LOG:-/var/log/ruian}"

echo Tento skript importuje data stazena z VDP do databaze.
echo ------------------------------------------------------
echo Pro informaci o prubehu importu, sledujte obsah souboru ImportRUIAN.log a ImportRUIANErr.log, pripadne ostatni logovaci soubory v adresari se stazenymi daty.
echo Import muze dle nastaveni a rychlosti pocitace trvat i nekolik hodin.
echo ------------------------------------------------------
echo !!!Nezavirejte toto okno do ukonceni skriptu!!!

cd $IMPORT_HOME
mkdir -p $LOG_DIR
python importruian.py 2>>ImportRUIAN.log 3>>ImportRUIANErr.log
mv *.log $LOG_DIR
cd $TOOLBOX_HOME
