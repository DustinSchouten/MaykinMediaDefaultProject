==================
maykinmedia
==================

:Version: 0.1.0
:Source: https://bitbucket.org/maykinmedia/maykinmedia
:Keywords: ``<keywords>``
:PythonVersion: 3.11

|build-status| |requirements|

Django webapp for collecting, storing and showing hotels and cities

Developed by `Maykin B.V.`_ for ``<client>``


Introduction
============

This Hotel app is a builded proof-of-concept for the case "Integrating third parties". It is a webapp written in Django where the user can view hotels and also filter on hotels by a specific city.


Documentation
=============

See ``INSTALL.rst`` for installation instructions, available settings and
commands.

.. image:: https://github.com/user-attachments/assets/5c2e912c-c56e-454b-85e0-98681f7a2d81
All hotels on page

.. image:: https://github.com/user-attachments/assets/e8a639ee-869a-4ca0-88b6-06df00a36605
Filtered on city


Run the project
***************
To run a Django project from this repository, you will need to follow a series of steps to make it work. Follow the steps below:


#. Clone the repository by running ``git clone https://github.com/DustinSchouten/MaykinMedia.git`` in a new folder on your local machine and navigate to that project folder.
#. Set up a virtual environment.
#. Install the project dependencies by running ``pip install -r requirements.txt``.
#. Create a .env file on the same level as the folders ``HotelApp``, ``MaykinMedia`` and ``manage.py``. Put all environment variables in it. These are:

- ``URL_CITY``
- ``URL_HOTEL``
- ``URL_USERNAME``
- ``URL_PASSWORD``
- ``DB_USER``
- ``DB_PASSWORD``
- ``DB_HOST``
- ``DB_PORT``
- ``DB_NAME``
- ``DJANGO_SECRET_KEY``
#. Apply the database migrations by running ``python manage.py makemigrations`` and then ``python manage.py migrate``.
#. (optional) To use the Django admin panel, create a superuseraccount by running ``python manage.py createsuperuser``.
#. Run the Django development server locally by running ``python manage.py runserver``. The webapp can be visited at ``http://127.0.0.1:8000/``.

Data
####
The data is retrieved from an authenticated HTTP server where two CSV-files are located. One of the files contains cities (PK and name) and the other contains hotels (PK, FK to city and name). See the simple datamodel below:

.. image:: https://github.com/user-attachments/assets/4233186f-0567-4fc3-b61a-f063308856fb

In this Django project, these tables are represented as models and the data is stored in a MySQL database.

Custom management command
#########################
In the app-folder in management/commands, a custom management command named ``load_csv_data_into_db`` is created for collecting the data and writing it into the database. This command can be called by running ``python manage.py load_csv_data_into_db``.

View and templates
##################
The Django project contains one class-based view named ``"Index"`` with a ``get()`` and a ``post()`` method. The ``get()`` method is called when the user visits the page and the ``post()`` method is called when the user clicks on the Search-button.

There are two HTML-templates used in this project:

base.html
"""""""""
This file contains basic HTML-content like the ``<header>`` tag and the ``<body>`` tag with a ``<h1>`` tag but without the actual content. This is done so that new pages can easily be added by reusing this template.

index.html
""""""""""
This file contains all HTML-content for showing the city input filter and the results section.

Tests
#####
In this project, all of the unit tests are added in ``tests.py``. These tests can be easily run with the command ``python manage.py test HotelApp`` in the terminal.

References
==========

* `Issues <https://taiga.maykinmedia.nl/project/maykinmedia>`_
* `Code <https://bitbucket.org/maykinmedia/maykinmedia>`_


.. |build-status| image:: http://jenkins.maykin.nl/buildStatus/icon?job=bitbucket/maykinmedia/master
    :alt: Build status
    :target: http://jenkins.maykin.nl/job/maykinmedia

.. |requirements| image:: https://requires.io/bitbucket/maykinmedia/maykinmedia/requirements.svg?branch=master
     :target: https://requires.io/bitbucket/maykinmedia/maykinmedia/requirements/?branch=master
     :alt: Requirements status


.. _Maykin B.V.: https://www.maykinmedia.nl
