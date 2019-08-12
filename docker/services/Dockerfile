# Docker obraz pro aplikaci webových sluzeb nad geodatabazi RUIAN ulozenou v postgis.
#
# Postavit pomoci prikazu: 
#       docker build -t sysnetcz/ruian-service .
#
# Do externiho volume:
#       -   /opt/ruian/toolbox/sharedtools/DownloadedData
#       -   /opt/ruian/toolbox/DownloadRUIAN.cfg
#       -   /opt/ruian/toolbox/ImportRUIAN.cfg
#       -   /opt/ruian/toolbox/RUIANServices.cfg
# 
# Spustit napriklad:
#       docker run -d --name ruian-service - 8080:80 --network ruian-net -v vfr-data:/opt/ruian/toolbox/sharedtools/DownloadedData:ro -t sysnetcz/ruian-service
#

FROM sysnetcz/ruian-base:latest
MAINTAINER SYSNET s.r.o. "info@sysnet.cz"

ENV RUIAN_TOOLBOX_HOME /opt/ruian/toolbox/downloader
ENV RUIAN_DOWNLOAD_HOME /opt/ruian/toolbox/downloader
ENV RUIAN_IMPORT_HOME /opt/ruian/toolbox/importer
ENV RUIAN_DATA_DIR /opt/ruian/sharedtools/DownloadedData
ENV RUIAN_LOG=${RUIAN_DATA_DIR}/logs
ENV RUIAN_VFR_FILES=${RUIAN_DATA_DIR}/data

EXPOSE 80

RUN apt-get update && apt-get install -y apache2 bash wget
RUN a2enmod cgi


COPY ../../ruian-toolbox ./toolbox
ENV PATH="/opt/ruian/vfr:/opt/ruian/toolbox:${PATH}"

RUN mkdir -p ${RUIAN_LOG}
RUN mkdir -p ${RUIAN_VFR_FILES}
COPY ruian-download /etc/cron.d/ruian-download
RUN chmod 0644 /etc/cron.d/ruian-download
RUN crontab /etc/cron.d/ruian-download
RUN touch ${RUIAN_LOG}/cron.log



# Run the command on container startup
CMD cron && tail -f ${RUIAN_LOG}/cron.log
