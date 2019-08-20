# Docker obraz pro aplikaci webových sluzeb nad geodatabazi RUIAN ulozenou v postgis.
#
# Postavit pomoci prikazu: 
#       docker build -t sysnetcz/ruian-rest .
#
# Do externiho volume:
#       -   /opt/ruian/toolbox/sharedtools/DownloadedData
#       -   /opt/ruian/toolbox/DownloadRUIAN.cfg
#       -   /opt/ruian/toolbox/ImportRUIAN.cfg
#       -   /opt/ruian/toolbox/RUIANServices.cfg
# 
# Spustit napriklad:
#       docker run -d --name ruian-rest - 8080:5689 --network ruian-net -v vfr-data:/opt/ruian/toolbox/sharedtools/DownloadedData:ro -t sysnetcz/ruian-rest
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
EXPOSE 5689

COPY ../../ruian-toolbox ./toolbox
ENV PATH="/opt/ruian/vfr:/opt/ruian/toolbox:${PATH}"

RUN mkdir -p ${RUIAN_LOG}
RUN mkdir -p ${RUIAN_VFR_FILES}
RUN pip install lpthw.web

CMD ["python", "/opt/ruian/toolbox/RUIANServices/services/rest.py"]
