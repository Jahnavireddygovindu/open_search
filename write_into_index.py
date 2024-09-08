import json
from opensearchpy import OpenSearch, RequestsHttpConnection

# Replace these with your OpenSearch URL, username, and password
host = 'search-learning-xm7e7q544mrpb4bfdvaqb32dpa.eu-north-1.es.amazonaws.com'
port = 443
auth = ('admin', 'Passw0rd@')  # Tuple with username and password

# Create an OpenSearch client
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    connection_class=RequestsHttpConnection,
    timeout = 1200
)

def check_connection():
    try:
        # Perform a health check
        response = client.cluster.health()
        print(f"Connection successful. Cluster health: {response['status']}")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

def upload_documents_from_file(index_name, file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of documents.")

        responses = []
        for index, doc in enumerate(data):
            print(f"Indexing document {index}")
            doc_id = str(index)  # Use index as the document ID
            response = client.index(index=index_name, id=doc_id, body=doc,)
            responses.append(response)

        return responses

    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise Exception("Error decoding JSON file.")
    except Exception as e:
        raise Exception(f"Error uploading documents: {str(e)}")

if __name__ == '__main__':
    if check_connection():
        index_name = 'recipe_management'
        file_path = 'dataset/full_format_recipes.json'

        responses = upload_documents_from_file(index_name, file_path)
        print('Upload responses:', responses)
    else:
        print("Failed to connect to OpenSearch.")
