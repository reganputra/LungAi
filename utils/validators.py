from utils.file_utils import allowed_file
from utils.response_utils import error_response


def validate_prediction_request(request):
    """Validate prediction request"""
    # Check if file is present
    if 'file' not in request.files:
        return error_response('No file provided')

    file = request.files['file']

    # Check if file is selected
    if file.filename == '':
        return error_response('No file selected')

    # Check file extension
    if not allowed_file(file.filename):
        from config import Config
        return error_response(
            f'File type not allowed. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
        )

    return None
