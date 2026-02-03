import os

news_dir = "noticias"
js_tag = '<script src="../assets/js/layout-fix.js"></script>'
css_tag = '<link rel="stylesheet" href="../assets/css/wix-fix.css">'

print("Iniciando inyección de script en noticias...")

count = 0
for filename in os.listdir(news_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(news_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated = False
        
        # Inyectar CSS si falta
        if "wix-fix.css" not in content:
            if '<link rel="stylesheet" href="../assets/css/custom-news-styles.css">' in content:
                content = content.replace(
                    '<link rel="stylesheet" href="../assets/css/custom-news-styles.css">',
                    f'{css_tag}\n<link rel="stylesheet" href="../assets/css/custom-news-styles.css">'
                )
                updated = True
                print(f"CSS inyectado en {filename}")
        
        # Inyectar JS si falta
        if "layout-fix.js" not in content:
            if "</body>" in content:
                content = content.replace("</body>", f"{js_tag}\n</body>")
                updated = True
                print(f"JS inyectado en {filename}")
            else:
                # Fallback: al final del archivo
                content += f"\n{js_tag}"
                updated = True
                print(f"JS inyectado al final de {filename}")

        if updated:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1

print(f"Completado. {count} archivos actualizados.")
