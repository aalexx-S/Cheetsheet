# Cheetsheet

## Prerequisite
+ docker
+ docker-compose
+ python 3.7
+ pipenv
+ curl

## Installation
1. Download ElasticSearch docker image.
    ```sh
    $ docker pull docker.elastic.co/elasticsearch/elasticsearch:7.6.2
    ```
2. Launch the local cluster with 3 nodes using `docker compose`.
    ```sh
    $ docker-compose up
    ```
3. Prepare the Cheetsheet sample installer.
    ```sh
    $ pipenv install --dev
    ```
4. Run the Cheetsheet sample installer and populate the local ElasticSearch cluster.
   ```sh
   $ pipenv run python install.py samples
   ```
5. Verify the installation using simple Elastic query.
   ```sh
   $ curl http://localhost:9200/_search\?
   ```

