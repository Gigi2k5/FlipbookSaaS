"""Service de gestion du stockage"""

import os
import json
import uuid
import shutil
from datetime import datetime
from config import UPLOAD_FOLDER, FLIPBOOK_FOLDER, METADATA_FILE


class StorageManager:
    """Gestionnaire centralisé du stockage"""
    
    def __init__(self):
        self._ensure_metadata_file()
    
    def _ensure_metadata_file(self):
        if not os.path.exists(METADATA_FILE):
            os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
            self._save_metadata({"flipbooks": {}})
    
    def _load_metadata(self):
        try:
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"flipbooks": {}}
    
    def _save_metadata(self, data):
        try:
            with open(METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def create_flipbook_id(self):
        return str(uuid.uuid4())
    
    def get_flipbook_path(self, flipbook_id):
        return os.path.join(FLIPBOOK_FOLDER, flipbook_id)
    
    def get_upload_path(self, flipbook_id):
        return os.path.join(UPLOAD_FOLDER, f"{flipbook_id}.pdf")
    
    def create_flipbook_directory(self, flipbook_id):
        base_path = self.get_flipbook_path(flipbook_id)
        pages_path = os.path.join(base_path, 'pages')
        os.makedirs(pages_path, exist_ok=True)
        return {"base_path": base_path, "pages_path": pages_path}
    
    def save_flipbook_metadata(self, flipbook_id, metadata):
        data = self._load_metadata()
        data["flipbooks"][flipbook_id] = {
            "id": flipbook_id,
            "title": metadata.get("title", "Sans titre"),
            "pages_count": metadata.get("pages_count", 0),
            "created_at": datetime.now().isoformat(),
            "url": f"/view/{flipbook_id}",
            "pdf_size_bytes": metadata.get("pdf_size_bytes", 0)
        }
        return self._save_metadata(data)
    
    def get_flipbook_metadata(self, flipbook_id):
        return self._load_metadata()["flipbooks"].get(flipbook_id)
    
    def get_all_flipbooks(self):
        return list(self._load_metadata()["flipbooks"].values())
    
    def flipbook_exists(self, flipbook_id):
        metadata = self.get_flipbook_metadata(flipbook_id)
        if not metadata:
            return False
        return os.path.exists(self.get_flipbook_path(flipbook_id))
    
    def delete_flipbook(self, flipbook_id):
        try:
            data = self._load_metadata()
            if flipbook_id in data["flipbooks"]:
                del data["flipbooks"][flipbook_id]
                self._save_metadata(data)
            
            flipbook_path = self.get_flipbook_path(flipbook_id)
            if os.path.exists(flipbook_path):
                shutil.rmtree(flipbook_path)
            
            pdf_path = self.get_upload_path(flipbook_id)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            
            return True
        except Exception:
            return False
    
    def get_stats(self):
        flipbooks = self._load_metadata()["flipbooks"]
        total_pages = sum(fb.get("pages_count", 0) for fb in flipbooks.values())
        total_size = sum(fb.get("pdf_size_bytes", 0) for fb in flipbooks.values())
        return {
            "total_flipbooks": len(flipbooks),
            "total_pages": total_pages,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
    
    def update_flipbook_metadata(self, flipbook_id, updates, allowed_fields=None):
        """Met à jour les métadonnées d'un flipbook"""
        data = self._load_metadata()
        
        if flipbook_id not in data["flipbooks"]:
            return False
        
        for key, value in updates.items():
            if allowed_fields is None or key in allowed_fields:
                data["flipbooks"][flipbook_id][key] = value
        
        return self._save_metadata(data)


# Instance globale
storage = StorageManager()
