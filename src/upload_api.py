# upload_api.py
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from upload import upload_documents_from_file
from config import Config

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if file and file.filename.endswith('.json'):
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)

        try:
            responses = upload_documents_from_file(Config.OPENSEARCH_INDEX, file_path)
            return jsonify({"status": "success", "responses": responses}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.remove(file_path)  # Clean up the uploaded file
    else:
        return jsonify({"error": "Invalid file type. Only JSON files are allowed."}), 400
