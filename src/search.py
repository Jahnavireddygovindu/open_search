
from flask import Blueprint, request, jsonify
from opensearch_client import get_opensearch_client
from config import Config

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_documents():
    keyword = request.args.get('keyword', '')  # Get 'keyword' query parameter
    if not keyword:
        return jsonify({"error": "No keyword provided."}), 400

    query = {
        "query": {
            "match": {
                "text": keyword
            }
        }
    }

    es = get_opensearch_client()
    index_name = Config.OPENSEARCH_INDEX

    try:
        response = es.search(index=index_name, body=query)
        return jsonify(response['hits']['hits']), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
