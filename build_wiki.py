import json
import os
import html
from urllib.parse import urlparse

def get_site_name(url):
    """Extrait un nom lisible à partir de l'URL."""
    try:
        path = urlparse(url).path
        if path and path != "/":
            # On prend la dernière partie du chemin (ex: /DeepFaceLive -> DeepFaceLive)
            name = path.split('/')[-1]
            if not name: # cas où ça finit par /
                name = path.split('/')[-2]
        else:
            # Sinon on prend le nom de domaine (ex: google.com -> Google)
            name = urlparse(url).netloc.replace('www.', '').split('.')[0]
        
        return name.replace('-', ' ').replace('_', ' ').capitalize()
    except:
        return "Lien"

def super_sanitize(text):
    if not text or text == "None":
        return "Pas de description."
    text = html.escape(str(text))
    replacements = {'{': '&#123;', '}': '&#125;', '<': '&lt;', '>': '&gt;', '$': '&#36;'}
    for char, escape in replacements.items():
        text = text.replace(char, escape)
    return text

# Charger les données
with open('links_final.json', 'r', encoding='utf-8') as f:
    links = json.load(f)

os.makedirs('docs/categories', exist_ok=True)

grouped = {}
for item in links:
    cat = item.get('category', 'divers').lower().strip()
    if cat not in grouped: grouped[cat] = []
    grouped[cat].append(item)

for cat, items in grouped.items():
    safe_name = "".join([c for c in cat if c.isalnum() or c in ('-', '_')])
    filename = f"docs/categories/{safe_name}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"---\ntitle: 📁 {cat.upper()}\n---\n\n")
        f.write(f"# {cat.upper()}\n\n")
        
        for link in items:
            url = link.get('url', '#')
            site_name = get_site_name(url)
            fr = super_sanitize(link.get('descriptionFR', ''))
            en = super_sanitize(link.get('descriptionEN', ''))
            
            # Titre avec le nom du site
            f.write(f"### 🔗 [{site_name}]({url})\n\n")
            
            # Affichage de l'URL brute
            f.write(f"**Lien :** `{url}`\n\n")
            
            # Bloc d'info (Admonition) corrigé avec les bons sauts de ligne
            f.write(f"info Descriptions\n\n") 
            f.write(f"**FR :** {fr}\n\n")
            f.write(f"**EN :** {en}\n\n")
            f.write(f"\n\n")
            
            f.write("---\n\n")

print(f"✅ Wiki mis à jour avec les noms de sites et formatage corrigé.")