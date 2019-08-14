# RUIAN Base

Zakladni obraz pro GIS aplikace. Obsahuje kompletní podproru GDAL a VFR (Výměnný format RUIAN). Viz [dokumentace](http://freegis.fsv.cvut.cz/gwiki/RUIAN_/_GDAL#VFR_konverzn.C3.AD_skripty).

## Vytvoření obrazu

Obraz se vytvoří příkazem

        $ docker build -t sysnetcz/ruian-base .

## Ruční spuštění kontejneru

Tento obraz se nehodí pro prodikční účely. Pokud jej chcete použí pro testování vytvořte relevantní kontejnery ručně. Pozor přitom na vzájemnou viditelnost kontejnerů. 

        docker run -it --name ruian-base --network ruian-net -t sysnetcz/ruian-base /bin/bash

Předpokládá se, že kontejner **postgis** se nachází v síti **ruian-net**. 

## Portainer

Pokud se chcete vyznat ve svých kontejnerech a platformě Docker, používejte skvělý opensource nástroj **portainer.io**. Pokud ho nezačleníze do svého systému, dá se nainstalovat ručne na hostitelský stroj platformy Docker:

        $ docker volume create portainer_data

        $ sudo docker run -d \
            --name portainer \
            -p 8000:8000 -p 9000:9000 \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v portainer_data:/data \
            --network ruian-net \
            --restart always \
            -t portainer/portainer

... a je to :-) 


