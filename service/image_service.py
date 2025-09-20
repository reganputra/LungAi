import cv2
import numpy as np
import io
import base64
from PIL import Image
import logging

from config import Config


class ImageService:
    """Service class for image processing operations"""

    @staticmethod
    def histogram_equalization(img):
        """Apply histogram equalization to improve image contrast"""
        return cv2.equalizeHist(img)

    @staticmethod
    def preprocess_image(image_path):
        """
        Preprocess image for model prediction
        Returns processed image array and original/equalized images
        """
        try:
            # Read image in grayscale
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError("Could not read image file")

            # Apply histogram equalization
            img_eq = ImageService.histogram_equalization(img)

            # Resize to target size
            img_resized = cv2.resize(img_eq, Config.TARGET_SIZE)

            # Convert grayscale to RGB (3 channels)
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2RGB)

            # Normalize to [0,1]
            img_normalized = img_rgb / 255.0

            # Add batch dimension
            img_ready = np.expand_dims(img_normalized, axis=0)

            return img_ready, img, img_eq

        except Exception as e:
            logging.error(f"Error preprocessing image: {str(e)}")
            raise

    @staticmethod
    def image_to_base64(img_array):
        """Convert numpy array to base64 string for JSON response"""
        try:
            # Convert to PIL Image
            pil_img = Image.fromarray(img_array.astype('uint8'))

            # Save to bytes buffer
            buffer = io.BytesIO()
            pil_img.save(buffer, format='PNG')
            buffer.seek(0)

            # Encode to base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            return img_base64
        except Exception as e:
            logging.error(f"Error converting image to base64: {str(e)}")
            return None
