import os
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename

from service.image_service import ImageService
from service.prediction_service import PredictionService
from utils.file_utils import allowed_file, cleanup_file
from utils.response_utils import success_response, error_response
from utils.validators import validate_prediction_request

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        # Validate request
        validation_error = validate_prediction_request(request)
        if validation_error:
            return validation_error

        # Check if model is loaded
        if not current_app.model_service.is_loaded:
            return error_response('Model not loaded. Please check server logs.', 500)

        file = request.files['file']

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Process image
            img_ready, img_ori, img_eq = ImageService.preprocess_image(
                filepath)

            # Make prediction
            raw_prediction = current_app.model_service.predict(img_ready)

            # Process prediction result
            prediction_result = PredictionService.process_prediction(
                raw_prediction)

            # Prepare response
            response_data = {
                'prediction': prediction_result['result'],
                'confidence': prediction_result['confidence'],
                'raw_prediction': prediction_result['raw_prediction']
            }

            # Add images to response if requested
            include_images = request.form.get(
                'include_images', 'false').lower() == 'true'
            if include_images:
                img_ori_b64 = ImageService.image_to_base64(img_ori)
                img_eq_b64 = ImageService.image_to_base64(img_eq)

                if img_ori_b64 and img_eq_b64:
                    response_data['images'] = {
                        'original': img_ori_b64,
                        'equalized': img_eq_b64
                    }

            return success_response(response_data)

        finally:
            cleanup_file(filepath)

    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return error_response(f'Prediction failed: {str(e)}', 500)
