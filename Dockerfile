ARG DJANGO_CONTAINER_VERSION=2.0.3

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} as app-prewebpack-container

USER root

RUN apt-get update && apt-get install -y libpq-dev postgresql-client

USER acait

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ /app/project/

RUN /app/bin/pip install -r requirements.txt
RUN /app/bin/pip install psycopg2

RUN . /app/bin/activate && python manage.py test

FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack --mode=production

FROM app-prewebpack-container as app-container

COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/retention_dashboard/bundles/* /app/retention_dashboard/static/retention_dashboard/bundles/
COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/ /static/
COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/webpack-stats.json /app/retention_dashboard/static/webpack-stats.json

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} as app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
