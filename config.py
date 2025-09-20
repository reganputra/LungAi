class Config:
    """Application configuration"""
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
    MODEL_PATH = "model_mobilenet (1).keras"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    TARGET_SIZE = (224, 224)
