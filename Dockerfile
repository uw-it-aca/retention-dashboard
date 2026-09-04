ARG DJANGO_CONTAINER_VERSION=3.1.4

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} AS app-prewebpack-container

USER root

RUN apt-get update && apt-get install -y postgresql-client

USER acait

COPY --chown=acait:acait . /app/
COPY --chown=acait:acait docker/ /app/project/

RUN /app/bin/pip install -r requirements.txt

RUN . /app/bin/activate && python manage.py test

FROM node:8.15.1-jessie AS wpack
COPY . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack --mode=production

FROM app-prewebpack-container AS app-container

COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/retention_dashboard/bundles/* /app/retention_dashboard/static/retention_dashboard/bundles/
COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/ /static/
COPY --chown=acait:acait --from=wpack /app/retention_dashboard/static/webpack-stats.json /app/retention_dashboard/static/webpack-stats.json

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} AS app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
