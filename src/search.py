from flask import Blueprint, request, jsonify
from opensearch_client import get_opensearch_client
from config import Config
from custom_response import ApiResponse

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['GET'])
def search_by_keyword():
    keyword = request.args.get('keyword', '')  # Get 'keyword' query parameter
    if not keyword:
        return jsonify({"error": "No keyword provided."}), 400

    query = {
        "query": {
            "match": {
                "ingredients": keyword
            }
        }
    }

    es = get_opensearch_client()
    index_name = Config.OPENSEARCH_INDEX

    try:
        response = es.search(index=index_name, body=query)
        hits = response['hits']['hits']

        results = []
        for hit in hits:
            source = hit['_source']

            source = {
                'title': source.get('title'),
                'categories': source.get('categories')
            }
            result = {
                'id': hit['_id'],
                'source': source
            }
            results.append(result)

        response = ApiResponse(status="success", data=results)
        return jsonify(response.to_dict()), 200
    except Exception as e:
        response = ApiResponse(status="error", message=str(e))
        return jsonify(response.to_dict()), 500


@search_bp.route('/toprated', methods=['GET'])
def get_top_rated():
    query = {
        "query": {
            "range": {
                "rating": {
                    "gt": 4
                }
            }
        }
    }

    es = get_opensearch_client()
    index_name = Config.OPENSEARCH_INDEX

    try:
        response = es.search(index=index_name, body=query)
        hits = response['hits']['hits']

        results = []
        for hit in hits:
            source = hit['_source']

            source = {
                'title': source.get('title'),
                'categories': source.get('categories')
            }
            result = {
                'id': hit['_id'],
                'source': source
            }
            results.append(result)

        response = ApiResponse(status="success", data=results)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        response = ApiResponse(status="error", message=str(e))
        return jsonify(response.to_dict()), 500


@search_bp.route('/getRecipe', methods=['GET'])
def get_recipe_id():
    document_id = request.args.get('id', '')

    es = get_opensearch_client()
    index_name = Config.OPENSEARCH_INDEX

    try:
        response = es.get(index=index_name, id=document_id)

        result = {
            'id': response['_id'],
            'source': response['_source']
        }

        response = ApiResponse(status="success", data=result)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        response = ApiResponse(status="error", message=str(e))
        return jsonify(response.to_dict()), 500


@search_bp.route('/filters', methods=['POST'])
def get_recipes_by_filters():
    data = request.json

    categories = data.get('categories', [])
    ingredients = data.get('ingredients', [])
    rating_threshold = data.get('rating')

    # Start constructing the OpenSearch query
    query = {
        "query": {
            "bool": {
                "must": []
            }
        }
    }

    # Add category filters if provided
    if categories:
        query['query']['bool']['must'].append({
            "bool": {
                "must": [{"match": {"categories": category}} for category in categories]
            }
        })

    # Add ingredient filters if provided
    if ingredients:
        query['query']['bool']['must'].append({
            "bool": {
                "must": [{"match": {"ingredients": ingredient}} for ingredient in ingredients]
            }
        })

    # Add rating filter if provided
    if rating_threshold is not None:
        query['query']['bool']['must'].append({
            "range": {
                "rating": {
                    "gt": rating_threshold
                }
            }
        })

    es = get_opensearch_client()
    index_name = Config.OPENSEARCH_INDEX

    try:
        # Execute search query
        response = es.search(index=index_name, body=query)
        hits = response['hits']['hits']

        results = []
        for hit in hits:
            source = hit['_source']

            source = {
                'title': source.get('title'),
                'categories': source.get('categories')
            }
            result = {
                'id': hit['_id'],
                'source': source
            }
            results.append(result)

        response = ApiResponse(status="success", data=results)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        response = ApiResponse(status="error", message=str(e))
        return jsonify(response.to_dict()), 500
