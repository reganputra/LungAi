import numpy as np
import logging


class PredictionService:
    """Service class for prediction business logic"""

    @staticmethod
    def process_prediction(prediction):
        """
        Process raw model prediction into human-readable format
        Returns result, confidence, and processed prediction
        """
        try:
            if prediction.shape[1] == 1:  # Binary classification
                probability = float(prediction[0][0])
                if probability < 0.5:
                    result = "Kanker Paru-paru"
                    confidence = 1 - probability
                else:
                    result = "Normal"
                    confidence = probability
            else:  # Multi-class classification
                class_idx = int(np.argmax(prediction))
                confidence = float(np.max(prediction))
                result = f"Class {class_idx}"

            return {
                'result': result,
                'confidence': confidence,
                'raw_prediction': prediction.tolist()
            }

        except Exception as e:
            logging.error(f"Error processing prediction: {str(e)}")
            raise
