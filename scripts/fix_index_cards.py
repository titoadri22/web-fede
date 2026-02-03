#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_FILE = os.path.join(BASE_DIR, "noticias.html")

def fix_index_cards():
    if not os.path.exists(INDEX_FILE):
        print(f"Error: No se encuentra {INDEX_FILE}")
        return

    print(f"Procesando: {os.path.basename(INDEX_FILE)}")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    modified = False

    # 1. Asegurar CSS Link
    head = soup.find('head')
    if head:
        # Check for wix-fix.css (relative path might be assets/css/wix-fix.css)
        css_link = soup.find('link', href=lambda h: h and 'wix-fix.css' in h)
        if not css_link:
            print("  -> Inyectando wix-fix.css")
            new_link = soup.new_tag('link', rel='stylesheet', href='assets/css/wix-fix.css')
            head.append(new_link)
            modified = True
    
    # 2. Limpiar Tarjetas (Repeater Items)
    repeater_items = soup.find_all(class_=lambda c: c and 'wixui-repeater__item' in c)
    print(f"  -> Encontradas {len(repeater_items)} tarjetas.")
    
    for item in repeater_items:
        # Limpiar estilos inline del contenedor principal
        if item.has_attr('style'):
            del item['style']
            modified = True
        
        # Recorrer todos los hijos recursivamente y limpiar posicionamiento
        for child in item.find_all(True): # True matches all tags
            if child.has_attr('style'):
                styles = child['style']
                # Eliminar position, top, left, grid-area, margin, width, height fixes
                # La forma más radical: borrar todo el style
                # Pero cuidado con background images... las tarjetas de texto no suelen tenerlas.
                
                # Vamos a borrar estilos de posicionamiento conflictivos
                style_list = [s.strip() for s in styles.split(';') if s.strip()]
                new_styles = []
                for s in style_list:
                    key = s.split(':')[0].strip().lower()
                    if key not in ['position', 'top', 'left', 'grid-area', 'width', 'height', 'margin', 'transform']:
                        new_styles.append(s)
                
                if len(new_styles) != len(style_list):
                    if new_styles:
                         child['style'] = '; '.join(new_styles)
                    else:
                        del child['style']
                    modified = True
            
            # Asegurarse de que los textes tengan la clase para reset (ya añadida en CSS nuclear *)
            # Pero podemos forzar más cosas si queremos.
            
    if modified:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("  -> Guardado noticias.html arreglado.")
    else:
        print("  -> No se necesitaron cambios en noticias.html")

if __name__ == '__main__':
    fix_index_cards()
