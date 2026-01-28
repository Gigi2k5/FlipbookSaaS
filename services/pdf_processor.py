"""Service de conversion PDF en images"""

import os
import io
import fitz  # PyMuPDF
from PIL import Image
from config import PDF_DPI, MAX_IMAGE_WIDTH, IMAGE_QUALITY, IMAGE_FORMAT


class PDFProcessor:
    """Convertit un PDF en images optimisées"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = None
        self.pages_count = 0
    
    def open(self):
        try:
            self.doc = fitz.open(self.pdf_path)
            self.pages_count = len(self.doc)
            
            if self.pages_count == 0:
                return {"success": False, "error": "PDF vide"}
            
            return {"success": True, "pages_count": self.pages_count}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        if self.doc:
            self.doc.close()
    
    def extract_page(self, page_num):
        """Extrait une page en image PIL"""
        try:
            page = self.doc[page_num]
            zoom = PDF_DPI / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("jpeg")))
            return img
        except Exception:
            return None
    
    def optimize_image(self, img):
        """Redimensionne et optimise l'image"""
        if img.width > MAX_IMAGE_WIDTH:
            ratio = MAX_IMAGE_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        return img
    
    def convert_to_images(self, output_dir):
        """Convertit toutes les pages en images"""
        pages_dir = os.path.join(output_dir, 'pages')
        os.makedirs(pages_dir, exist_ok=True)
        
        images = []
        
        for page_num in range(self.pages_count):
            img = self.extract_page(page_num)
            if img is None:
                continue
            
            img = self.optimize_image(img)
            filename = f"page_{page_num + 1}.jpg"
            output_path = os.path.join(pages_dir, filename)
            
            img.save(output_path, format=IMAGE_FORMAT, quality=IMAGE_QUALITY, 
                     optimize=True, progressive=True)
            images.append(filename)
        
        self.close()
        
        return {
            "success": len(images) == self.pages_count,
            "pages_count": len(images),
            "images": images
        }


def convert_pdf_to_images(pdf_path, output_dir):
    """Fonction principale de conversion"""
    processor = PDFProcessor(pdf_path)
    
    result = processor.open()
    if not result["success"]:
        return result
    
    return processor.convert_to_images(output_dir)


def get_pdf_info(pdf_path):
    """Récupère les infos d'un PDF"""
    try:
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        info = {
            "success": True,
            "pages_count": len(doc),
            "title": metadata.get("title", "") or "Sans titre",
            "author": metadata.get("author", ""),
            "size_bytes": os.path.getsize(pdf_path)
        }
        doc.close()
        return info
    except Exception as e:
        return {"success": False, "error": str(e)}
