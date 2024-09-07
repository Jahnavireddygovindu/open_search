from opensearchpy import OpenSearch
from config import Config


def get_opensearch_client():
    es = OpenSearch(
        [Config.OPENSEARCH_ENDPOINT],
        http_auth=(Config.OPENSEARCH_USERNAME, Config.OPENSEARCH_PASSWORD),
        scheme="https",
        port=443
    )
    return es
