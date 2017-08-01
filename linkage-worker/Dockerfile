FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Docker file for forming local/dev Django container
RUN mkdir -p /user_data/media/datasets /user_data/media/linking
RUN mkdir /tmp/django-email-dev
# Ownership change not a requirement for local/dev docker environments
RUN chmod -R 0777 /user_data

# Install Celery Requirements
COPY ./linkage-worker/link-server /linkage-worker
RUN pip install -r /linkage-worker/requirements.txt

# Install Data Linking Requirements
COPY ./data-linking/requirements /linkage-worker/lib/requirements
RUN pip install -r /linkage-worker/lib/requirements/base.txt

# Install Data Linking Packages
COPY ./data-linking /linkage-worker/lib
RUN pip install -e /linkage-worker/lib/cdi-linking/
RUN pip install -e /linkage-worker/lib/linking_ext/

RUN echo 'django:x:999:999:django:/:/bin/sh' >> /etc/passwd

RUN chown 999:999 -R /linkage-worker
RUN chown 999:999 -R /user_data
RUN chown 999:999 -R /tmp

USER "999:999"
WORKDIR /linkage-worker

ENTRYPOINT ["celery", "-A", "tasks", "worker", "--loglevel=info"]
