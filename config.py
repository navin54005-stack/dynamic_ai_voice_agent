# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv'}
    
    # AI settings
    MAX_RESPONSE_WORDS = 30  # Keep responses short
    CLUSTER_COUNT = 3  # Number of conversation clusters
    
    # Session settings
    SESSION_TIMEOUT = 3600  # 1 hour session timeout

# Create necessary directories
import os
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data/sessions', exist_ok=True)
os.makedirs('data/clusters', exist_ok=True)
os.makedirs('data/patterns', exist_ok=True)
