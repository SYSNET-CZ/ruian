# NGINX

V případě ruční instalace je vhodné samostaně nainstalovat reverzní proxy, aby bylo možno uzavřít přístup k ostatním kontejnerům.
Reverzní proxy zpřístupní pouze ty služby, které jsou určeny pro přístup zvenčí.

        # mkdir -p data/conf/sites
        # mkdir -p data/conf/ssl
        # mkdir -p data/html
        # mkdir -p data/logs
        # cp ../contrib/conf/nginx/nginx.conf data/conf/nginx.conf
        # cp ../contrib/conf/nginx/.htpasswd data/conf/.htpasswd
        # cp -R ../contrib/conf/nginx/sites data/conf/sites
        # cp -R ../contrib/conf/nginx/ssl data/conf/ssl
        # cp -R ../contrib/conf/nginx/html data/html
   
        # docker run -d \
            --name nginx \
            -p 80:80 -p 443:443 \
            -v ${PWD}/data/conf/nginx.conf:/etc/nginx/nginx.conf \
            -v ${PWD}/data/conf/.htpasswd:/etc/nginx/.htpasswd \
            -v ${PWD}/data/conf/sites:/etc/nginx/sites \
            -v ${PWD}/data/conf/ssl:/etc/nginx/ssl \
            -v ${PWD}/data/html:/usr/share/nginx/html:ro \
            -v ${PWD}/data/logs:/var/log/nginx \
            --network ruian-net \
            --restart unless-stopped \
            -t nginx

... a je to :-)
