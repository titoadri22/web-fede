#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_DIR = os.path.join(BASE_DIR, "noticias")

def fix_news_padding_brute_force():
    if not os.path.exists(NEWS_DIR):
        print("Directorio de noticias no encontrado.")
        return

    print("Iniciando inyección de padding de emergencia...")
    
    for filename in os.listdir(NEWS_DIR):
        if filename.endswith(".html"):
            filepath = os.path.join(NEWS_DIR, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            modified = False
            
            # Estrategia: Buscar el contenedor de texto principal
            # Usualmente es un div con clase que contiene 'rich-text' o un ID 'comp-...'
            
            # Vamos a buscar el h1 y subir hasta encontrar un contenedor ancho
            # O simplemente buscar todos los contenedores probables y meterles padding
            
            # 1. Padding en el MAIN (Seguro global)
            main = soup.find('main')
            if main:
                # Forzar un padding seguro en el main container
                current_style = main.get('style', '')
                if 'padding-left' not in current_style:
                    padding_rule = "padding-left: 20px !important; padding-right: 20px !important; box-sizing: border-box !important;"
                    main['style'] = current_style + '; ' + padding_rule if current_style else padding_rule
                    modified = True
            
            # 2. Padding en los DIVs de texto enriquecido (Rich Text)
            # Para asegurar que los textos que se salen del flujo tengan padding
            rich_texts = soup.find_all(class_=lambda c: c and ('wixui-rich-text' in c or 'rich-text' in c))
            for rt in rich_texts:
                current_style = rt.get('style', '')
                if 'padding' not in current_style:
                    # Solo aplicamos si no parece tener ya un padding
                    padding_rule = "padding-left: 10px !important; padding-right: 10px !important; box-sizing: border-box !important;"
                    rt['style'] = current_style + '; ' + padding_rule if current_style else padding_rule
                    modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print(f"  -> Padding inyectado en: {filename}")
            else:
                print(f"  -> {filename} sin cambios requeridos.")

if __name__ == '__main__':
    fix_news_padding_brute_force()
