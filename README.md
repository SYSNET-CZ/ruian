# RUIAN Service



    docker build -t sysnetcz/ruian-base .

    docker run -it --name ruian -t sysnetcz/ruian-base /bin/bash


## GDAL-VFR

Full VFR (Vymenny format RUIAN) support in GDAL library.

### References (in Czech)

http://freegis.fsv.cvut.cz/gwiki/RUIAN_/_GDAL#VFR_konverzn.C3.AD_skripty

docker network create -d bridge ruian-net

docker volume create postgis_data
docker volume create postgis_backup
docker volume create postgis_logs
docker run -d --name "postgis" \
  -p 5432:5432 \
  -e POSTGRES_USER=docker \
  -e POSTGRES_PASS=docker \
  -e POSTGRES_DBNAME=ruian \
  -e "POSTGRES_MULTIPLE_EXTENSIONS=postgis,hstore,postgis_topology" \
  -e "ALLOW_IP_RANGE=0.0.0.0/0" \
  -e "IP_LIST=*" \
  -e "LANG=cs_CZ.UTF-8" \
  -e "LC_COLLATE=cs_CZ.UTF-8" \
  -e "LC_ALL=cs_CZ.UTF-8" \
  --network ruian-net \
  -v postgis_data:/var/lib/postgresql \
  -v postgis_backup:/backups \
  -v postgis_logs:/var/log \
  -t sysnetcz/postgis:manual-build



docker volume create portainer_data
docker run -d --name portainer \
  -p 8000:8000 -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  --network ruian \
  portainer/portainer
