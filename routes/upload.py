"""Route d'upload et conversion de PDF"""

import os
import magic
from flask import Blueprint, request, jsonify
from config import allowed_file, ALLOWED_MIME_TYPES, MESSAGES
from services.storage_manager import storage
from services.pdf_processor import convert_pdf_to_images, get_pdf_info
from services.flipbook_generator import generate_viewer

upload_bp = Blueprint('upload', __name__)


def validate_file(file):
    """Valide le fichier uploadé"""
    if not file or file.filename == '':
        return False, MESSAGES['no_file']
    
    if not allowed_file(file.filename):
        return False, MESSAGES['invalid_type']
    
    # Validation MIME
    try:
        file_mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        if file_mime not in ALLOWED_MIME_TYPES:
            return False, MESSAGES['invalid_type']
    except Exception:
        pass  # Fallback si python-magic échoue
    
    return True, None


@upload_bp.route('/upload', methods=['POST'])
def upload_pdf():
    """Upload et conversion de PDF"""
    
    # Validation
    if 'file' not in request.files:
        return jsonify({"success": False, "error": MESSAGES['no_file']}), 400
    
    file = request.files['file']
    valid, error = validate_file(file)
    if not valid:
        return jsonify({"success": False, "error": error}), 400
    
    # Création flipbook
    try:
        flipbook_id = storage.create_flipbook_id()
        paths = storage.create_flipbook_directory(flipbook_id)
        pdf_path = storage.get_upload_path(flipbook_id)
        file.save(pdf_path)
        
        # Info PDF
        pdf_info = get_pdf_info(pdf_path)
        if not pdf_info["success"]:
            storage.delete_flipbook(flipbook_id)
            return jsonify({"success": False, "error": MESSAGES['invalid_pdf']}), 400
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
    # Conversion
    try:
        result = convert_pdf_to_images(pdf_path, paths["base_path"])
        if not result["success"]:
            storage.delete_flipbook(flipbook_id)
            return jsonify({"success": False, "error": MESSAGES['conversion_error']}), 500
        
    except Exception as e:
        storage.delete_flipbook(flipbook_id)
        return jsonify({"success": False, "error": str(e)}), 500
    
    # Génération viewer
    try:
        viewer_result = generate_viewer(flipbook_id, result["pages_count"], paths["base_path"])
        if not viewer_result["success"]:
            storage.delete_flipbook(flipbook_id)
            return jsonify({"success": False, "error": MESSAGES['conversion_error']}), 500
        
    except Exception as e:
        storage.delete_flipbook(flipbook_id)
        return jsonify({"success": False, "error": str(e)}), 500
    
    # Sauvegarde métadonnées
    storage.save_flipbook_metadata(flipbook_id, {
        "title": pdf_info.get("title", "Sans titre"),
        "pages_count": result["pages_count"],
        "pdf_size_bytes": os.path.getsize(pdf_path)
    })
    
    return jsonify({
        "success": True,
        "flipbook_id": flipbook_id,
        "url": f"/view/{flipbook_id}",
        "pages_count": result["pages_count"],
        "title": pdf_info.get("title", "Sans titre")
    })


@upload_bp.route('/upload/status/<flipbook_id>')
def upload_status(flipbook_id):
    """Vérifie le statut d'un flipbook"""
    if storage.flipbook_exists(flipbook_id):
        return jsonify({
            "success": True,
            "status": "completed",
            "metadata": storage.get_flipbook_metadata(flipbook_id)
        })
    return jsonify({"success": False, "status": "not_found"}), 404
