# elasticsearch-exr
In order to use this program follow these steps:
1. install elasticsearch by typing this line in terminal:
    pip3 install elasticsearch
2. Follow the guidelines here (only items 1-5):
    https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-stack-docker.html.
3. Start docker by typing this line in terminal:
    docker run --rm -p 9200:9200 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.2.3
4. Let the docker run while you use the program.