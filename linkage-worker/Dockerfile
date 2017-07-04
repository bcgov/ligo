FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY ./linkage-worker/link-server /linkage-worker

RUN mkdir /linkage-worker/lib
COPY ./data-linking/  /linkage-worker/lib

RUN pip install -e /linkage-worker/lib/cdi-linking/
RUN pip install -e /linkage-worker/lib/linking_ext/

RUN mkdir /user_data
RUN mkdir /user_data/media
RUN mkdir  /user_data/media/datasets
RUN mkdir  /user_data/media/linking


#the following change in ownership instructions are not absolutely essential for docker based local/dev env

RUN chmod -R 0777 /user_data
RUN echo 'django:x:999:999:django:/:/bin/sh' >> /etc/passwd

RUN chown  999:999 -R /linkage-worker
RUN chown  999:999 -R /user_data

RUN mkdir /tmp/django-email-dev
RUN chown  999:999 -R /tmp

WORKDIR /linkage-worker
RUN pip install -r requirements.txt

USER "999:999"
# Install celery requirements

ENTRYPOINT celery -A tasks worker --loglevel=info