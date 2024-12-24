from flask import Flask
from flask_migrate import Migrate
from backend.extensions.extensions import db, jwt, cors, celery
from backend.config.environment import CONFIG, ENVIRONMENT, Environment
from backend.auth.models import User
import logging
import os

# Initialize migrations
migrate = Migrate()

def create_app(config_class=CONFIG):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db, directory='backend/migrations')
    jwt.init_app(app)
    
    # Configure CORS with proper headers
    cors.init_app(app, 
        resources={r"/*": {
            "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
            "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization", "Cache-Control"],
            "expose_headers": ["Authorization", "Content-Type"],
            "supports_credentials": True,
            "send_wildcard": False
        }}
    )
    
    # Additional error handlers for JWT
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.debug(f"Invalid token error: {error}")
        return {"error": "Invalid token"}, 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        app.logger.debug(f"Unauthorized error: {error}")
        return {"error": "No token provided"}, 401
        
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.debug("Token expired")
        return {"error": "Token has expired"}, 401
        
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        app.logger.debug("Fresh token required")
        return {"error": "Fresh token required"}, 401
        
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        try:
            user = User.query.filter_by(id=int(identity)).one_or_none()
            return user
        except (ValueError, TypeError):
            return None
    celery.conf.update(app.config)
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
            if ENVIRONMENT == Environment.DEVELOPMENT:
                # Create test user if it doesn't exist
                test_user = User.query.filter_by(email='test@example.com').first()
                if not test_user:
                    test_user = User(username='testuser', email='test@example.com')
                    test_user.set_password('TestUser@2024Secure!')
                    db.session.add(test_user)
                    db.session.commit()
                    app.logger.info('Test user created successfully')
                else:
                    app.logger.info('Test user already exists')
        except Exception as e:
            app.logger.error(f'Database initialization error: {str(e)}')
            db.session.rollback()  # Rollback on error
            # Try to create tables if they don't exist
            db.create_all()
            app.logger.info('Database tables created')
    
    # Register blueprints
    from backend.api.routes import api_bp
    from backend.auth.routes import auth_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app
