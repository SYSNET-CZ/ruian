# RUIAN Importer

Obraz Docker poskytující službu **downloadu** a **importu** dat RUIAN.
Download i import se provádějí pomocí úlohy cron spouštěné každou neděli.
Obraz vychází ze základního obrazu pro GIS aplikace **sysnetcz/ruian-base:latest**.

## Vytvoření obrazu

Obraz se vytvoří příkazem

        # docker build -t sysnetcz/ruian-import .

## Ruční spuštění kontejneru

Pro produkční účely doporučujeme vytvořit komplentí implementaci služby pomocí **docker-compose**, avšak pro testovací a/nebo poloprovozní účel postačí ruční vytvoření kontejneru. Pozor přitom na vzájemnou viditelnost kontejnerů.

        # docker run -d --name ruian-import --network ruian-net -t sysnetcz/ruian-import

Předpokládá se, že kontejner **postgis** se nachází v síti **ruian-net**.
