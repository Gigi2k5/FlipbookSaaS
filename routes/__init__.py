"""Routes package"""

from .main import main_bp
from .upload import upload_bp
from .viewer import viewer_bp
from .editor import editor_bp

__all__ = ['main_bp', 'upload_bp', 'viewer_bp', 'editor_bp']
