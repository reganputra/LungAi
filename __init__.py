"""
Lung Cancer Prediction API Package

A Flask-based REST API for lung cancer detection using deep learning.
This package provides a complete machine learning service for medical image analysis.

Author: Your Name
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Lung Cancer Prediction API using MobileNet"

# Make key classes/functions easily importable from the main package
from .app import create_app
from .config import Config

# Define what gets imported when someone does: from LungAi import *
__all__ = ['create_app', 'Config']
