#!/usr/bin/env python3
import os
import re
from bs4 import BeautifulSoup

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTICIAS_DIR = os.path.join(BASE_DIR, "noticias")

def fix_news_file(filepath):
    filename = os.path.basename(filepath)
    print(f"Procesando: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Detectar si es un archivo de Wix (tiene wixui-rich-text)
    if 'wixui-rich-text' not in content:
        print(f"  -> Saltando (no parece noticia Wix)")
        return

    # Usamos BeautifulSoup para manipulación estructural robusta
    # Nota: html.parser es el estándar, lxml sería más rápido pero requiere dependencia.
    soup = BeautifulSoup(content, 'html.parser')
    
    # --- FIX DE LAYOUT (GRID -> BLOCK) ---
    # Estrategia: Encontrar contenedores de texto rico y transformar su padre a Block
    
    rich_texts = soup.find_all('div', class_=lambda c: c and 'wixui-rich-text' in c)
    modified = False
    
    for rt in rich_texts:
        # Verificar si es el H1 inyectado o cuerpo
        # Si es el H1 inyectado, ya tiene nuestra clase (quizás)
        # Pero queremos aplicar el fix al PADRE
        
        parent = rt.parent
        if parent and parent.name == 'div':
            # Aplicar clase al padre para romper el Grid
            if 'news-container-block' not in parent.get('class', []):
                # Asegurarse de que 'class' sea una lista antes de append
                if not parent.get('class'):
                    parent['class'] = []
                parent['class'].append('news-container-block')
                modified = True
            
            # Aplicar clase al hijo (el texto mismo) para que fluya
             # Limpiar estilos inline conflictivos grid-area, position absolute
            if 'news-content-relative' not in rt.get('class', []):
                 if not rt.get('class'):
                    rt['class'] = []
                 rt['class'].append('news-content-relative')
                 
                 # Si parece ser el cuerpo (tiene muchos párrafos), añadir margen extra
                 if len(rt.find_all('p')) > 2:
                     rt['class'].append('news-content-body')
                 
                 # Limpiar estilos conflictivos inline
                 if rt.has_attr('style'):
                     styles = rt['style'].split(';')
                     new_styles = [s for s in styles if 'grid-area' not in s and 'position' not in s and 'top' not in s]
                     rt['style'] = ';'.join(new_styles)
                 
                 modified = True

    # --- INYECCIÓN DE H1 LIMPIO (SI NO EXISTE YA) ---
    # Buscar si ya existe el H1 inyectado
    existing_h1 = soup.find('h1', class_='news-article-title-fixed')
    if not existing_h1:
        # Buscar el título original (h2 oculto o similar)
        # El patrón suele ser h2 dentro de wixui-rich-text, a veces oculto visualmente
        # O en algunos archivos puede ser diferente.
        # Intentaremos encontrar el primer texto significativo
        pass # Por ahora asumimos que el script previo ya inyectó H1s, no queremos duplicar.
        # Si el usuario quiere regenerar H1s, deberíamos borrar los previos.
    
    # Asegurar que wix-fix.css está vinculado
    head = soup.find('head')
    if head:
        css_link = soup.find('link', href=lambda h: h and 'wix-fix.css' in h)
        if not css_link:
            new_link = soup.new_tag('link', rel='stylesheet', href='../assets/css/wix-fix.css')
            head.append(new_link)
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"  -> Modificado y guardado.")
    else:
        print(f"  -> No se requirieron cambios.")

def main():
    files = [f for f in os.listdir(NOTICIAS_DIR) if f.endswith('.html')]
    for file in files:
        fix_news_file(os.path.join(NOTICIAS_DIR, file))

if __name__ == '__main__':
    # Necesitamos instalar beautifulsoup4 si no está
    try:
        import bs4
    except ImportError:
        print("Instalando beautifulsoup4...")
        os.system("pip3 install beautifulsoup4")
    
    main()
