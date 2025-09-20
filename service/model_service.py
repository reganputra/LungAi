import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import logging

from config import Config


class ModelService:
    """Service class for handling model operations"""

    def __init__(self):
        self.model = None
        self.is_loaded = False

    def load_model(self):
        """Load the machine learning model"""
        try:
            self.model = load_model(Config.MODEL_PATH)
            self.is_loaded = True
            logging.info("Model loaded successfully")
            return True
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            self.is_loaded = False
            return False

    def predict(self, image_array):
        """Make prediction on preprocessed image"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")

        try:
            prediction = self.model.predict(image_array)
            logging.info(f"Raw prediction: {prediction}")
            return prediction
        except Exception as e:
            logging.error(f"Error during prediction: {str(e)}")
            raise

    def get_model_info(self):
        """Get model information"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")

        return {
            'input_shape': self.model.input_shape,
            'output_shape': self.model.output_shape,
            'model_type': 'MobileNet for Lung Cancer Detection',
            'is_loaded': self.is_loaded
        }
