"""Configuration centralisée FlipBook SaaS"""

import os

# Chemins
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
FLIPBOOK_FOLDER = os.path.join(BASE_DIR, 'flipbooks')
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
METADATA_FILE = os.path.join(DATA_FOLDER, 'flipbooks.json')

# Limites upload
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30 MB
MAX_FILE_SIZE_MB = 30

# Conversion PDF
PDF_DPI = 120
MAX_IMAGE_WIDTH = 1200
IMAGE_QUALITY = 75
IMAGE_FORMAT = 'JPEG'
ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_MIME_TYPES = ['application/pdf']

# Messages
MESSAGES = {
    'no_file': 'Aucun fichier sélectionné',
    'invalid_type': 'Seuls les fichiers PDF sont acceptés',
    'file_too_large': f'Taille maximale : {MAX_FILE_SIZE_MB} MB',
    'invalid_pdf': 'Fichier PDF invalide ou corrompu',
    'conversion_error': 'Erreur lors de la conversion',
    'not_found': 'Flipbook introuvable',
}


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32).hex())
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Config active selon environnement
config = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig


def allowed_file(filename):
    """Vérifie si l'extension est autorisée"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_directories():
    """Initialise les dossiers et fichiers requis"""
    for directory in [UPLOAD_FOLDER, FLIPBOOK_FOLDER, DATA_FOLDER]:
        os.makedirs(directory, exist_ok=True)
    
    if not os.path.exists(METADATA_FILE):
        import json
        with open(METADATA_FILE, 'w') as f:
            json.dump({'flipbooks': {}}, f)
