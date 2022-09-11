.. _installation:


Installation
=============

Install progress-updater::

    pip install progress-updater


Advanced: local setup for development (Ubuntu)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These instructions assume that ``git``, ``docker``, and ``docker-compose`` are
installed on your host machine.

First, clone this repo and make some required directories.::

    git clone https://github.com/pyprogrammerblog/progress-updater.git
    cd progress-updater

Then build the docker image::

    docker-compose run --rm app poetry install

Then install dependencies::

    docker-compose run --rm app poetry install

Run the tests::

    docker-compose run app poetry run pytest

Then run the app and access inside the docker with the env activated::

    docker-compose run --rm app poetry shell

Finally you can down the services::

    docker-compose down

Advanced: Jupyter Notebook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hit the command::

    docker-compose run --rm -p 8888:8888 app poetry shell

Then inside the docker::

    jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
