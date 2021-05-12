# Portainer

Pokud se chcete vyznat ve svých kontejnerech a platformě Docker, používejte skvělý opensource nástroj [portainer.io](https://www.portainer.io/). Pokud ho nezačleníze do svého systému, dá se nainstalovat ručne na hostitelský stroj platformy Docker:

        # docker volume create portainer_data

        # sudo docker run -d \
            --name portainer \
            -p 8000:8000 -p 9000:9000 \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v portainer_data:/data \
            --network ruian-net \
            --restart always \
            -t portainer/portainer

... a je to :-)
