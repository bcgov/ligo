FROM python:3.6

ENV PYTHONUNBUFFERED 1
RUN pwd

COPY ./linkage-worker/link-server /linkage-worker

RUN mkdir /linkage-worker/lib
COPY ./data-linking/  /linkage-worker/lib

RUN pip install -e /linkage-worker/lib/cdi-linking/
RUN pip install -e /linkage-worker/lib/linking_ext/


RUN mkdir /user_data
RUN mkdir /user_data/media
RUN mkdir  /user_data/media/datasets
RUN mkdir  /user_data/media/linking

WORKDIR /linkage-worker

# Install celery requirements
RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info

