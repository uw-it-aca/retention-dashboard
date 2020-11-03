FROM acait/django-container:1.1.17 as app-container

USER root
RUN apt-get update
RUN apt-get install -y libpq-dev postgresql-client
USER acait

ADD --chown=acait:acait retention_dashboard/VERSION /app/retention_dashboard/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/

RUN . /app/bin/activate && pip install -r requirements.txt
RUN . /app/bin/activate && pip install psycopg2
RUN . /app/bin/activate && pip install django-webpack-loader

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack --mode=production

FROM app-container

COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/retention_dashboard/bundles/* /app/retention_dashboard/static/retention_dashboard/bundles/
COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/ /static/
COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/webpack-stats.json /app/retention_dashboard/static/webpack-stats.json
