from flask import Blueprint, jsonify
from flask_wtf import request
from services.mongo_service import MongoService

upload_api = Blueprint('upload_api', __name__)

@upload_api.route('/upload', methods=['POST'])
def upload_file():
    data = request.form
    file = request.files['file']
    MongoService().insert_file(file)
    return jsonify({'file_id': str(file.id)})