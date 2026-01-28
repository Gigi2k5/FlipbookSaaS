"""Route de l'éditeur de flipbook"""

from flask import Blueprint, render_template, abort, request, jsonify
from services.storage_manager import storage

editor_bp = Blueprint('editor', __name__)


@editor_bp.route('/editor')
def editor_home():
    """Page éditeur - Dashboard par défaut"""
    flipbooks = storage.get_all_flipbooks()
    return render_template('editor/dashboard.html', flipbooks=flipbooks)


@editor_bp.route('/editor/new')
def editor_new():
    """Création d'un nouveau flipbook"""
    return render_template('editor/new.html')


@editor_bp.route('/editor/<flipbook_id>')
def editor_edit(flipbook_id):
    """Édition d'un flipbook existant"""
    if not storage.flipbook_exists(flipbook_id):
        abort(404)
    
    flipbook = storage.get_flipbook_metadata(flipbook_id)
    return render_template('editor/edit.html', flipbook=flipbook)


@editor_bp.route('/api/flipbook/<flipbook_id>', methods=['GET'])
def api_get_flipbook(flipbook_id):
    """API: Récupérer les données d'un flipbook"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    flipbook = storage.get_flipbook_metadata(flipbook_id)
    return jsonify({"success": True, "flipbook": flipbook})


@editor_bp.route('/api/flipbook/<flipbook_id>', methods=['PATCH'])
def api_update_flipbook(flipbook_id):
    """API: Mettre à jour les paramètres d'un flipbook"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Données invalides"}), 400
    
    # Champs modifiables
    allowed_fields = ['title', 'mode', 'background_color', 'background_image', 'logo']
    
    # Vérifier si on doit régénérer le viewer
    regenerate_fields = ['mode', 'background_color']
    should_regenerate = any(field in data for field in regenerate_fields)
    
    success = storage.update_flipbook_metadata(flipbook_id, data, allowed_fields)
    
    if success and should_regenerate:
        # Régénérer le viewer avec les nouveaux paramètres
        from services.flipbook_generator import generate_viewer
        
        metadata = storage.get_flipbook_metadata(flipbook_id)
        flipbook_path = storage.get_flipbook_path(flipbook_id)
        
        generate_viewer(
            flipbook_id,
            metadata.get('pages_count', 0),
            flipbook_path,
            mode=metadata.get('mode', 'default'),
            background_color=metadata.get('background_color', '#0f0f0f')
        )
    
    if success:
        flipbook = storage.get_flipbook_metadata(flipbook_id)
        return jsonify({"success": True, "flipbook": flipbook})
    else:
        return jsonify({"success": False, "error": "Erreur de sauvegarde"}), 500


@editor_bp.route('/api/flipbook/<flipbook_id>/delete', methods=['POST'])
def api_delete_flipbook(flipbook_id):
    """API: Supprimer un flipbook"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    success = storage.delete_flipbook(flipbook_id)
    
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Erreur de suppression"}), 500


@editor_bp.route('/api/flipbook/<flipbook_id>/pages')
def api_get_pages(flipbook_id):
    """API: Récupérer la liste des pages d'un flipbook"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    pages_count = metadata.get('pages_count', 0)
    
    pages = []
    for i in range(1, pages_count + 1):
        pages.append({
            "number": i,
            "url": f"/view/{flipbook_id}/pages/page_{i}.jpg"
        })
    
    return jsonify({
        "success": True,
        "pages": pages,
        "total": pages_count
    })


@editor_bp.route('/api/flipbook/<flipbook_id>/hotspots', methods=['GET'])
def api_get_hotspots(flipbook_id):
    """API: Récupérer les hotspots d'un flipbook"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    hotspots = metadata.get('hotspots', [])
    
    return jsonify({"success": True, "hotspots": hotspots})


@editor_bp.route('/api/flipbook/<flipbook_id>/hotspots', methods=['POST'])
def api_add_hotspot(flipbook_id):
    """API: Ajouter un hotspot"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Données invalides"}), 400
    
    required = ['page', 'x', 'y', 'width', 'height', 'type']
    if not all(k in data for k in required):
        return jsonify({"success": False, "error": "Champs manquants"}), 400
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    hotspots = metadata.get('hotspots', [])
    
    # Générer un ID unique
    import uuid
    hotspot = {
        'id': str(uuid.uuid4())[:8],
        'page': data['page'],
        'x': data['x'],
        'y': data['y'],
        'width': data['width'],
        'height': data['height'],
        'type': data['type'],  # 'url' ou 'page'
        'target': data.get('target', ''),
        'label': data.get('label', '')
    }
    
    hotspots.append(hotspot)
    storage.update_flipbook_metadata(flipbook_id, {'hotspots': hotspots})
    
    # Régénérer le viewer
    regenerate_viewer_with_hotspots(flipbook_id)
    
    return jsonify({"success": True, "hotspot": hotspot})


@editor_bp.route('/api/flipbook/<flipbook_id>/hotspots/<hotspot_id>', methods=['DELETE'])
def api_delete_hotspot(flipbook_id, hotspot_id):
    """API: Supprimer un hotspot"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    hotspots = metadata.get('hotspots', [])
    
    hotspots = [h for h in hotspots if h.get('id') != hotspot_id]
    storage.update_flipbook_metadata(flipbook_id, {'hotspots': hotspots})
    
    # Régénérer le viewer
    regenerate_viewer_with_hotspots(flipbook_id)
    
    return jsonify({"success": True})


@editor_bp.route('/api/flipbook/<flipbook_id>/hotspots/<hotspot_id>', methods=['PATCH'])
def api_update_hotspot(flipbook_id, hotspot_id):
    """API: Modifier un hotspot"""
    if not storage.flipbook_exists(flipbook_id):
        return jsonify({"success": False, "error": "Flipbook introuvable"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Données invalides"}), 400
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    hotspots = metadata.get('hotspots', [])
    
    for h in hotspots:
        if h.get('id') == hotspot_id:
            for key in ['x', 'y', 'width', 'height', 'type', 'target', 'label']:
                if key in data:
                    h[key] = data[key]
            break
    
    storage.update_flipbook_metadata(flipbook_id, {'hotspots': hotspots})
    
    # Régénérer le viewer
    regenerate_viewer_with_hotspots(flipbook_id)
    
    return jsonify({"success": True})


def regenerate_viewer_with_hotspots(flipbook_id):
    """Régénère le viewer avec les hotspots"""
    from services.flipbook_generator import generate_viewer
    
    metadata = storage.get_flipbook_metadata(flipbook_id)
    flipbook_path = storage.get_flipbook_path(flipbook_id)
    
    generate_viewer(
        flipbook_id,
        metadata.get('pages_count', 0),
        flipbook_path,
        mode=metadata.get('mode', 'default'),
        background_color=metadata.get('background_color', '#0f0f0f'),
        hotspots=metadata.get('hotspots', [])
    )
