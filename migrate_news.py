import os
import re

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --primary-color: #333;
            --accent-color: #000;
            --bg-color: #f9f9f9;
            --container-width: 1100px; /* Increased max width for BIGGER impact */
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: var(--primary-color);
            background-color: var(--bg-color);
            line-height: 1.6;
        }}

        /* Nav Placeholder - Minimalist */
        .header-bar {{
            background: #fff;
            padding: 10px 0; /* Reduced padding */
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 20px; /* Reduced margin */
        }}
        .header-content {{
            max-width: var(--container-width);
            margin: 0 auto;
            padding: 0 20px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .header-content a {{
            text-decoration: none;
            color: #000;
        }}

        /* Main Content */
        .main-container {{
            max-width: var(--container-width);
            margin: 0 auto;
            padding: 0 10px 40px; /* Reduced padding side/top */
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        }}

        article {{
            padding: 20px; /* Reduced padding */
        }}

        h1 {{
            font-size: 2.2rem;
            line-height: 1.3;
            color: #000;
            margin-bottom: 20px; 
            text-align: center;
        }}

        .content-text {{
            font-size: 1.1rem;
            margin-bottom: 30px;
            max-width: 900px; /* Wider text to match */
            margin-left: auto;
            margin-right: auto;
            text-align: justify; 
        }}
        
        .content-text p {{
            margin-bottom: 15px; 
        }}

        /* Images Grid: 3 Columns Precise */
        .image-gallery {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px; /* Tighter gap */
            margin-top: 20px;
        }}

        .gallery-item {{
            /* Calc width for 3 columns minus gap */
            width: calc(33.333% - 8px); 
            max-width: none; 
            height: 550px; /* MUCH TALLER to allow vertical images to shine */
            overflow: hidden; 
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
            background: #fff;
        }}

        .gallery-item:hover {{
            z-index: 10;
            transform: scale(1.02); /* Pop out effect instead of just up */
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        }}

        .gallery-item img {{
            width: 100%;
            height: 100%;
            object-fit: contain; 
            object-position: center;
            display: block;
        }}
        
        @media (max-width: 768px) {{
            .gallery-item {{
                width: 100%;
                height: auto;
                max-height: 600px;
            }}
            article {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>

    <div class="header-bar">
        <div class="header-content">
            <a href="../index.html">← Volver a Noticias</a>
        </div>
    </div>

    <main class="main-container">
        <article>
            <h1>{title}</h1>

            <div class="content-text">
                {content_html}
            </div>

            <div class="image-gallery">
                {images_html}
            </div>

        </article>
    </main>

</body>
</html>
"""

DIR = "noticias"
SKIP = ["noticia-clean.html", "algemesi-final.html"] 

def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Extract Title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else None
    
    if not title:
         title_tag = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
         if title_tag:
             title = title_tag.group(1).split('|')[0].strip()
         else:
             title = os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()

    # Extract Content
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
    cleaned_paragraphs = []
    
    for p in paragraphs:
        clean_p = re.sub(r'<[^>]+>', '', p).strip()
        
        garbage = ["InicioSubvención", "PSA Calendario", "ClasificaciónNormativa", "FedérateCONTACTO"]
        if any(g in clean_p for g in garbage):
             clean_p = clean_p.replace("InicioSubvención PSA CalendarioClasificaciónNormativaNoticiasFedérateCONTACTO", "").strip()
             if not clean_p or len(clean_p) < 5:
                 continue

        if len(clean_p) > 20 and not "wix" in clean_p.lower():
             cleaned_paragraphs.append(f"<p>{clean_p}</p>")
    
    content_html = "\n".join(cleaned_paragraphs)
    if not content_html:
        content_html = "<p>Contenido no disponible automáticamente.</p>"

    # Method 2: Universal Source Capture
    images = []
    
    all_srcs_match = re.finditer(r'src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    
    for match in all_srcs_match:
        src = match.group(1)
        
        # Filter for Valid Images
        is_image = False
        
        # 1. Local Images
        if "assets/images" in src or "images/" in src:
            is_image = True
            
        # 2. Wix Static Media (Remote)
        elif "wixstatic.com/media" in src:
            if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                is_image = True
                
            if any(bad in src.lower() for bad in ['icon', 'logo', 'spacer', 'blank']):
                 if "logo" in src.lower() and "federacion" in src.lower():
                      is_image = False
                 else:
                      pass 
            
            if "icon" in src.lower(): is_image = False

        if is_image:
             # AGGRESSIVE CLEANING FOR HD
             # Look for the file extension followed by /v1/ or anything similar
             # OR if it contains ~mv2.ext, strip everything after
             
             if "~mv2." in src:
                 # Standard Wix structure: uuid~mv2.jpg/v1/fill...
                 # We want uuid~mv2.jpg
                 base_match = re.search(r'(.*?~mv2\.(?:jpg|jpeg|png|webp))', src, re.IGNORECASE)
                 if base_match:
                     src = base_match.group(1)
             
             # Fallback: if no ~mv2, but has /v1/fill
             elif "/v1/fill/" in src:
                  base_match = re.search(r'(.*?\.([a-zA-Z]{3,4}))/v1/fill', src)
                  if base_match:
                       src = base_match.group(1) 

             if src not in images:
                 images.append(src)
    
    # De-duplicate
    final_images = []
    seen = set()
    for img in images:
        if img not in seen:
            final_images.append(img)
            seen.add(img)

    # Generate Image HTML
    images_html = ""
    for src in final_images:
        images_html += f'<div class="gallery-item"><img src="{src}" alt="Imagen noticia"></div>'

    return title, content_html, images_html

def migrate():
    files = [f for f in os.listdir(DIR) if f.endswith('.html')]
    
    for filename in files:
        if filename in SKIP or filename.endswith('.backup'):
            continue
            
        path = os.path.join(DIR, filename)
        print(f"Processing {filename}...")
        
        if not os.path.exists(path + ".backup"):
            with open(path, 'rb') as orig:
                 with open(path + ".backup", 'wb') as backup:
                      backup.write(orig.read())
        
        source_path = path + ".backup"
        if os.path.exists(source_path):
             title, content, images = extract_content(source_path)
        else:
             title, content, images = extract_content(path)
        
        new_html = TEMPLATE.format(title=title, content_html=content, images_html=images)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
            
        print(f"Migrated {filename}")

if __name__ == "__main__":
    migrate()
