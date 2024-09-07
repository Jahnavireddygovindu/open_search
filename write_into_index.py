import json
from opensearchpy import OpenSearch


endpoint = 'https://your-opensearch-endpoint.amazonaws.com'
username = 'admin'
password = 'Passw0rd@'

# Initialize OpenSearch client
es = OpenSearch(
    [endpoint],
    http_auth=(username,password),  # if authentication is enabled
    scheme="https",
    port=443
)

try:
    print(es.info())
except Exception as e:
    print(f"Error: {e}")


data_json_path = "dataset/full_format_recipes.json"
# Load the JSON data from file
with open(data_json_path, 'r') as f:
    documents = json.load(f)

# Index the documents into OpenSearch
for doc in documents:
    response = es.index(
        index='all_recipes',
        body=doc,
        # id=doc['id'],  # Optionally use the 'id' field from the JSON
        refresh=True  # Ensure the document is searchable immediately
    )
    print(f"Indexed document {doc}: {response['result']}")

print("All documents indexed successfully.")
