# RUIAN Services

Obraz Docker poskytující webové služby nad replikou RUIAN.
Je použit http server Apache2.
Obraz vychází ze základního obrazu pro GIS aplikace **sysnetcz/ruian-base:latest**.

## Vytvoření obrazu

Obraz se vytvoří příkazem

        # cd ..
        # cd ..
        # docker build -f ${PWD}/docker/services/Apache.Dockerfile -t sysnetcz/ruian-service .

        # cd ..
        # cd ..
        # docker build -f ${PWD}/docker/services/Python.Dockerfile -t sysnetcz/ruian-rest .


## Ruční spuštění kontejneru

Pro produkční účely doporučujeme vytvořit komplentí implementaci služby pomocí **docker-compose**, avšak pro testovací a/nebo poloprovozní účel postačí ruční vytvoření kontejneru. Pozor přitom na vzájemnou viditelnost kontejnerů.

        # docker run -d --name ruian-service --network ruian-net -t sysnetcz/ruian-import

nebo

        # docker run -d --name ruian-rest --network ruian-net -t sysnetcz/ruian-rest

Předpokládá se, že kontejner **postgis** se nachází v síti **ruian-net**.
