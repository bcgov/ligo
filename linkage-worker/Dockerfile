FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Docker file for forming local/dev Django container
RUN mkdir -p /user_data/media/datasets /user_data/media/linking
RUN mkdir /tmp/django-email-dev
# Ownership change not a requirement for local/dev docker environments
RUN chmod -R 0777 /user_data

# Install Celery Requirements
COPY ./linkage-worker/link-server /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

# Install Data Linking Requirements
COPY ./data-linking/requirements /usr/src/app/lib/requirements
RUN pip install -r /usr/src/app/lib/requirements/base.txt

# Install Data Linking Packages
COPY ./data-linking /usr/src/app/lib
RUN pip install -e /usr/src/app/lib/cdi-linking/
RUN pip install -e /usr/src/app/lib/linking_ext/

RUN echo 'django:x:999:999:django:/:/bin/sh' >> /etc/passwd

RUN chown 999:999 -R /usr/src/app
RUN chown 999:999 -R /user_data
RUN chown 999:999 -R /tmp

USER "999:999"
WORKDIR /usr/src/app

ENTRYPOINT celery -A tasks worker --loglevel=info
