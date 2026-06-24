#!/usr/bin/env python3
"""
Génère une preview realistic du dashboard ReviewWatch 
pour la landing page (review.gk365.fr)
"""

from PIL import Image, ImageDraw, ImageFont
import os

W = 1200
H = 800

# Couleurs du design system GK365
BG = (10, 10, 15)
CARD = (18, 18, 31)
BORDER = (30, 30, 50)
GREEN = (74, 222, 128)
CYAN = (34, 211, 238)
TEXT = (224, 224, 224)
TEXT_DIM = (100, 116, 139)
TEXT_WHITE = (255, 255, 255)
STAR_YELLOW = (250, 204, 21)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Polices (fallback si FiraCode absent) ──
try:
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    font_mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except:
    font_bold = ImageFont.load_default()
    font_small = font_bold
    font_tiny = font_bold
    font_big = font_bold
    font_mid = font_bold

# ── Header ──
draw.rectangle([0, 0, W, 60], fill=CARD)
draw.line([0, 60, W, 60], fill=BORDER)

# Logo text
draw.text((30, 16), "★  ReviewWatch", fill=GREEN, font=font_mid)
draw.text((260, 24), "Dashboard", fill=TEXT_DIM, font=font_small)

# Stats en haut
stats_data = [
    ("⭐ 4.8", "Note moyenne"),
    ("📝 342", "Avis traités"),
    ("💬 89%", "Taux de réponse"),
    ("📈 +23%", "Ce mois"),
]
x_start = 600
for label, sub in stats_data:
    draw.text((x_start, 12), label, fill=TEXT_WHITE, font=font_bold)
    draw.text((x_start, 36), sub, fill=TEXT_DIM, font=font_tiny)
    x_start += 140

# ── Section : Avis récents ──
section_y = 80
draw.text((30, section_y), "📋 Avis Google récents", fill=TEXT_WHITE, font=font_bold)
draw.text((500, section_y), "Réponse IA générée", fill=TEXT_DIM, font=font_small)

# Ligne de séparation
draw.line([30, section_y+35, W-30, section_y+35], fill=BORDER)

# ── Un avis ──
def draw_review_card(draw, y, author, rating, text, response, highlight=False):
    card_y = y
    card_h = 105
    bg = (22, 28, 40) if highlight else CARD
    draw.rounded_rectangle([30, card_y, W-30, card_y+card_h], radius=10, fill=bg, outline=BORDER)
    
    # Auteur
    draw.text((50, card_y+14), author, fill=TEXT_WHITE, font=font_bold)
    
    # Étoiles
    stars = "★" * rating + "☆" * (5-rating)
    draw.text((350, card_y+14), stars, fill=STAR_YELLOW, font=font_small)
    
    # Texte de l'avis
    draw.text((50, card_y+40), text[:90], fill=TEXT, font=font_tiny)
    
    # Réponse (à droite)
    draw.text((550, card_y+14), "✅ Réponse envoyée", fill=GREEN, font=font_tiny)
    draw.text((550, card_y+35), response[:80], fill=TEXT_DIM, font=font_tiny)
    
    # Timbre "IA"
    draw.rounded_rectangle([970, card_y+12, 1040, card_y+32], radius=4, fill=(74, 222, 128, 30))
    draw.text((978, card_y+14), "🤖 IA", fill=GREEN, font=font_tiny)

avis = [
    ("Marie L.", 5, "Super restaurant ! Les burger sont incroyables et le service rapide. Je recommande vivement !",
     "Merci Marie pour votre retour ! Toute l'équipe est ravie que vous ayez apprécié nos burgers. À très bientôt ! — Le Chef"),
    ("Thomas D.", 4, "Très bon accueil, cadre agréable. Petit bémol sur l'attente le week-end mais ça vaut le détour.",
     "Merci Thomas pour votre avis ! Nous travaillons à réduire l'attente le week-end. Au plaisir de vous revoir ! — L'équipe"),
    ("Sophie M.", 5, "Découverte formidable, je reviendrai sans hésiter ! Produits frais et personnel attentionné.",
     "Quel plaisir de lire ces mots Sophie ! Toute l'équipe vous remercie et vous attend pour votre prochaine visite. — La Direction"),
    ("Karim B.", 3, "Correct sans plus. La viande était un peu trop cuite à mon goût mais le service était sympa.",
     "Merci Karim pour votre honnêteté ! Nous allons vérifier la cuisson auprès de notre chef. Votre satisfaction est notre priorité. — L'équipe"),
]

for i, (author, rating, text, response) in enumerate(avis):
    y = section_y + 50 + i * 115
    draw_review_card(draw, y, author, rating, text, response, highlight=(i==0))

# ── Footer ──
footer_y = H - 50
draw.line([30, footer_y-10, W-30, footer_y-10], fill=BORDER)
draw.text((30, footer_y), "⚡ Réponses automatiques • IA personnalisée • Alertes WhatsApp", fill=TEXT_DIM, font=font_tiny)
draw.text((850, footer_y), "ReviewWatch — GK365", fill=TEXT_DIM, font=font_tiny)

# ── Sauvegarde en PNG puis conversion WebP ──
png_path = "/home/hermes/business/reviewwatch/landing/dashboard_preview.png"
webp_path = "/home/hermes/business/reviewwatch/landing/dashboard_preview.webp"
img.save(png_path)
print(f"✅ PNG créé : {png_path}")

# Conversion en WebP
img.save(webp_path, "WEBP", quality=85)
size_kb = os.path.getsize(webp_path) / 1024
print(f"✅ WebP créé : {webp_path} ({size_kb:.0f} KB)")
