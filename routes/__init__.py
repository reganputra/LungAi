"""
Routes package for the Lung Cancer Prediction API.

Contains all the API endpoint definitions organized as Flask blueprints.
This package handles HTTP routing and request/response processing.
"""

from .health_routes import health_bp
from .prediction_routes import prediction_bp

# Define what gets imported when someone does: from routes import *
__all__ = ['health_bp', 'prediction_bp']
