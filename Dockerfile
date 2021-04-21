FROM ubuntu:focal
LABEL maintainer="SYSNET s.r.o.<info@sysnet.cz>"

# http://freegis.fsv.cvut.cz/gwiki/RUIAN_/_GDAL

ARG HOME_DIR=/opt/ruian
ARG ENCODING=UTF-8
ARG LANGUAGE_GROUP=cs
ARG LANGUAGE=${LANGUAGE_GROUP}_CZ
ARG LOCALE=${LANGUAGE}.${ENCODING}

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
RUN apt-get clean \
    && apt-get update \
    && apt-get install -qq apt-utils \
    && apt-get install -qq tzdata \
    && apt-get install -qq locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen "${LOCALE}" \
    && update-locale LANG=${LOCALE}

ENV LANG=${LOCALE} \
    LANGUAGE=${LANGUAGE}:${LANGUAGE_GROUP} \
    LC_ALL=${LOCALE} \
    TZ=Europe/Prague \
    PYTHONUNBUFFERED=1 \
    CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get update \
    && apt-get install -qq iputils-ping \
    && apt-get install -qq python3 python3-dev python3-pip \
    && apt-get install -qq python-is-python3 \
    && apt-mark hold \
    python2 python2-minimal \
    python2.7 python2.7-minimal \
    libpython2-stdlib libpython2.7-minimal libpython2.7-stdlib

RUN apt-get install -qq gettext \
    && apt-get install -qq software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa && apt-get update \
    && add-apt-repository ppa:ubuntugis/ppa && apt-get update

RUN apt-get install -qq gdal-bin binutils libproj-dev \
    && apt-get install -qq libgdal-dev \
    && apt-get install -qq libpq-dev postgresql-client python3-psycopg2 \
    && apt-get install -qq python3-numpy \
    && apt-get install -qq python3-gdal

WORKDIR ${HOME_DIR}
COPY ./gdal-vfr ./vfr
COPY ./ruian-toolbox ./toolbox
COPY ./config ./config

ENV PATH="/opt/ruian/vfr:/opt/ruian/toolbox:${PATH}" \
    CUZK_VYMENNYFORMAT=https://vdp.cuzk.cz/vdp/ruian/vymennyformat \
    RUIAN_CONFIG_DIRECTORY=${HOME_DIR}/config \
    RUIAN_DATA_DIRECTORY=${HOME_DIR}/data \
    RUIAN_DOWNLOAD_DIRECTORY=${HOME_DIR}/data \
    RUIAN_CONFIG_FILE_DOWNLOAD=DownloadRUIAN.cfg \
    RUIAN_CONFIG_FILE_IMPORT=ImportRUIAN.cfg \
    OS4GEO_PATH=${HOME_DIR}/vfr \
    RUIAN_DB_NAME=ruian \
    RUIAN_DB_SCHEMA=public \
    RUIAN_DB_HOST=postgis \
    RUIAN_DB_PORT=5432 \
    RUIAN_DB_USER=docker \
    RUIAN_DB_PASSWORD=docker \
    RUIAN_SERVICE_TABLES=True \
    RUIAN_AUTOCOMPLETE_TABLES=True

RUN pip3 install -r ./toolbox/requirements.txt

RUN chmod 755 ${HOME_DIR}/toolbox/download.sh
RUN chmod 755 ${HOME_DIR}/toolbox/import.sh
RUN chmod 755 ${HOME_DIR}/toolbox/toolbox.sh

ADD crontab /etc/cron.d/ruian-cron
RUN chmod 0644 /etc/cron.d/ruian-cron
RUN touch /var/log/cron.log
RUN apt-get update && apt-get -y install cron
CMD ["cron", "-f"]