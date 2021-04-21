# Zakladni GDAL-VFR Docker obraz pro dalsi pouziti. Vhodne pro import dat z RUIAN, sluzby nad importovanymi daty,
# GeoDjango aplikace a dalsi GIS aplikace.
#
# Postavit z rootu projektu pomoci prikazu: docker build -f ${PWD}/docker/base/Aoache.Dockerfile.p3.2 -t sysnetcz/ruian-base .
#

FROM ubuntu:bionic

# http://freegis.fsv.cvut.cz/gwiki/RUIAN_/_GDAL

LABEL maintainer="SYSNET s.r.o. <info@sysnet.cz>"
LABEL version="1.0.0"

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get clean && apt-get update && apt-get install -y apt-utils
RUN apt-get install -y locales
RUN localedef -i cs_CZ -c -f UTF-8 -A /usr/share/locale/locale.alias cs_CZ.UTF-8
RUN sed -i -e 's/# cs_CZ.UTF-8 UTF-8/cs_CZ.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG=cs_CZ.UTF-8 \
    LANGUAGE=cs_CZ:cs \
    LC_ALL=cs_CZ.UTF-8 \
    LC_CTYPE="cs_CZ.UTF-8" \
    LC_NUMERIC="cs_CZ.UTF-8" \
    LC_TIME="cs_CZ.UTF-8" \
    LC_COLLATE="cs_CZ.UTF-8" \
    LC_MONETARY="cs_CZ.UTF-8" \
    LC_MESSAGES="cs_CZ.UTF-8" \
    LC_PAPER="cs_CZ.UTF-8" \
    LC_NAME="cs_CZ.UTF-8" \
    LC_ADDRESS="cs_CZ.UTF-8" \
    LC_TELEPHONE="cs_CZ.UTF-8" \
    LC_MEASUREMENT="cs_CZ.UTF-8" \
    LC_IDENTIFICATION="cs_CZ.UTF-8"
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y python-pip python-dev gettext \
  && cd /usr/local/bin \
  && pip install --upgrade pip

RUN apt-get install -y software-properties-common 
RUN add-apt-repository ppa:ubuntugis/ppa && apt-get update
RUN apt-get install -y gdal-bin binutils libproj-dev 
RUN apt-get install -y libgdal-dev
RUN apt-get install -y libpq-dev postgresql-client python-psycopg2

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get install -y python-numpy && apt-get install -y python-gdal

WORKDIR /opt/ruian
COPY gdal-vfr ./vfr
#COPY ruian-toolbox ./toolbox
#ENV PATH="/opt/ruian/vfr:/opt/ruian/toolbox:${PATH}"
ENV PATH="/opt/ruian/vfr:${PATH}"

CMD ["/bin/bash"]
