LIGO
===============

|Cookiecutter| |nbsp| |License|

Ligo an open source application that provides an easy-to-use web interface that lets analysts
select among a number of data linking methods and use these in a documented, repeatable, tested,
step-by-step process to deduplicate and match administrative records.

Ligo's framework for managing data linking projects is extensible to allow for the addition of new
methodologies and algorithms in the completion of administrative data linking projects.

Built in Python and implemented as a desktop-capable and cloud-deployable containerized application,
Ligo includes many of the latest data-linking comparison algorithms with a plugin architecture that
supports the simple addition of new formulae and methods.

Currently, deterministic approaches to linking have been implemented and probabilistic methods are
in alpha testing. The high-level application road-map anticipates the inclusion of machine learning
extensions in future releases.



**LIGO** will help you:

* Identity common entities in a CSV formatted dataset [de-duplication]
* Identify common entities between two CSV formatted datasets [linking]


Features
--------

* Support for deterministic linking with probabilistic linking underway
* Support for multi-step projects
    * Each step allows you to define a specific blocking (filtering the search space) and linking criteria
    * For de-duplication, you can choose the step(s) where entities are identified (i.e., you can join multiple de-duplication steps)
    * You can have multiple records representing the same entity; the software links entities (not records). At each step, only not-linked entities are evaluated.
* Comparison rules such as SoundEx, Levenshtein and Jaro-Winkler allow you to tailor matching criteria for individual fields
* Designed for handling large datasets
* Results in CSV and PDF for easy processing / viewing
* Can run in both offline workstations and cloud environments
* Supports running concurrent sessions on cloud infrastructure.

Documentation
-------------
A very basic user manual has been started. Feel free to contribute to it here //docs/ 



Errors / Bugs
-------------

If something is not behaving intuitively, it is likely a bug, and `should be reported <https://github.com/bcgov/LIGO/issues>`_


Dependencies
------------

Since we depend on the data-linking library, we must acquire a copy of the ligo-lib repository and store it in  the application root under data-linking. Run the following in the application root:

.. code:: sh

    git checkout git@github.com:bcgov/ligo-lib.git


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

Ligo expects data files and resources in certain pre-defined locations. Run the following command in the application root:

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
linkage-worker Variables  Description
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


You can use the env.example files as a template for creating your environment variable files.


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

* To create an **superuser account**, (that allows for the management of users) use this command:

.. code:: python

    python manage.py createsuperuser




Database Migration
~~~~~~~~~~~~~~~~~~

Ligo  uses PostgreSQL  for managing datasets and linking projects. To migrate the database, on the application root directory run:

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
.. |License| image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
    :target: http://www.apache.org/licenses/LICENSE-2.0
    :alt: License: Apache 2.0
.. |nbsp| unicode:: 0xA0
