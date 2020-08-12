=================
DataBroker Server
=================

.. image:: https://img.shields.io/travis/bluesky/databroker-server.svg
        :target: https://travis-ci.org/bluesky/databroker-server

.. image:: https://img.shields.io/pypi/v/databroker-server.svg
        :target: https://pypi.python.org/pypi/databroker-server


HTTP server exposing the DataBroker API in a language agnostic way.

* Open source software: 3-clause BSD license
* Documentation: (COMING SOON!) https://bluesky.github.io/databroker-server.

To get up and running just clone the repository, install the requirements and
start the server::

    $ pip install -r requirements.txt
    $ uvicorn --port 6942 databroker_server.main:app --reload

Right now there is no default web interface, the RESTful API can be explored
using the generated documentation at http://localhost:6942/docs with a Python
file for each endpoint in the routers directory and integration with databroker
in the model directory.

Features
--------

* TODO
