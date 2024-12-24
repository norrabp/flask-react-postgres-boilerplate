from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.auth.models import User
from backend.app import db
import logging
from pydantic import ValidationError

from backend.auth.request_models import LoginRequest, RegisterRequest

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = RegisterRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    
    if User.query.filter_by(username=data.username).first():
        return jsonify({'error': 'Username already registered'}), 400

    if User.query.filter_by(email=data.email).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    user = User(
        username=data.username,
        email=data.email
    )
    user.set_password(data.password)
    user.create()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = LoginRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    
    logger.info(f"Login attempt for email: {data.email}")

    user = User.query.filter_by(email=data.email).first()
    
    if not user or not user.check_password(data.password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    logger.info(f"Login successful for user {user.id}")
    response = jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    })
    return response, 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })
