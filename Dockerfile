#FROM ubuntu:bionic
#FROM debian:stable
FROM python:3

MAINTAINER SYSNET s.r.o. "info@sysnet.cz"

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN localedef -i cs_CZ -c -f UTF-8 -A /usr/share/locale/locale.alias cs_CZ.UTF-8
RUN sed -i -e 's/# cs_CZ.UTF-8 UTF-8/cs_CZ.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG cs_CZ.UTF-8  
ENV LANGUAGE cs_CZ:cs  
ENV LC_ALL cs_CZ.UTF-8   
ENV LC_CTYPE="cs_CZ.UTF-8"
ENV LC_NUMERIC="cs_CZ.UTF-8"
ENV LC_TIME="cs_CZ.UTF-8"
ENV LC_COLLATE="cs_CZ.UTF-8"
ENV LC_MONETARY="cs_CZ.UTF-8"
ENV LC_MESSAGES="cs_CZ.UTF-8"
ENV LC_PAPER="cs_CZ.UTF-8"
ENV LC_NAME="cs_CZ.UTF-8"
ENV LC_ADDRESS="cs_CZ.UTF-8"
ENV LC_TELEPHONE="cs_CZ.UTF-8"
ENV LC_MEASUREMENT="cs_CZ.UTF-8"
ENV LC_IDENTIFICATION="cs_CZ.UTF-8"

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y -qq \
    # std libs
    unzip wget sudo less nano curl git gosu build-essential software-properties-common \
    # python basic libs
    python3 python3-dev gettext \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install pip
# RUN wget https://bootstrap.pypa.io/get-pip.py && python3.7 get-pip.py && rm get-pip.py
# RUN pip3 install --no-cache-dir setuptools wheel -U


WORKDIR /opt/ruian
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
#COPY . .
#CMD [ "python", "./your-daemon-or-script.py" ]

CMD ["/bin/bash"]
