"""Routes du viewer flipbook"""

import os
from flask import Blueprint, send_from_directory, abort, render_template
from services.storage_manager import storage
from config import MESSAGES

viewer_bp = Blueprint('viewer', __name__)


@viewer_bp.route('/view/<flipbook_id>')
def view_flipbook(flipbook_id):
    """Affiche le viewer d'un flipbook"""
    if not storage.flipbook_exists(flipbook_id):
        return render_template('error.html',
            error_title="Flipbook introuvable",
            error_message=MESSAGES['not_found'],
            error_code=404
        ), 404
    
    flipbook_path = storage.get_flipbook_path(flipbook_id)
    viewer_file = os.path.join(flipbook_path, 'viewer.html')
    
    if not os.path.exists(viewer_file):
        # Régénérer le viewer si nécessaire
        from services.flipbook_generator import generate_viewer
        metadata = storage.get_flipbook_metadata(flipbook_id)
        generate_viewer(
            flipbook_id, 
            metadata.get('pages_count', 0), 
            flipbook_path,
            mode=metadata.get('mode', 'default'),
            background_color=metadata.get('background_color', '#0f0f0f'),
            hotspots=metadata.get('hotspots', [])
        )
    
    return send_from_directory(flipbook_path, 'viewer.html')


@viewer_bp.route('/view/<flipbook_id>/pages/<filename>')
def serve_page(flipbook_id, filename):
    """Sert les images des pages"""
    if not storage.flipbook_exists(flipbook_id):
        abort(404)
    
    pages_dir = os.path.join(storage.get_flipbook_path(flipbook_id), 'pages')
    file_path = os.path.join(pages_dir, filename)
    
    if not os.path.exists(file_path):
        abort(404)
    
    return send_from_directory(pages_dir, filename, mimetype='image/jpeg', max_age=86400)


@viewer_bp.route('/flipbook/<flipbook_id>/info')
def flipbook_info(flipbook_id):
    """Retourne les infos d'un flipbook en JSON"""
    if not storage.flipbook_exists(flipbook_id):
        return {"success": False, "error": MESSAGES['not_found']}, 404
    
    return {"success": True, "flipbook": storage.get_flipbook_metadata(flipbook_id)}


@viewer_bp.route('/embed/<flipbook_id>')
def embed_flipbook(flipbook_id):
    """Version embed du flipbook"""
    if not storage.flipbook_exists(flipbook_id):
        abort(404)
    
    return send_from_directory(storage.get_flipbook_path(flipbook_id), 'viewer.html')


@viewer_bp.route('/flipbook/<flipbook_id>/download')
def download_pdf(flipbook_id):
    """Télécharge le PDF original"""
    if not storage.flipbook_exists(flipbook_id):
        abort(404)
    
    pdf_path = storage.get_upload_path(flipbook_id)
    if not os.path.exists(pdf_path):
        abort(404)
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    filename = f"{metadata.get('title', 'document')}.pdf"
    
    return send_from_directory(
        os.path.dirname(pdf_path),
        os.path.basename(pdf_path),
        as_attachment=True,
        download_name=filename
    )


@viewer_bp.route('/flipbook/<flipbook_id>/regenerate', methods=['POST'])
def regenerate_viewer(flipbook_id):
    """Régénère le viewer avec les paramètres actuels"""
    if not storage.flipbook_exists(flipbook_id):
        return {"success": False, "error": "Flipbook introuvable"}, 404
    
    from services.flipbook_generator import generate_viewer
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    flipbook_path = storage.get_flipbook_path(flipbook_id)
    
    result = generate_viewer(
        flipbook_id,
        metadata.get('pages_count', 0),
        flipbook_path,
        mode=metadata.get('mode', 'default'),
        background_color=metadata.get('background_color', '#0f0f0f'),
        hotspots=metadata.get('hotspots', [])
    )
    
    return {"success": result["success"]}
