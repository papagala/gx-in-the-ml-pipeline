#!/bin/bash

docker exec -t gx-in-the-ml-pipeline-notebook bash -c 'poetry run isort --profile=black /notebooks && poetry run black /notebooks'