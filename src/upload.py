import json
import uuid
from opensearch_client import get_opensearch_client

def upload_documents_from_file(index_name, file_path):
    es = get_opensearch_client()

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of documents.")

        responses = []
        for index, doc in enumerate(data):
            doc_id = str(index)  # Use index as the document ID
            response = es.index(index=index_name, id=doc_id, body=doc)
            responses.append(response)

        return responses

    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise Exception("Error decoding JSON file.")
    except Exception as e:
        raise Exception(f"Error uploading documents: {str(e)}")
