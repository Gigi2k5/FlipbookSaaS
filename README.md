# 📘 Flipbook SaaS — Interactive PDF Viewer

Plateforme SaaS légère permettant de transformer des documents PDF en flipbooks interactifs modernes, consultables via un viewer web fluide (desktop & mobile).

Le projet est conçu avec une architecture claire, modulaire et extensible, orientée produit.

## 🚀 Fonctionnalités principales

📄 Import de PDF

🖼️ Conversion PDF → images (pages)

📚 Génération automatique de flipbooks

🧭 Viewer interactif :navigation, fluidepagination, zoom, plein écran

✏️ Éditeur de flipbooks :création, édition, tableau de bord

## 🧠 Vision produit

Ce projet pose les bases d’un SaaS de publication interactive :

catalogues

magazines

brochures

documents commerciaux

présentations clients

L’objectif est de proposer une alternative moderne aux PDF statiques, avec une UX web fluide et immersive.

## 🏗️ Architecture du projet
flipbook-saas/
├── app.py                     # Point d’entrée Flask
├── config.py                  # Configuration globale
├── requirements.txt           # Dépendances Python
├── data/
│   └── flipbooks.json         # Métadonnées des flipbooks
├── uploads/                   # PDFs uploadés (temporaire)
├── services/
│   ├── flipbook_generator.py  # Génération HTML du viewer
│   ├── pdf_processor.py       # Traitement / conversion PDF
│   └── storage_manager.py     # Gestion du stockage
├── routes/
│   ├── main.py                # Pages publiques
│   ├── upload.py              # Upload PDF
│   ├── editor.py              # Interface d’édition
│   └── viewer.py              # Consultation flipbook
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── error.html
│   └── editor/
│       ├── base.html
│       ├── dashboard.html
│       ├── new.html
│       └── edit.html
├── static/
│   ├── css/
│   │   ├── main.css
│   │   └── editor.css
│   └── js/
│       └── upload.js
└── README.md

## 🛠️ Stack technique
### Backend

Python 3

Flask

### Frontend

HTML5 / CSS3

JavaScript vanilla

Viewer basé sur Swiper.js

⚙️ Installation (local)
Prérequis

Python ≥ 3.10

pip

Installation
git clone https://github.com/Gigi2k5/FlipbookSaaS.git
cd flipbook-saas
python -m venv venv
source venv/bin/activate  # Linux / macOS
pip install -r requirements.txt

Lancer l’application
python app.py


Puis ouvrir :

http://localhost:5000

👤 Auteur

Projet conçu et développé par Charbel

📄 Licence

Projet open-source
