# PostGIS

V případě ruční instalace je nutné nainstalovat geografickou databázi postgis tak, aby s ní mohly ostatní kontejnery pracovat.
Používá se standardní obraz **sysnetcz/postgis**.

        # docker volume create postgis_data

        # sudo docker run -d \
            --name postgis \
            -p 5432:5432 \
            -v postgres_data:/var/lib/postgresql \
            --network ruian-net \
            -e POSTGRES_DBNAME=ruian \
            -e POSTGRES_MULTIPLE_EXTENSIONS=postgis,hstore,postgis_topology,fuzzystrmatch \
            -e POSTGRES_USER=docker \
            -e POSTGRES_PASS=docker \
            -e ALLOW_IP_RANGE=<0.0.0.0> \
            --restart unless-stopped \
            -t sysnetcz/postgis:manual-build

... a je to :-)
