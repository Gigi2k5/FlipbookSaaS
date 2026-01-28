# FlipBook SaaS

Convertisseur PDF → Flipbook interactif.

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

Ouvrir http://localhost:5000

## Structure

```
├── app.py              # Point d'entrée Flask
├── config.py           # Configuration
├── routes/             # Routes HTTP
├── services/           # Logique métier
├── templates/          # Templates HTML
├── static/             # CSS/JS
├── uploads/            # PDFs temporaires
└── flipbooks/          # Flipbooks générés
```

## Tech

- Flask 3.0
- PyMuPDF (conversion PDF)
- Pillow (images)
- Swiper.js (viewer)
