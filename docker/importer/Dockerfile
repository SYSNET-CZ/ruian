# Docker obraz pro aplikaci importu VFR dat z RUIAN a ulozeni do PostGIS gatabaze.
#
# Postavit z rootu projektu pomoci prikazu: docker build -f ${PWD}/docker/importer/Aoache.Dockerfile -t sysnetcz/ruian-import .
#
# Do externiho volume:
#       -   /opt/ruian/toolbox/sharedtools/DownloadedData
#       -   /opt/ruian/toolbox/DownloadRUIAN.cfg
#       -   /opt/ruian/toolbox/ImportRUIAN.cfg
#       -   /opt/ruian/toolbox/RUIANServices.cfg
# 
# Spustit napriklad:
#       docker run -d --name ruian-import --network ruian-net -v vfr-data:/opt/ruian/toolbox/sharedtools/DownloadedData -t sysnetcz/ruian-import
#

FROM sysnetcz/ruian-base:latest
LABEL maintainer="SYSNET s.r.o. <info@sysnet.cz>"
LABEL version="1.0.0"

ENV RUIAN_TOOLBOX_HOME /opt/ruian/toolbox/downloader
ENV RUIAN_DOWNLOAD_HOME /opt/ruian/toolbox/downloader
ENV RUIAN_IMPORT_HOME /opt/ruian/toolbox/importer
ENV RUIAN_DATA_DIR /opt/ruian/sharedtools/DownloadedData
ENV RUIAN_LOG=${RUIAN_DATA_DIR}/logs
ENV RUIAN_VFR_FILES=${RUIAN_DATA_DIR}/data

RUN apt-get update && apt-get install -y cron bash wget

COPY ${PWD}/ruian-toolbox ./toolbox
ENV PATH="/opt/ruian/vfr:/opt/ruian/toolbox:${PATH}"

RUN mkdir -p ${RUIAN_LOG}
RUN mkdir -p ${RUIAN_VFR_FILES}
COPY ${PWD}/docker/importer/ruian-download /etc/cron.d/ruian-download
RUN chmod 0644 /etc/cron.d/ruian-download
RUN crontab /etc/cron.d/ruian-download
RUN touch ${RUIAN_LOG}/cron.log

# Run the command on container startup
CMD cron && tail -f ${RUIAN_LOG}/cron.log
