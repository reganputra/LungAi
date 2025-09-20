import os
import logging
from flask import Flask
from flask_cors import CORS

from config import Config
from routes.prediction_routes import prediction_bp
from routes.health_routes import health_bp
from service.model_service import ModelService
from utils.logger import setup_logger


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup CORS
    CORS(app)

    # Setup logging
    setup_logger()

    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize model service
    model_service = ModelService()
    if not model_service.load_model():
        logging.error("Failed to load model. Server will not start properly.")

    # Store model service in app context
    app.model_service = model_service

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(prediction_bp)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Register global error handlers"""
    from utils.response_utils import error_response

    @app.errorhandler(413)
    def too_large(e):
        return error_response('File too large. Maximum file size is 16MB.', 413)

    @app.errorhandler(404)
    def not_found(e):
        return error_response('Endpoint not found', 404)

    @app.errorhandler(500)
    def internal_error(e):
        logging.error(f"Internal server error: {str(e)}")
        return error_response('Internal server error', 500)


if __name__ == '__main__':
    app = create_app()
    logging.info("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
