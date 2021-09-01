# FROM python:3.6-alpine
FROM python:3-bullseye

ARG WORK_DIR=/opt/ruian
RUN mkdir -p ${WORK_DIR}
WORKDIR ${WORK_DIR}

COPY requirements.txt ${WORK_DIR}

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install connexion[swagger-ui]

ENV POSTGIS_HOST=postgis
ENV POSTGIS_PORT=5432
ENV RUIAN_DATABASE=ruian
ENV POVODI_DATABASE=gis
ENV MAPY_DATABASE=gis
ENV POSTGIS_USER=docker
ENV POSTGIS_PASSWORD=docker
ENV SERVICE_ENVIRONMENT=production

COPY . ${WORK_DIR}

EXPOSE 8080

# ENTRYPOINT ["python3"]
# CMD ["-m", "swagger_server"]
CMD ["gunicorn", "app:app", "-w", "4", "-b", "0.0.0.0:8080"]
