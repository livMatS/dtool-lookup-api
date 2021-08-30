#!/bin/bash
#
# This snippet is meant for running tests quickly locally and may be outdated.
# The proper testing workflow resides within .github/workflows/ttest.yml
#
# Make https://github.com/jotelha/dtool-lookup-server-container-composition
# available below dtool-lookup-server-container-composition
# within the root of this repository, i.e. by
#
#   git clone https://github.com/jotelha/dtool-lookup-server-container-composition
#
# and run test script from within repository root via
#
#   bash tests/run.sh
#
# Docker is required and a clean python venv recommended.
#
set -euxo pipefail
cd dtool-lookup-server-container-composition
docker-compose down --volumes --timeout 30

docker-compose pull
echo "docker image ls"
docker image ls

echo "generate certs and keys"
cd keys
bash generate.sh
bash generate_jwt_key.sh

cd ../..
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel setuptools-scm[toml] importlib-metadata
pip install flake8 pytest pytest-cov pytest-ordering

if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
pip install ".[testing]"
echo "pip list"
pip list

# stop the build if there are Python syntax errors or undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

cd dtool-lookup-server-container-composition
docker-compose -p dtool-lookup-server-container-composition up -d --no-build  # will pull missing images with build command in compose file

sleep 10

echo "docker container ls --all"
docker container ls --all

echo "docker volume ls"
docker volume ls

echo "docker images"
docker-compose images

echo "dtool lookup server log"
docker-compose logs dtool_lookup_server

echo "dtool lookup client log"
docker-compose logs dtool_lookup_client

echo "dtool ls smb://test-share"
docker-compose run dtool_lookup_client dtool ls smb://test-share

echo "explicitly re-evoke dataset indexing"
docker-compose exec -T dtool_lookup_server /refresh_index

echo "dtool query '{}'"
docker-compose run dtool_lookup_client dtool query '{}'

cd ..
sleep 10
pytest --deselect=dtool-lookup-server-container-composition

cd dtool-lookup-server-container-composition
echo "docker-compose down --volumes"
docker-compose down --volumes --timeout 30
cd ..
