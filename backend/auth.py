from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User
from .app import db
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        logger.error("No JSON data in request")
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        logger.error("Missing email or password in request")
        return jsonify({'error': 'Email and password are required'}), 400

    logger.info(f"Login attempt for email: {email}")
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        logger.info(f"Login successful for user {user.id}")
        response = jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        })
        return response, 200
    
    logger.warning(f"Login failed for email: {email}")
    return jsonify({'error': 'Invalid credentials'}), 401

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
