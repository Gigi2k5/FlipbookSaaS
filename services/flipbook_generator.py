"""Service de génération du viewer HTML avec modes d'affichage et hotspots"""

import os
import json


class FlipbookGenerator:
    """Génère le viewer HTML pour flipbooks avec modes multiples et hotspots"""
    
    MODES = {
        'default': 'Standard',
        'magazine': 'Magazine',
        'coverflow': 'Coverflow',
        'cards': 'Cartes',
        'cube': 'Cube',
        'flip': 'Flip',
        'fade': 'Fondu'
    }
    
    def __init__(self, flipbook_id, pages_count, mode='default', background_color='#0f0f0f', hotspots=None):
        self.flipbook_id = flipbook_id
        self.pages_count = pages_count
        self.mode = mode if mode in self.MODES else 'default'
        self.background_color = background_color or '#0f0f0f'
        self.hotspots = hotspots or []
    
    def generate(self, output_path):
        try:
            html = self._build_html()
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            return True
        except Exception as e:
            print(f"Error generating viewer: {e}")
            return False
    
    def _get_hotspots_for_page(self, page_num):
        return [h for h in self.hotspots if h.get('page') == page_num]
    
    def _build_hotspots_html(self, page_num):
        page_hotspots = self._get_hotspots_for_page(page_num)
        html = ''
        for h in page_hotspots:
            if h.get('type') == 'url':
                html += f'''<a href="{h.get('target', '#')}" target="_blank" class="hotspot" 
                   style="left:{h.get('x', 0)}%;top:{h.get('y', 0)}%;width:{h.get('width', 10)}%;height:{h.get('height', 10)}%"
                   title="{h.get('label', '')}"></a>'''
            elif h.get('type') == 'page':
                html += f'''<div class="hotspot hotspot-page" data-target-page="{h.get('target', 1)}"
                     style="left:{h.get('x', 0)}%;top:{h.get('y', 0)}%;width:{h.get('width', 10)}%;height:{h.get('height', 10)}%"
                     title="{h.get('label', '')}"></div>'''
        return html
    
    def _build_html(self):
        hotspots_json = json.dumps(self.hotspots)
        
        # Pages pour Swiper
        swiper_pages = '\n'.join([
            f'''                <div class="swiper-slide" data-page="{i}">
                    <div class="page">
                        <img src="/view/{self.flipbook_id}/pages/page_{i}.jpg" alt="Page {i}" loading="lazy">
                        {self._build_hotspots_html(i)}
                    </div>
                </div>'''
            for i in range(1, self.pages_count + 1)
        ])
        
        mode_options = '\n'.join([
            f'''                        <button class="mode-option{' active' if key == self.mode else ''}" data-mode="{key}">{name}</button>'''
            for key, name in self.MODES.items()
        ])
        
        return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipbook</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
    <style>
        :root {{
            --bg: {self.background_color};
            --surface: #1a1a1a;
            --surface-2: #242424;
            --border: #2a2a2a;
            --text: #e5e5e5;
            --text-muted: #888;
            --accent: #3b82f6;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            user-select: none;
        }}
        
        /* Header */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1.5rem;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            flex-shrink: 0;
            z-index: 100;
        }}
        
        .logo {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .logo svg {{ width: 20px; height: 20px; fill: var(--accent); }}
        
        .header-actions {{ display: flex; gap: 0.5rem; align-items: center; }}
        
        .mode-selector {{ position: relative; }}
        
        .mode-btn {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.75rem;
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text);
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.15s;
        }}
        
        .mode-btn:hover {{ background: var(--border); }}
        .mode-btn svg {{ width: 16px; height: 16px; }}
        
        .mode-dropdown {{
            position: absolute;
            top: calc(100% + 0.5rem);
            right: 0;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            min-width: 140px;
            display: none;
            z-index: 200;
            overflow: hidden;
        }}
        
        .mode-dropdown.open {{ display: block; }}
        
        .mode-option {{
            display: block;
            width: 100%;
            padding: 0.6rem 1rem;
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.85rem;
            text-align: left;
            cursor: pointer;
            transition: all 0.15s;
        }}
        
        .mode-option:hover {{ background: var(--surface-2); color: var(--text); }}
        .mode-option.active {{ background: var(--accent); color: #fff; }}
        
        .btn {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.15s;
        }}
        
        .btn:hover {{ background: var(--border); color: var(--text); }}
        .btn:disabled {{ opacity: 0.3; cursor: not-allowed; }}
        .btn svg {{ width: 18px; height: 18px; }}
        
        /* Viewer */
        .viewer {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            overflow: hidden;
            position: relative;
        }}
        
        /* Swiper */
        .swiper-container {{
            width: 100%;
            height: 100%;
            max-width: 1200px;
        }}
        
        .swiper {{ width: 100%; height: 100%; }}
        
        .swiper-slide {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .page {{
            position: relative;
            background: #fff;
            box-shadow: 0 4px 24px rgba(0,0,0,0.6);
            border-radius: 2px;
            overflow: hidden;
            max-height: calc(100vh - 140px);
        }}
        
        .page img {{
            display: block;
            max-width: 100%;
            max-height: calc(100vh - 140px);
            object-fit: contain;
        }}
        
        .swiper.mode-coverflow .swiper-slide {{ width: 70%; }}
        .swiper.mode-cards .swiper-slide {{ width: 85%; }}
        
        /* ========================================
           MAGAZINE MODE - Ultra Réaliste
           ======================================== */
        .magazine-container {{
            display: none;
            width: 100%;
            height: 100%;
            align-items: center;
            justify-content: center;
            perspective: 3000px;
            perspective-origin: 50% 50%;
        }}
        
        .magazine-container.active {{
            display: flex;
        }}
        
        .book-wrapper {{
            position: relative;
            transform-style: preserve-3d;
        }}
        
        /* Ombre sous le livre */
        .book-shadow {{
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            height: 40px;
            background: radial-gradient(ellipse at center, rgba(0,0,0,0.4) 0%, transparent 70%);
            filter: blur(15px);
            pointer-events: none;
        }}
        
        .book {{
            position: relative;
            transform-style: preserve-3d;
            display: flex;
        }}
        
        /* Page statique */
        .book-page {{
            position: relative;
            background: #fff;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
        }}
        
        .book-page img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            pointer-events: none;
        }}
        
        .book-page.left {{
            border-radius: 5px 0 0 5px;
            transform-origin: right center;
        }}
        
        .book-page.right {{
            border-radius: 0 5px 5px 0;
            transform-origin: left center;
        }}
        
        /* Effet de reliure */
        .book-page.left::after {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 40px;
            height: 100%;
            background: linear-gradient(to left, 
                rgba(0,0,0,0.2) 0%, 
                rgba(0,0,0,0.1) 20%,
                rgba(0,0,0,0.05) 40%,
                transparent 100%);
            pointer-events: none;
        }}
        
        .book-page.right::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 40px;
            height: 100%;
            background: linear-gradient(to right, 
                rgba(0,0,0,0.2) 0%, 
                rgba(0,0,0,0.1) 20%,
                rgba(0,0,0,0.05) 40%,
                transparent 100%);
            pointer-events: none;
            z-index: 2;
        }}
        
        /* Canvas pour l'animation de page */
        #pageFlipCanvas {{
            position: absolute;
            top: 0;
            left: 0;
            pointer-events: none;
            z-index: 100;
        }}
        
        /* Zones interactives */
        .flip-zone {{
            position: absolute;
            top: 0;
            width: 100px;
            height: 100%;
            cursor: pointer;
            z-index: 50;
        }}
        
        .flip-zone.left {{
            left: 0;
            cursor: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%23ffffff" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>') 12 12, w-resize;
        }}
        
        .flip-zone.right {{
            right: 0;
            cursor: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%23ffffff" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>') 12 12, e-resize;
        }}
        
        /* Coin de page (hover effect) */
        .page-corner {{
            position: absolute;
            width: 60px;
            height: 60px;
            z-index: 60;
            pointer-events: none;
            transition: transform 0.2s ease;
        }}
        
        .page-corner.bottom-right {{
            bottom: 0;
            right: 0;
            background: linear-gradient(135deg, transparent 50%, rgba(0,0,0,0.1) 50%);
            transform-origin: bottom right;
            transform: scale(0);
            border-radius: 0 0 5px 0;
        }}
        
        .page-corner.bottom-left {{
            bottom: 0;
            left: 0;
            background: linear-gradient(-135deg, transparent 50%, rgba(0,0,0,0.1) 50%);
            transform-origin: bottom left;
            transform: scale(0);
            border-radius: 0 0 0 5px;
        }}
        
        .book-page.right:hover .page-corner.bottom-right,
        .book-page.left:hover .page-corner.bottom-left {{
            transform: scale(1);
        }}
        
        /* Drag zone pour tourner avec la souris */
        .drag-corner {{
            position: absolute;
            width: 80px;
            height: 80px;
            z-index: 70;
            cursor: grab;
        }}
        
        .drag-corner:active {{
            cursor: grabbing;
        }}
        
        .drag-corner.bottom-right {{
            bottom: 0;
            right: 0;
        }}
        
        .drag-corner.bottom-left {{
            bottom: 0;
            left: 0;
        }}
        
        .drag-corner.top-right {{
            top: 0;
            right: 0;
        }}
        
        .drag-corner.top-left {{
            top: 0;
            left: 0;
        }}
        
        /* Hotspots */
        .hotspot {{
            position: absolute;
            background: rgba(59, 130, 246, 0.15);
            border: 2px solid rgba(59, 130, 246, 0.5);
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            z-index: 10;
        }}
        
        .hotspot:hover {{
            background: rgba(59, 130, 246, 0.3);
            border-color: var(--accent);
        }}
        
        /* Controls */
        .controls {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem;
            background: var(--surface);
            border-top: 1px solid var(--border);
            flex-shrink: 0;
        }}
        
        .nav-group {{ display: flex; align-items: center; gap: 0.25rem; }}
        
        .page-info {{
            font-size: 0.85rem;
            color: var(--text-muted);
            min-width: 100px;
            text-align: center;
            font-variant-numeric: tabular-nums;
        }}
        
        .divider {{ width: 1px; height: 24px; background: var(--border); }}
        
        .swiper-button-next, .swiper-button-prev, .swiper-pagination {{ display: none; }}
        
        /* Sound toggle */
        .sound-toggle {{
            position: relative;
        }}
        
        .sound-toggle.muted svg {{
            opacity: 0.4;
        }}
        
        @media (max-width: 768px) {{
            .header {{ padding: 0.5rem 1rem; }}
            .controls {{ gap: 0.5rem; padding: 0.5rem; }}
            .btn {{ width: 32px; height: 32px; }}
            .btn svg {{ width: 16px; height: 16px; }}
            .page-info {{ font-size: 0.75rem; min-width: 80px; }}
            .divider {{ display: none; }}
            .mode-btn span {{ display: none; }}
            .flip-zone {{ width: 60px; }}
            .drag-corner {{ width: 50px; height: 50px; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="/" class="logo">
            <svg viewBox="0 0 24 24"><path d="M6 2a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6H6zm7 1.5L18.5 9H13V3.5zM8 12h8v2H8v-2zm0 4h8v2H8v-2z"/></svg>
            FlipBook
        </a>
        <div class="header-actions">
            <div class="mode-selector">
                <button class="mode-btn" id="modeBtn">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                        <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                    </svg>
                    <span id="currentMode">{self.MODES.get(self.mode, 'Standard')}</span>
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M6 9l6 6 6-6"/>
                    </svg>
                </button>
                <div class="mode-dropdown" id="modeDropdown">
{mode_options}
                </div>
            </div>
            <button class="btn sound-toggle" id="soundToggle" title="Son">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                    <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
                    <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
                </svg>
            </button>
            <button class="btn" id="fullscreenBtn" title="Plein écran">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
                </svg>
            </button>
        </div>
    </header>
    
    <div class="viewer">
        <!-- Swiper -->
        <div class="swiper-container" id="swiperContainer">
            <div class="swiper" id="viewer">
                <div class="swiper-wrapper">
{swiper_pages}
                </div>
            </div>
        </div>
        
        <!-- Magazine -->
        <div class="magazine-container" id="magazineContainer">
            <div class="book-wrapper" id="bookWrapper">
                <div class="book-shadow"></div>
                <div class="book" id="book"></div>
                <canvas id="pageFlipCanvas"></canvas>
            </div>
        </div>
    </div>
    
    <div class="controls">
        <div class="nav-group">
            <button class="btn" id="firstBtn" title="Première page">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 19l-7-7 7-7M18 19l-7-7 7-7"/>
                </svg>
            </button>
            <button class="btn" id="prevBtn" title="Page précédente">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M15 19l-7-7 7-7"/>
                </svg>
            </button>
        </div>
        
        <span class="page-info"><span id="current">1</span> / {self.pages_count}</span>
        
        <div class="nav-group">
            <button class="btn" id="nextBtn" title="Page suivante">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 5l7 7-7 7"/>
                </svg>
            </button>
            <button class="btn" id="lastBtn" title="Dernière page">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M13 5l7 7-7 7M6 5l7 7-7 7"/>
                </svg>
            </button>
        </div>
        
        <div class="divider"></div>
        
        <div class="nav-group">
            <button class="btn" id="zoomOutBtn" title="Zoom -">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35M8 11h6"/>
                </svg>
            </button>
            <button class="btn" id="zoomInBtn" title="Zoom +">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35M11 8v6M8 11h6"/>
                </svg>
            </button>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
    (function() {{
        'use strict';
        
        // ========================================
        // CONFIGURATION
        // ========================================
        const CONFIG = {{
            TOTAL: {self.pages_count},
            ID: "{self.flipbook_id}",
            DEFAULT_MODE: "{self.mode}",
            HOTSPOTS: {hotspots_json}
        }};
        
        // ========================================
        // STATE
        // ========================================
        const state = {{
            currentMode: null,
            currentPage: 1,
            zoom: 1,
            swiper: null,
            
            // Magazine specific
            isLandscape: false,
            pageWidth: 0,
            pageHeight: 0,
            pagesLoaded: [],
            
            // Animation
            isAnimating: false,
            isDragging: false,
            dragStartX: 0,
            dragStartY: 0,
            dragProgress: 0,
            dragCorner: null,
            
            // Sound
            soundEnabled: true
        }};
        
        // ========================================
        // DOM ELEMENTS
        // ========================================
        const $ = id => document.getElementById(id);
        const $$ = sel => document.querySelectorAll(sel);
        
        const elements = {{
            swiperContainer: $('swiperContainer'),
            magazineContainer: $('magazineContainer'),
            bookWrapper: $('bookWrapper'),
            book: $('book'),
            canvas: $('pageFlipCanvas'),
            currentDisplay: $('current'),
            soundToggle: $('soundToggle')
        }};
        
        let ctx = elements.canvas.getContext('2d');
        
        // ========================================
        // AUDIO - Son de page qui tourne
        // ========================================
        const AudioManager = {{
            context: null,
            
            init() {{
                try {{
                    this.context = new (window.AudioContext || window.webkitAudioContext)();
                }} catch(e) {{
                    console.log('Audio not supported');
                }}
            }},
            
            playPageTurn() {{
                if (!this.context || !state.soundEnabled) return;
                
                // Créer un son de page qui tourne synthétique
                const duration = 0.4;
                const now = this.context.currentTime;
                
                // Bruit blanc filtré pour simuler le froissement du papier
                const bufferSize = this.context.sampleRate * duration;
                const buffer = this.context.createBuffer(1, bufferSize, this.context.sampleRate);
                const data = buffer.getChannelData(0);
                
                for (let i = 0; i < bufferSize; i++) {{
                    const t = i / bufferSize;
                    // Enveloppe qui monte puis descend
                    const envelope = Math.sin(t * Math.PI) * 0.3;
                    // Bruit avec plus de basses fréquences
                    data[i] = (Math.random() * 2 - 1) * envelope;
                }}
                
                const source = this.context.createBufferSource();
                source.buffer = buffer;
                
                // Filtre passe-bas pour un son plus doux
                const filter = this.context.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.setValueAtTime(2000, now);
                filter.frequency.linearRampToValueAtTime(800, now + duration);
                
                // Gain
                const gainNode = this.context.createGain();
                gainNode.gain.setValueAtTime(0.15, now);
                gainNode.gain.linearRampToValueAtTime(0, now + duration);
                
                source.connect(filter);
                filter.connect(gainNode);
                gainNode.connect(this.context.destination);
                
                source.start(now);
            }}
        }};
        
        // ========================================
        // SWIPER
        // ========================================
        const swiperConfigs = {{
            default: {{
                slidesPerView: 1,
                spaceBetween: 30,
                keyboard: {{ enabled: true }},
                mousewheel: {{ forceToAxis: true }}
            }},
            coverflow: {{
                effect: 'coverflow',
                grabCursor: true,
                centeredSlides: true,
                slidesPerView: 'auto',
                coverflowEffect: {{ rotate: 50, stretch: 0, depth: 100, modifier: 1, slideShadows: true }},
                keyboard: {{ enabled: true }}
            }},
            cards: {{
                effect: 'cards',
                grabCursor: true,
                keyboard: {{ enabled: true }}
            }},
            cube: {{
                effect: 'cube',
                grabCursor: true,
                cubeEffect: {{ shadow: true, slideShadows: true, shadowOffset: 20, shadowScale: 0.94 }},
                keyboard: {{ enabled: true }}
            }},
            flip: {{
                effect: 'flip',
                grabCursor: true,
                keyboard: {{ enabled: true }}
            }},
            fade: {{
                effect: 'fade',
                fadeEffect: {{ crossFade: true }},
                keyboard: {{ enabled: true }}
            }}
        }};
        
        function initSwiper(mode) {{
            const idx = state.swiper ? state.swiper.activeIndex : (state.currentPage - 1);
            if (state.swiper) state.swiper.destroy(true, true);
            
            $('viewer').className = 'swiper mode-' + mode;
            
            state.swiper = new Swiper('#viewer', {{
                ...swiperConfigs[mode],
                on: {{ 
                    slideChange: () => {{ 
                        state.currentPage = state.swiper.activeIndex + 1; 
                        updateUI(); 
                    }} 
                }}
            }});
            
            if (idx > 0) state.swiper.slideTo(idx, 0);
        }}
        
        // ========================================
        // MAGAZINE - Core
        // ========================================
        function getPageSrc(num) {{
            if (num < 1 || num > CONFIG.TOTAL) return null;
            return `/view/${{CONFIG.ID}}/pages/page_${{num}}.jpg`;
        }}
        
        async function loadImage(src) {{
            return new Promise((resolve, reject) => {{
                const img = new Image();
                img.onload = () => resolve(img);
                img.onerror = reject;
                img.src = src;
            }});
        }}
        
        async function detectPageFormat() {{
            try {{
                const img = await loadImage(getPageSrc(1));
                const ratio = img.naturalWidth / img.naturalHeight;
                state.isLandscape = ratio > 1.2;
                return {{ width: img.naturalWidth, height: img.naturalHeight, ratio }};
            }} catch(e) {{
                state.isLandscape = false;
                return {{ width: 800, height: 1000, ratio: 0.8 }};
            }}
        }}
        
        function calculatePageSize(pageInfo) {{
            const container = elements.magazineContainer;
            const maxHeight = container.clientHeight - 60;
            const maxWidth = container.clientWidth - 60;
            
            if (state.isLandscape) {{
                // Mode single page
                if (maxWidth * 0.9 / pageInfo.ratio <= maxHeight) {{
                    state.pageWidth = Math.floor(maxWidth * 0.85);
                    state.pageHeight = Math.floor(state.pageWidth / pageInfo.ratio);
                }} else {{
                    state.pageHeight = Math.floor(maxHeight * 0.95);
                    state.pageWidth = Math.floor(state.pageHeight * pageInfo.ratio);
                }}
            }} else {{
                // Mode double page
                const availableWidth = maxWidth * 0.95;
                const singleWidth = availableWidth / 2;
                
                if (singleWidth / pageInfo.ratio <= maxHeight) {{
                    state.pageWidth = Math.floor(singleWidth);
                    state.pageHeight = Math.floor(state.pageWidth / pageInfo.ratio);
                }} else {{
                    state.pageHeight = Math.floor(maxHeight * 0.95);
                    state.pageWidth = Math.floor(state.pageHeight * pageInfo.ratio);
                }}
            }}
        }}
        
        async function preloadPages() {{
            // Précharger toutes les images
            const promises = [];
            for (let i = 1; i <= CONFIG.TOTAL; i++) {{
                promises.push(
                    loadImage(getPageSrc(i))
                        .then(img => {{ state.pagesLoaded[i] = img; }})
                        .catch(() => {{ state.pagesLoaded[i] = null; }})
                );
            }}
            await Promise.all(promises);
        }}
        
        // ========================================
        // MAGAZINE - Rendering
        // ========================================
        function getCurrentSpread() {{
            if (state.isLandscape) {{
                return {{ left: state.currentPage, right: null }};
            }} else {{
                const leftPage = state.currentPage % 2 === 1 ? state.currentPage : state.currentPage - 1;
                return {{
                    left: leftPage,
                    right: leftPage + 1 <= CONFIG.TOTAL ? leftPage + 1 : null
                }};
            }}
        }}
        
        function renderBook() {{
            const spread = getCurrentSpread();
            const book = elements.book;
            
            if (state.isLandscape) {{
                // Single page mode
                book.innerHTML = `
                    <div class="book-page single" style="width:${{state.pageWidth}}px;height:${{state.pageHeight}}px;">
                        <img src="${{getPageSrc(spread.left)}}" alt="Page ${{spread.left}}">
                        <div class="page-corner bottom-right"></div>
                        <div class="page-corner bottom-left"></div>
                        <div class="drag-corner bottom-right" data-corner="br" data-direction="next"></div>
                        <div class="drag-corner bottom-left" data-corner="bl" data-direction="prev"></div>
                        <div class="drag-corner top-right" data-corner="tr" data-direction="next"></div>
                        <div class="drag-corner top-left" data-corner="tl" data-direction="prev"></div>
                        <div class="flip-zone right" data-direction="next"></div>
                        <div class="flip-zone left" data-direction="prev"></div>
                    </div>
                `;
            }} else {{
                // Double page mode
                book.innerHTML = `
                    <div class="book-page left" style="width:${{state.pageWidth}}px;height:${{state.pageHeight}}px;">
                        ${{spread.left ? `<img src="${{getPageSrc(spread.left)}}" alt="Page ${{spread.left}}">` : ''}}
                        <div class="page-corner bottom-left"></div>
                        <div class="drag-corner bottom-left" data-corner="bl" data-direction="prev"></div>
                        <div class="drag-corner top-left" data-corner="tl" data-direction="prev"></div>
                        <div class="flip-zone left" data-direction="prev"></div>
                    </div>
                    <div class="book-page right" style="width:${{state.pageWidth}}px;height:${{state.pageHeight}}px;">
                        ${{spread.right ? `<img src="${{getPageSrc(spread.right)}}" alt="Page ${{spread.right}}">` : ''}}
                        <div class="page-corner bottom-right"></div>
                        <div class="drag-corner bottom-right" data-corner="br" data-direction="next"></div>
                        <div class="drag-corner top-right" data-corner="tr" data-direction="next"></div>
                        <div class="flip-zone right" data-direction="next"></div>
                    </div>
                `;
            }}
            
            // Setup canvas
            const totalWidth = state.isLandscape ? state.pageWidth : state.pageWidth * 2;
            elements.canvas.width = totalWidth;
            elements.canvas.height = state.pageHeight;
            elements.canvas.style.width = totalWidth + 'px';
            elements.canvas.style.height = state.pageHeight + 'px';
            
            // Bind interactions
            bindDragEvents();
            bindClickEvents();
            
            updateUI();
        }}
        
        // ========================================
        // MAGAZINE - Page Turn Animation
        // ========================================
        function animatePageTurn(direction, fromDrag = false, startProgress = 0) {{
            if (state.isAnimating && !fromDrag) return;
            
            const spread = getCurrentSpread();
            let canTurn = false;
            let turningPageNum, nextPageNum, underPageNum;
            
            if (state.isLandscape) {{
                if (direction === 'next' && state.currentPage < CONFIG.TOTAL) {{
                    canTurn = true;
                    turningPageNum = state.currentPage;
                    nextPageNum = state.currentPage + 1;
                }} else if (direction === 'prev' && state.currentPage > 1) {{
                    canTurn = true;
                    turningPageNum = state.currentPage;
                    nextPageNum = state.currentPage - 1;
                }}
            }} else {{
                if (direction === 'next' && spread.right && spread.right < CONFIG.TOTAL) {{
                    canTurn = true;
                    turningPageNum = spread.right;
                    nextPageNum = spread.right + 1;
                    underPageNum = spread.right + 2;
                }} else if (direction === 'prev' && spread.left > 1) {{
                    canTurn = true;
                    turningPageNum = spread.left;
                    nextPageNum = spread.left - 1;
                    underPageNum = spread.left - 2;
                }}
            }}
            
            if (!canTurn) return;
            
            state.isAnimating = true;
            AudioManager.playPageTurn();
            
            const turningImage = state.pagesLoaded[turningPageNum];
            const nextImage = state.pagesLoaded[nextPageNum];
            const underImage = underPageNum ? state.pagesLoaded[underPageNum] : null;
            
            let progress = startProgress;
            const duration = fromDrag ? 400 * (1 - startProgress) : 600;
            const startTime = performance.now();
            
            function animate(currentTime) {{
                const elapsed = currentTime - startTime;
                
                if (fromDrag) {{
                    progress = startProgress + (1 - startProgress) * Math.min(elapsed / duration, 1);
                }} else {{
                    progress = easeInOutCubic(Math.min(elapsed / duration, 1));
                }}
                
                drawPageTurn(direction, progress, turningImage, nextImage, underImage);
                
                if (progress < 1) {{
                    requestAnimationFrame(animate);
                }} else {{
                    finishPageTurn(direction);
                }}
            }}
            
            requestAnimationFrame(animate);
        }}
        
        function drawPageTurn(direction, progress, turningImage, nextImage, underImage) {{
            const w = state.pageWidth;
            const h = state.pageHeight;
            const isDouble = !state.isLandscape;
            
            ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
            
            if (isDouble) {{
                // Double page mode
                if (direction === 'next') {{
                    // Page de droite qui tourne vers la gauche
                    const foldX = w + w * (1 - progress);
                    const angle = progress * Math.PI;
                    
                    // Page du dessous (nouvelle page droite)
                    if (underImage) {{
                        ctx.save();
                        ctx.beginPath();
                        ctx.rect(w, 0, w, h);
                        ctx.clip();
                        ctx.drawImage(underImage, w, 0, w, h);
                        
                        // Ombre sur la page du dessous
                        const shadowIntensity = Math.sin(progress * Math.PI) * 0.4;
                        ctx.fillStyle = `rgba(0,0,0,${{shadowIntensity}})`;
                        ctx.fillRect(w, 0, w * (1 - progress) + 20, h);
                        ctx.restore();
                    }}
                    
                    // Page qui tourne - face avant
                    if (progress < 0.5 && turningImage) {{
                        ctx.save();
                        ctx.beginPath();
                        ctx.moveTo(foldX, 0);
                        ctx.lineTo(w * 2, 0);
                        ctx.lineTo(w * 2, h);
                        ctx.lineTo(foldX, h);
                        ctx.closePath();
                        ctx.clip();
                        
                        ctx.translate(foldX, 0);
                        ctx.scale((1 - progress * 2) || 0.01, 1);
                        ctx.translate(-foldX, 0);
                        ctx.drawImage(turningImage, w, 0, w, h);
                        
                        // Ombre sur la page qui tourne
                        const gradient = ctx.createLinearGradient(foldX - 50, 0, foldX, 0);
                        gradient.addColorStop(0, 'rgba(0,0,0,0)');
                        gradient.addColorStop(1, `rgba(0,0,0,${{0.3 * (1 - progress * 2)}})`);
                        ctx.fillStyle = gradient;
                        ctx.fillRect(w, 0, w, h);
                        
                        ctx.restore();
                    }}
                    
                    // Page qui tourne - face arrière
                    if (progress >= 0.5 && nextImage) {{
                        ctx.save();
                        const backFoldX = w - (w * (progress - 0.5) * 2);
                        
                        ctx.beginPath();
                        ctx.moveTo(0, 0);
                        ctx.lineTo(backFoldX, 0);
                        ctx.lineTo(backFoldX, h);
                        ctx.lineTo(0, h);
                        ctx.closePath();
                        ctx.clip();
                        
                        ctx.translate(backFoldX, 0);
                        ctx.scale(-((progress - 0.5) * 2) || 0.01, 1);
                        ctx.translate(-backFoldX, 0);
                        ctx.drawImage(nextImage, 0, 0, w, h);
                        
                        // Ombre
                        const gradient = ctx.createLinearGradient(backFoldX, 0, backFoldX + 50, 0);
                        gradient.addColorStop(0, `rgba(0,0,0,${{0.3 * ((progress - 0.5) * 2)}})`);
                        gradient.addColorStop(1, 'rgba(0,0,0,0)');
                        ctx.fillStyle = gradient;
                        ctx.fillRect(0, 0, w, h);
                        
                        ctx.restore();
                    }}
                    
                    // Pli central (ombre de reliure)
                    ctx.save();
                    const spineGradient = ctx.createLinearGradient(w - 20, 0, w + 20, 0);
                    spineGradient.addColorStop(0, 'rgba(0,0,0,0)');
                    spineGradient.addColorStop(0.5, 'rgba(0,0,0,0.2)');
                    spineGradient.addColorStop(1, 'rgba(0,0,0,0)');
                    ctx.fillStyle = spineGradient;
                    ctx.fillRect(w - 20, 0, 40, h);
                    ctx.restore();
                    
                }} else {{
                    // Page de gauche qui tourne vers la droite (direction === 'prev')
                    const foldX = w * progress;
                    
                    // Page du dessous (nouvelle page gauche)
                    if (underImage) {{
                        ctx.save();
                        ctx.beginPath();
                        ctx.rect(0, 0, w, h);
                        ctx.clip();
                        ctx.drawImage(underImage, 0, 0, w, h);
                        
                        const shadowIntensity = Math.sin(progress * Math.PI) * 0.4;
                        ctx.fillStyle = `rgba(0,0,0,${{shadowIntensity}})`;
                        ctx.fillRect(w * progress - 20, 0, w * (1 - progress) + 20, h);
                        ctx.restore();
                    }}
                    
                    // Page qui tourne - face avant
                    if (progress < 0.5 && turningImage) {{
                        ctx.save();
                        ctx.beginPath();
                        ctx.moveTo(0, 0);
                        ctx.lineTo(foldX, 0);
                        ctx.lineTo(foldX, h);
                        ctx.lineTo(0, h);
                        ctx.closePath();
                        ctx.clip();
                        
                        ctx.translate(foldX, 0);
                        ctx.scale((1 - progress * 2) || 0.01, 1);
                        ctx.translate(-foldX, 0);
                        ctx.drawImage(turningImage, 0, 0, w, h);
                        
                        const gradient = ctx.createLinearGradient(foldX, 0, foldX + 50, 0);
                        gradient.addColorStop(0, `rgba(0,0,0,${{0.3 * (1 - progress * 2)}})`);
                        gradient.addColorStop(1, 'rgba(0,0,0,0)');
                        ctx.fillStyle = gradient;
                        ctx.fillRect(0, 0, w, h);
                        
                        ctx.restore();
                    }}
                    
                    // Face arrière
                    if (progress >= 0.5 && nextImage) {{
                        ctx.save();
                        const backFoldX = w + (w * (progress - 0.5) * 2);
                        
                        ctx.beginPath();
                        ctx.moveTo(w, 0);
                        ctx.lineTo(backFoldX, 0);
                        ctx.lineTo(backFoldX, h);
                        ctx.lineTo(w, h);
                        ctx.closePath();
                        ctx.clip();
                        
                        ctx.translate(backFoldX, 0);
                        ctx.scale(-((progress - 0.5) * 2) || 0.01, 1);
                        ctx.translate(-backFoldX, 0);
                        ctx.drawImage(nextImage, w, 0, w, h);
                        
                        const gradient = ctx.createLinearGradient(backFoldX - 50, 0, backFoldX, 0);
                        gradient.addColorStop(0, 'rgba(0,0,0,0)');
                        gradient.addColorStop(1, `rgba(0,0,0,${{0.3 * ((progress - 0.5) * 2)}})`);
                        ctx.fillStyle = gradient;
                        ctx.fillRect(w, 0, w, h);
                        
                        ctx.restore();
                    }}
                    
                    // Pli central
                    ctx.save();
                    const spineGradient = ctx.createLinearGradient(w - 20, 0, w + 20, 0);
                    spineGradient.addColorStop(0, 'rgba(0,0,0,0)');
                    spineGradient.addColorStop(0.5, 'rgba(0,0,0,0.2)');
                    spineGradient.addColorStop(1, 'rgba(0,0,0,0)');
                    ctx.fillStyle = spineGradient;
                    ctx.fillRect(w - 20, 0, 40, h);
                    ctx.restore();
                }}
            }} else {{
                // Single page mode (landscape)
                if (direction === 'next') {{
                    const foldX = w * (1 - progress);
                    
                    // Page du dessous
                    if (nextImage) {{
                        ctx.drawImage(nextImage, 0, 0, w, h);
                        const shadowIntensity = Math.sin(progress * Math.PI) * 0.5;
                        ctx.fillStyle = `rgba(0,0,0,${{shadowIntensity}})`;
                        ctx.fillRect(0, 0, foldX + 20, h);
                    }}
                    
                    // Page qui tourne
                    if (progress < 0.5 && turningImage) {{
                        ctx.save();
                        ctx.beginPath();
                        ctx.moveTo(foldX, 0);
                        ctx.lineTo(w, 0);
                        ctx.lineTo(w, h);
                        ctx.lineTo(foldX, h);
                        ctx.closePath();
                        ctx.clip();
                        
                        const scaleX = Math.max(0.01, 1 - progress * 2);
                        ctx.translate(foldX, 0);
                        ctx.scale(scaleX, 1);
                        ctx.translate(-foldX, 0);
                        ctx.drawImage(turningImage, 0, 0, w, h);
                        
                        ctx.restore();
                    }}
                }} else {{
                    const foldX = w * progress;
                    
                    // Page du dessous
                    if (nextImage) {{
                        ctx.drawImage(nextImage, 0, 0, w, h);
                        const shadowIntensity = Math.sin(progress * Math.PI) * 0.5;
                        ctx.fillStyle = `rgba(0,0,0,${{shadowIntensity}})`;
                        ctx.fillRect(foldX - 20, 0, w - foldX + 20, h);
                    }}
                    
                    // Page qui tourne
                    if (progress < 0.5 && turningImage) {{
                        ctx.save();
                        ctx.beginPath();
                        ctx.moveTo(0, 0);
                        ctx.lineTo(foldX, 0);
                        ctx.lineTo(foldX, h);
                        ctx.lineTo(0, h);
                        ctx.closePath();
                        ctx.clip();
                        
                        const scaleX = Math.max(0.01, 1 - progress * 2);
                        ctx.translate(foldX, 0);
                        ctx.scale(scaleX, 1);
                        ctx.translate(-foldX, 0);
                        ctx.drawImage(turningImage, 0, 0, w, h);
                        
                        ctx.restore();
                    }}
                }}
            }}
        }}
        
        function finishPageTurn(direction) {{
            ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
            
            if (state.isLandscape) {{
                state.currentPage += direction === 'next' ? 1 : -1;
            }} else {{
                state.currentPage += direction === 'next' ? 2 : -2;
                // Ajuster pour rester sur une page impaire
                if (state.currentPage < 1) state.currentPage = 1;
                if (state.currentPage > CONFIG.TOTAL) state.currentPage = CONFIG.TOTAL;
                if (state.currentPage % 2 === 0) state.currentPage--;
            }}
            
            state.isAnimating = false;
            renderBook();
        }}
        
        function easeInOutCubic(t) {{
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }}
        
        // ========================================
        // MAGAZINE - Drag Interaction
        // ========================================
        function bindDragEvents() {{
            const dragCorners = elements.book.querySelectorAll('.drag-corner');
            
            dragCorners.forEach(corner => {{
                corner.addEventListener('mousedown', startDrag);
                corner.addEventListener('touchstart', startDrag, {{ passive: false }});
            }});
        }}
        
        function startDrag(e) {{
            if (state.isAnimating) return;
            e.preventDefault();
            
            const touch = e.touches ? e.touches[0] : e;
            state.isDragging = true;
            state.dragStartX = touch.clientX;
            state.dragStartY = touch.clientY;
            state.dragCorner = e.currentTarget.dataset.corner;
            state.dragDirection = e.currentTarget.dataset.direction;
            state.dragProgress = 0;
            
            document.addEventListener('mousemove', onDrag);
            document.addEventListener('mouseup', endDrag);
            document.addEventListener('touchmove', onDrag, {{ passive: false }});
            document.addEventListener('touchend', endDrag);
        }}
        
        function onDrag(e) {{
            if (!state.isDragging) return;
            e.preventDefault();
            
            const touch = e.touches ? e.touches[0] : e;
            const deltaX = touch.clientX - state.dragStartX;
            const maxDrag = state.pageWidth;
            
            let progress;
            if (state.dragDirection === 'next') {{
                progress = Math.max(0, Math.min(1, -deltaX / maxDrag));
            }} else {{
                progress = Math.max(0, Math.min(1, deltaX / maxDrag));
            }}
            
            state.dragProgress = progress;
            
            // Dessiner l'aperçu du pli
            drawDragPreview(state.dragDirection, progress);
        }}
        
        function drawDragPreview(direction, progress) {{
            if (progress < 0.02) {{
                ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
                return;
            }}
            
            const spread = getCurrentSpread();
            let turningImage, nextImage, underImage;
            
            if (state.isLandscape) {{
                if (direction === 'next') {{
                    turningImage = state.pagesLoaded[state.currentPage];
                    nextImage = state.pagesLoaded[state.currentPage + 1];
                }} else {{
                    turningImage = state.pagesLoaded[state.currentPage];
                    nextImage = state.pagesLoaded[state.currentPage - 1];
                }}
            }} else {{
                if (direction === 'next') {{
                    turningImage = state.pagesLoaded[spread.right];
                    nextImage = state.pagesLoaded[spread.right + 1];
                    underImage = state.pagesLoaded[spread.right + 2];
                }} else {{
                    turningImage = state.pagesLoaded[spread.left];
                    nextImage = state.pagesLoaded[spread.left - 1];
                    underImage = state.pagesLoaded[spread.left - 2];
                }}
            }}
            
            drawPageTurn(direction, progress * 0.5, turningImage, nextImage, underImage);
        }}
        
        function endDrag(e) {{
            if (!state.isDragging) return;
            
            document.removeEventListener('mousemove', onDrag);
            document.removeEventListener('mouseup', endDrag);
            document.removeEventListener('touchmove', onDrag);
            document.removeEventListener('touchend', endDrag);
            
            const progress = state.dragProgress;
            state.isDragging = false;
            
            if (progress > 0.3) {{
                // Compléter l'animation
                animatePageTurn(state.dragDirection, true, progress * 0.5);
            }} else {{
                // Annuler - retourner à la position initiale
                cancelDrag(state.dragDirection, progress * 0.5);
            }}
        }}
        
        function cancelDrag(direction, startProgress) {{
            const duration = 300 * startProgress;
            const startTime = performance.now();
            
            const spread = getCurrentSpread();
            let turningImage, nextImage, underImage;
            
            if (state.isLandscape) {{
                turningImage = state.pagesLoaded[state.currentPage];
                nextImage = direction === 'next' ? 
                    state.pagesLoaded[state.currentPage + 1] : 
                    state.pagesLoaded[state.currentPage - 1];
            }} else {{
                if (direction === 'next') {{
                    turningImage = state.pagesLoaded[spread.right];
                    nextImage = state.pagesLoaded[spread.right + 1];
                    underImage = state.pagesLoaded[spread.right + 2];
                }} else {{
                    turningImage = state.pagesLoaded[spread.left];
                    nextImage = state.pagesLoaded[spread.left - 1];
                    underImage = state.pagesLoaded[spread.left - 2];
                }}
            }}
            
            function animate(currentTime) {{
                const elapsed = currentTime - startTime;
                const t = Math.min(elapsed / duration, 1);
                const progress = startProgress * (1 - easeInOutCubic(t));
                
                if (progress > 0.01) {{
                    drawPageTurn(direction, progress, turningImage, nextImage, underImage);
                    requestAnimationFrame(animate);
                }} else {{
                    ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
                }}
            }}
            
            requestAnimationFrame(animate);
        }}
        
        // ========================================
        // MAGAZINE - Click Events
        // ========================================
        function bindClickEvents() {{
            const flipZones = elements.book.querySelectorAll('.flip-zone');
            
            flipZones.forEach(zone => {{
                zone.addEventListener('click', (e) => {{
                    if (state.isDragging) return;
                    const direction = zone.dataset.direction;
                    animatePageTurn(direction);
                }});
            }});
        }}
        
        // ========================================
        // MAGAZINE - Init
        // ========================================
        async function initMagazine() {{
            elements.book.innerHTML = '<div style="color:#888;padding:20px;">Chargement...</div>';
            
            const pageInfo = await detectPageFormat();
            calculatePageSize(pageInfo);
            await preloadPages();
            
            // Ajuster pour démarrer sur une page impaire en mode double
            if (!state.isLandscape && state.currentPage % 2 === 0) {{
                state.currentPage--;
            }}
            
            renderBook();
        }}
        
        // ========================================
        // MODE SWITCHING
        // ========================================
        const modeNames = {{
            default: 'Standard',
            magazine: 'Magazine',
            coverflow: 'Coverflow',
            cards: 'Cartes',
            cube: 'Cube',
            flip: 'Flip',
            fade: 'Fondu'
        }};
        
        function changeMode(mode) {{
            if (state.currentMode === mode) return;
            
            // Sauvegarder la page actuelle
            if (state.swiper) {{
                state.currentPage = state.swiper.activeIndex + 1;
            }}
            
            state.currentMode = mode;
            
            // Mettre à jour l'UI
            $('currentMode').textContent = modeNames[mode];
            $$('.mode-option').forEach(opt => {{
                opt.classList.toggle('active', opt.dataset.mode === mode);
            }});
            $('modeDropdown').classList.remove('open');
            
            if (mode === 'magazine') {{
                elements.swiperContainer.style.display = 'none';
                elements.magazineContainer.classList.add('active');
                if (state.swiper) {{
                    state.swiper.destroy(true, true);
                    state.swiper = null;
                }}
                initMagazine();
            }} else {{
                elements.magazineContainer.classList.remove('active');
                elements.swiperContainer.style.display = '';
                ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
                initSwiper(mode);
                if (state.currentPage > 1 && state.swiper) {{
                    state.swiper.slideTo(state.currentPage - 1, 0);
                }}
            }}
            
            updateUI();
        }}
        
        // ========================================
        // UI & NAVIGATION
        // ========================================
        function updateUI() {{
            let displayText;
            let atStart, atEnd;
            
            if (state.currentMode === 'magazine') {{
                if (state.isLandscape) {{
                    displayText = state.currentPage;
                    atStart = state.currentPage <= 1;
                    atEnd = state.currentPage >= CONFIG.TOTAL;
                }} else {{
                    const spread = getCurrentSpread();
                    displayText = spread.right ? `${{spread.left}}-${{spread.right}}` : spread.left;
                    atStart = spread.left <= 1;
                    atEnd = !spread.right || spread.right >= CONFIG.TOTAL;
                }}
            }} else if (state.swiper) {{
                displayText = state.swiper.activeIndex + 1;
                atStart = state.swiper.activeIndex === 0;
                atEnd = state.swiper.activeIndex >= CONFIG.TOTAL - 1;
            }} else {{
                displayText = state.currentPage;
                atStart = state.currentPage <= 1;
                atEnd = state.currentPage >= CONFIG.TOTAL;
            }}
            
            elements.currentDisplay.textContent = displayText;
            $('firstBtn').disabled = $('prevBtn').disabled = atStart;
            $('nextBtn').disabled = $('lastBtn').disabled = atEnd;
        }}
        
        function goToPage(page) {{
            page = Math.max(1, Math.min(CONFIG.TOTAL, page));
            
            if (state.currentMode === 'magazine') {{
                if (!state.isLandscape && page % 2 === 0) page--;
                state.currentPage = page;
                renderBook();
            }} else if (state.swiper) {{
                state.swiper.slideTo(page - 1);
            }}
            
            updateUI();
        }}
        
        function nextPage() {{
            if (state.currentMode === 'magazine') {{
                animatePageTurn('next');
            }} else if (state.swiper) {{
                state.swiper.slideNext();
            }}
        }}
        
        function prevPage() {{
            if (state.currentMode === 'magazine') {{
                animatePageTurn('prev');
            }} else if (state.swiper) {{
                state.swiper.slidePrev();
            }}
        }}
        
        function setZoom(z) {{
            state.zoom = Math.max(0.5, Math.min(2, z));
            if (state.currentMode === 'magazine') {{
                elements.bookWrapper.style.transform = `scale(${{state.zoom}})`;
            }} else {{
                $$('.page img').forEach(img => {{
                    img.style.transform = `scale(${{state.zoom}})`;
                }});
            }}
        }}
        
        // ========================================
        // EVENT LISTENERS
        // ========================================
        $('firstBtn').onclick = () => goToPage(1);
        $('prevBtn').onclick = prevPage;
        $('nextBtn').onclick = nextPage;
        $('lastBtn').onclick = () => goToPage(CONFIG.TOTAL);
        $('zoomInBtn').onclick = () => setZoom(state.zoom + 0.25);
        $('zoomOutBtn').onclick = () => setZoom(state.zoom - 0.25);
        
        $('fullscreenBtn').onclick = () => {{
            if (!document.fullscreenElement) document.documentElement.requestFullscreen();
            else document.exitFullscreen();
        }};
        
        $('modeBtn').onclick = e => {{
            e.stopPropagation();
            $('modeDropdown').classList.toggle('open');
        }};
        
        document.addEventListener('click', () => $('modeDropdown').classList.remove('open'));
        
        $$('.mode-option').forEach(opt => {{
            opt.onclick = e => {{
                e.stopPropagation();
                changeMode(opt.dataset.mode);
            }};
        }});
        
        // Sound toggle
        elements.soundToggle.onclick = () => {{
            state.soundEnabled = !state.soundEnabled;
            elements.soundToggle.classList.toggle('muted', !state.soundEnabled);
            if (state.soundEnabled) AudioManager.init();
        }};
        
        // Hotspots
        $$('.hotspot-page').forEach(h => {{
            h.onclick = () => goToPage(parseInt(h.dataset.targetPage));
        }});
        
        // Keyboard
        document.addEventListener('keydown', e => {{
            if (state.isAnimating) return;
            if (e.key === 'ArrowLeft') prevPage();
            if (e.key === 'ArrowRight') nextPage();
            if (e.key === '+' || e.key === '=') setZoom(state.zoom + 0.25);
            if (e.key === '-') setZoom(state.zoom - 0.25);
            if (e.key === '0') setZoom(1);
            if (e.key === 'Home') goToPage(1);
            if (e.key === 'End') goToPage(CONFIG.TOTAL);
        }});
        
        // Resize
        let resizeTimeout;
        window.addEventListener('resize', () => {{
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(async () => {{
                if (state.currentMode === 'magazine') {{
                    const pageInfo = await detectPageFormat();
                    calculatePageSize(pageInfo);
                    renderBook();
                }}
            }}, 250);
        }});
        
        // ========================================
        // INIT
        // ========================================
        AudioManager.init();
        changeMode(CONFIG.DEFAULT_MODE);
        
    }})();
    </script>
</body>
</html>'''


def generate_viewer(flipbook_id, pages_count, output_dir, mode='default', background_color='#0f0f0f', hotspots=None):
    """Fonction principale de génération"""
    generator = FlipbookGenerator(flipbook_id, pages_count, mode, background_color, hotspots)
    viewer_path = os.path.join(output_dir, 'viewer.html')
    success = generator.generate(viewer_path)
    return {"success": success, "viewer_path": viewer_path if success else None}
