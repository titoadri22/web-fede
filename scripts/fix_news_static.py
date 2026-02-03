#!/usr/bin/env python3
import os
import re

def fix_news_html(filepath):
    """Fix visual issues in a news HTML file."""
    # print(f"Procesando: {os.path.basename(filepath)}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Remover layout-fix.js (por si acaso)
    content = re.sub(
        r'<script src="../assets/js/layout-fix\.js"></script>\s*',
        '',
        content
    )
    
    # Flags para saber qué hemos hecho
    h1_exists = '<h1 style="font-size: 40px !important;' in content
    
    # 2. Si NO hay H1 inyectado, buscar y reemplazar título original
    if not h1_exists:
        title_pattern = r'(<h[1-6]\s+class="font_[0-9]\s+wixui-rich-text__text">)([^<]+)(</h[1-6]>)'
        match = re.search(title_pattern, content, re.IGNORECASE)
        if match:
            # Ocultar el título original
            hidden_title = f'{match.group(1)}<span style="display:none;">{match.group(2)}</span>{match.group(3)}'
            
            # Crear H1 nuevo con z-index alto
            new_h1 = f'''<h1 style="font-size: 40px !important; font-weight: 700 !important; line-height: 1.2 !important; margin-bottom: 30px !important; margin-top: 0 !important; color: #000000 !important; display: block !important; position: relative !important; clear: both !important; z-index: 1000 !important;">{match.group(2)}</h1>
<div style="height: 60px; width: 100%; clear: both; display: block;"></div>
{hidden_title}'''
            
            content = content[:match.start()] + new_h1 + content[match.end():]
            print(f"  ✓ {os.path.basename(filepath)}: Título transformado a H1")
            h1_exists = True
        else:
            print(f"  ⚠ {os.path.basename(filepath)}: No se encontró título original")
    
    # 3. Forzar margin-top en el primer párrafo de contenido
    # Esto es CRÍTICO para evitar el solapamiento
    if h1_exists:
        # Buscar el primer <p> después del H1 o del título oculto
        # Buscamos un p con clase font_8 que NO tenga ya el margen aplicado
        first_p_pattern = r'(<p\s+class="font_8[^"]*")([^>]*>)'
        
        # Función para inyectar el margen
        def inject_margin(match):
            attrs = match.group(1)
            end = match.group(2)
            
            if 'margin-top: 100px' in attrs:
                return match.group(0) # Ya tiene el fix
                
            if 'style="' in attrs:
                return attrs.replace('style="', 'style="margin-top: 120px !important; ') + end
            else:
                return attrs + ' style="margin-top: 120px !important;"' + end

        # Reemplazamos SOLO la primera ocurrencia después del área del título
        # Como es difícil saber dónde está el título con regex simple, reemplazamos el primer <p class="font_8"> del documento
        # Asumimos que el primer párrafo de texto es el contenido de la noticia
        content = re.sub(first_p_pattern, inject_margin, content, count=1)
        # print(f"  ✓ {os.path.basename(filepath)}: Margen aplicado al primer párrafo")

    # 4. Limpieza de posicionamiento (segunda pasada para asegurar)
    content = re.sub(r'position:\s*absolute', 'position: relative', content)
    content = re.sub(r'top:\s*-?\d+(?:\.\d+)?px', 'top: auto', content)
    content = re.sub(r'left:\s*-?\d+(?:\.\d+)?px', 'left: auto', content)
    
    # 5. Escribir cambios
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    news_dir = 'noticias'
    exclude = ['blank-4.html', 'lodp.html']
    count = 0
    for filename in sorted(os.listdir(news_dir)):
        if filename.endswith('.html') and filename not in exclude:
            if fix_news_html(os.path.join(news_dir, filename)):
                count += 1
                print(f"Actualizado: {filename}")
    print(f"Total actualizados: {count}")

if __name__ == '__main__':
    main()
