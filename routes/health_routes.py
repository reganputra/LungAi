from flask import Blueprint, current_app
from utils.response_utils import success_response, error_response

health_bp = Blueprint('health', __name__)


@health_bp.route('/', methods=['GET'])
@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response({
        'message': 'Lung Cancer Prediction API is running',
        'model_loaded': current_app.model_service.is_loaded
    })


@health_bp.route('/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    try:
        model_info = current_app.model_service.get_model_info()
        return success_response({'model_info': model_info})

    except RuntimeError as e:
        return error_response(str(e), 500)
    except Exception as e:
        logging.error(f"Error getting model info: {str(e)}")
        return error_response(f'Failed to get model info: {str(e)}', 500)
