# Docker obraz pro aplikaci webových sluzeb nad geodatabazi RUIAN ulozenou v postgis.
#
# Postavit z rootu projektu pomoci prikazu: docker build -f ${PWD}/docker/services/Dockerfile -t sysnetcz/ruian-service .
#
# Do externiho volume:
#       -   /opt/ruian/toolbox/shared_tools/DownloadedData
#       -   /opt/ruian/toolbox/DownloadRUIAN.cfg
#       -   /opt/ruian/toolbox/ImportRUIAN.cfg
#       -   /opt/ruian/toolbox/ruian_services.cfg
# 
# Spustit napriklad:
#       docker run -d --name ruian-service - 8080:80 --network ruian-net -v vfr-data:/opt/ruian/toolbox/shared_tools/DownloadedData:ro -t sysnetcz/ruian-service
#

FROM sysnetcz/ruian-base:latest
MAINTAINER SYSNET s.r.o. "info@sysnet.cz"

ENV RUIAN_TOOLBOX_HOME /opt/ruian/toolbox/downloader
ENV RUIAN_DOWNLOAD_HOME /opt/ruian/toolbox/downloader
ENV RUIAN_IMPORT_HOME /opt/ruian/toolbox/importer
ENV RUIAN_SERVICE_HOME /opt/ruian/toolbox/RUIANServices
ENV RUIAN_DATA_DIR /opt/ruian/sharedtools/DownloadedData
ENV RUIAN_LOG=${RUIAN_DATA_DIR}/logs
ENV RUIAN_VFR_FILES=${RUIAN_DATA_DIR}/data

EXPOSE 80

RUN apt-get update && apt-get install -y apache2 bash wget
RUN a2enmod cgi

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

COPY ${PWD}/ruian-toolbox ./toolbox
ENV PATH="/opt/ruian/vfr:/opt/ruian/toolbox:${PATH}"

RUN mkdir -p ${RUIAN_LOG}
RUN mkdir -p ${RUIAN_VFR_FILES}

COPY ${PWD}/docker/services/apache2.conf /etc/apache2/apache2.conf
COPY ${PWD}/docker/services/apache-config.conf /etc/apache2/sites-enabled/000-default.conf

# Run the command on container startup
CMD /usr/sbin/apache2ctl -D FOREGROUND
