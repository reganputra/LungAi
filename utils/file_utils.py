import os
import logging
from config import Config


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def cleanup_file(filepath):
    """Remove file if it exists"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logging.debug(f"Cleaned up file: {filepath}")
    except Exception as e:
        logging.warning(f"Failed to cleanup file {filepath}: {str(e)}")
