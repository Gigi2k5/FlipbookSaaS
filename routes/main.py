"""Route principale - Page d'accueil"""

from flask import Blueprint, render_template
from services.storage_manager import storage

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Page d'accueil"""
    return render_template('home.html',
        stats=storage.get_stats(),
        recent_flipbooks=storage.get_all_flipbooks()[-3:]
    )


@main_bp.route('/health')
def health():
    """Endpoint de santé"""
    return {"status": "ok", "service": "FlipBook SaaS"}
