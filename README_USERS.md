 task-updater
=============

Clone the project and move inside:
```shell
git clone https://github.com/pyprogrammerblog/task-updater.git
cd task-updater
```
 
Install the virtualenv on the root project folder:
```shell
docker-compose run --rm --no-deps updater poetry install
```

Check your installed dependencies for security vulnerabilities
```shell
docker-compose run --rm updater poetry check
```

Run the tests:
```shell
docker-compose run --rm updater poetry run pytest
```

Shut down all services
```shell
docker-compose down
```


### Jupyter Notebook

Hit the command

```shell
docker-compose run --rm -p 8888:8888 updater poetry shell
```

Then inside the docker:

```shell
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

That is all!

Hupdatery Coding!
