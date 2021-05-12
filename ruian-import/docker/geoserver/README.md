# geoserver

	docker volume create geoserver_data
	docker run -d --name geoserver \
          --network ruian-net \
	  -e "GEOSERVER_ADMIN_PASSWORD=changeme" \
	  -p 8080:8080 \
	  --link postgis:postgis \
	  -v geoserver_data:/opt/geoserver/data_dir \
	  -t kartoza/geoserver


docker run -d --name geoserver \
  --network ruian-net \
  -e "GEOSERVER_ADMIN_PASSWORD=Egalite1651." \
  -p 8080:8080 \
  --link postgis:postgis \
  -t kartoza/geoserver

