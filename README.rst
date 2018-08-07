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



Build
-----

.. image:: https://travis-ci.org/NovaVic/ligo.svg?branch=master
    :target: https://travis-ci.org/NovaVic/ligo



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


Installation
------------
Warning: Despite the use of Django accounts to support multi-user linking project
management, Ligo is not designed to provide any security to prevent access to data or controls. 
The application should only be used within an access controlled desktop environment or behind a 
web firewall that limits access to trusted parties. Do NOT rely on user accounts to protect data.

The application has been containerized to support repeatablity in development processes and 
deployment - a refactoring to support leveraging scaling within a Kubernetes cluster is in the roadmap.



The following installation instructions/steps are for cases when users are pulling docker images from 
dockerhub instead of building any images from source code.

* Install docker-compose - https://docs.docker.com/compose/install/
* Create a subdirectory named ligo_app. 
* In this subdirectory create a subdirectory named files and within files directory create a subdirectory with the name 'media'.
* Ligo expects data files and resources in certain pre-defined locations. Under the ligo_app/files/media/ subdirectory, create a subdirectory named 'linking' and another subdirectory named 'datasets'. Basically run the following command in the application root (ligo_app folder):

.. code:: sh

    mkdir -p files/media/datasets files/media/linking

* Put the files that you want to de-duplicate or link in the ligo_app/files/media/datasets subdirectory.
* Add read and write permission for everyone to the ligo_app/files/ directory and corresponding subdirectories with an instruction like

.. code:: sh

    chmod -R 777 ligo_app/files

* Use a browser to download this docker-compose.yml and save the file into the directory ligo_app.
* To run the application, change to the ligo_app directory where you put the docker-compose.yml file and type the following command (and press enter):

.. code:: sh

    docker-compose up 

* You will see some text scroll by in the window as the application starts up. Once it has finished scrolling open a web browser like Edge/Firefox/Chrome and in the address bar type http://localhost:8002 and hit enter.

* Select "sign in" from top right-hand-side and login with username:baseuser password:Pass12345678 


If you are able to log in then you successfully installed the software on your system. Enjoy de-duplication and linking!




If you are not contributing to the source code of Ligo then you can easily ignore all the following sections.


Environment Variables (Only for developers modifying source code)
-----------------------------------------------------------------

The following environment variables are required for project settings:

=================  ==============================================
web-app Variables  Description
=================  ==============================================
IN_DOCKER          1 if Dockerized, 0 otherwise
C_FORCE_ROOT       Boolean - forces workspace from root directory
CELERY_BROKER_URL  Example: redis://localhost:6379/0
=================  ==============================================


========================  ===========================================================
worker Variables  Description
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
------
To recreate the docker containers use the following command (due to the content of the docker-compose file the 
--build option in the following command has no effect):

.. code:: sh

    docker-compose up --build --force-recreate  


Should everything be properly configured, you can visit http://localhost:8002




.. |Cookiecutter| image:: https://img.shields.io/badge/Built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django
     :alt: Built with Cookiecutter Django
.. |License| image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
    :target: http://www.apache.org/licenses/LICENSE-2.0
    :alt: License: Apache 2.0
.. |nbsp| unicode:: 0xA0
