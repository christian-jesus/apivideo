from flask import Blueprint, jsonify, request
from services.mongo_service import MongoService

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']
    user = MongoService().get_user(username, password)
    if user:
        return jsonify({'token': 'your_token'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401