Data Linking UI
===============

|Cookiecutter| |nbsp| |License|

A web application for linking multiple datasets.


Dependencies
------------

Since we depend on the data-linking library, we must acquire a copy of the data-linking repository and store it in  the application root under data-linking. Run the following in the application root:

.. code:: sh

    git checkout git@github.com:bcgov-c/data-linking.git


Then use the following commands in the application root directory to install the remaining python library requirements:

.. code:: sh

    pip install -r /requirements/local.txt


For production environment use:

.. code:: sh

    pip install -r /requirements/production.txt


Installation
------------

Folder Structure
~~~~~~~~~~~~~~~~

The data-linking-ui expects data files and resources in certain pre-defined locations. Run the following command in the application root:

.. code:: sh

    mkdir -p files/media/datasets files/media/linking


Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The following environment variables are required for project settings:

=================  ==============================================
web-app Variables  Description
=================  ==============================================
IN_DOCKER          1 if Dockerized, 0 otherwise
C_FORCE_ROOT       Boolean - forces workspace from root directory
CELERY_BROKER_URL  Example: redis://localhost:6379/0
=================  ==============================================


========================  ===========================================================
linkage-worker Variables          Description
========================  ===========================================================
IN_DOCKER                 1 if Dockerized, 0 otherwise
C_FORCE_ROOT              Boolean - forces workspace from root directory
CELERY_BROKER_URL         Example: redis://localhost:6379/0
LINK_DB_NAME              Database Name
LINK_DB_USER              Database User
LINK_DB_HOST              Database Host
LINK_DB_PORT              Database Port (5432)
LINK_DB_SERVICE           Database Type (postgres)
LINK_DB_PASSWORD          Database Password
LOGGING_LEVEL             Valid Logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
APP_ROOT_URL              Defines Root URL - Can be left blank
STATIC_URL                Example: /static/
========================  ===========================================================


Docker
~~~~~~

Once everything above has been satisfied, you may build the docker containers with the following command:

.. code:: sh

    docker-compose up --build --force-recreate


Should everything be properly configured, you can visit http://localhost:8002


Configuration
--------------

Setting Up Your Users
~~~~~~~~~~~~~~~~~~~~~

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command:

.. code:: python

    python manage.py createsuperuser


For convenience, you could keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.


Database Migration
~~~~~~~~~~~~~~~~~~

The data-linking-ui web application uses postgresql linkage database for managing datasets and linking projects. To migrate the database, on the application root directory run:

.. code:: python

    python manage.py migrate


Celery
~~~~~~

The web application uses Celery to run linking jobs asynchronously. You need to setup a Celery broker like Redis or
RabbitMQ and start a Celery worker.

The Celery broker is provided by the CELERY_BROKER_URL environment variable. To start a Celery worker use:

.. code:: sh

    celery -A linkage worker --loglevel=INFO


.. |Cookiecutter| image:: https://img.shields.io/badge/Built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django
     :alt: Built with Cookiecutter Django
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT
.. |nbsp| unicode:: 0xA0
