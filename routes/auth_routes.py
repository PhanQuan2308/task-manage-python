from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.find_by_username(data['username']):
        return jsonify({"msg": "Username already exists"}), 400

    User.create_user(data['username'], data['password'])
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.verify_password(data['username'], data['password'])
    if user:
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401
