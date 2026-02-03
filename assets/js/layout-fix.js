window.addEventListener('load', function () {
    console.log("Layout Fixer: Iniciando reparación AGRESIVA...");

    // 1. Desactivar posicionamiento absoluto y fijar contenedores
    const relativeContainers = document.querySelectorAll('main, section, article, [id^="comp-"], [class*="wixui-"]');
    relativeContainers.forEach(el => {
        el.style.position = 'relative';
        el.style.top = 'auto';
        el.style.left = 'auto';
        el.style.height = 'auto';
        el.style.minHeight = 'auto';
        el.style.width = '100%';
        el.style.maxWidth = '100%';
    });

    // 2. ENCONTRAR EL TÍTULO (Lógica mejorada)
    let titleElement = null;

    // Intento 1: Buscar elemento con clase 'news-article-title' si ya existe
    titleElement = document.querySelector('.news-article-title');

    // Intento 2: Buscar el primer párrafo con texto significativo que sea negrita
    if (!titleElement) {
        const candidates = document.querySelectorAll('p, span, h1, h2, div');
        for (let el of candidates) {
            const text = el.textContent.trim();
            // Ignorar menús, footers (heurística simple por longitud y posición)
            if (text.length > 10 && text.length < 150) {
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();

                // Si está en la parte superior (probablemente el título) y es visible
                if (rect.top < 400 && rect.height > 0) {
                    const isBold = style.fontWeight === '700' || style.fontWeight === 'bold' || parseInt(style.fontWeight) >= 600;

                    // Si es negrita O es el texto más grande encontrado hasta ahora
                    if (isBold) {
                        titleElement = el;
                        break;
                    }
                }
            }
        }
    }

    // Si aún no encontramos, buscar por conteo de palabras (títulos suelen ser cortos) al inicio del contenedor principal
    if (!titleElement) {
        const mainContent = document.querySelector('[data-testid="richTextElement"]');
        if (mainContent) {
            const firstP = mainContent.querySelector('p');
            if (firstP) titleElement = firstP;
        }
    }

    // 3. APLICAR FIX AL TÍTULO
    if (titleElement) {
        console.log("Título detectado:", titleElement.textContent);

        // Crear un nuevo elemento H1 limpio
        const h1 = document.createElement('h1');
        h1.textContent = titleElement.textContent;
        h1.className = 'news-article-title-fixed'; // Nueva clase específica

        // Insertar el H1 al principio del contenedor principal de texto
        const contentContainer = titleElement.closest('[data-testid="richTextElement"]') ||
            titleElement.closest('[class*="wixui-rich-text"]') ||
            titleElement.parentElement;

        if (contentContainer) {
            // Eliminar el elemento original (que era un párrafo pequeño o span)
            titleElement.style.display = 'none'; // Ocultar en lugar de borrar por si acaso

            // Insertar H1 al inicio
            contentContainer.insertBefore(h1, contentContainer.firstChild);

            // Añadir espaciador después del H1
            const spacer = document.createElement('div');
            spacer.style.height = '30px';
            spacer.style.width = '100%';
            contentContainer.insertBefore(spacer, h1.nextSibling);

            console.log("Título transformado a H1 y posicionado.");
        }
    }

    // 4. LIMPIEZA GENERAL DE TEXTO
    const allText = document.querySelectorAll('p, span:not([class*="wixui-"]), div[class*="wixui-rich-text__text"]');
    allText.forEach(el => {
        // Ignorar el título nuevo
        if (el.className === 'news-article-title-fixed') return;

        // Forzar estilos legibles
        el.style.fontSize = '18px';
        el.style.lineHeight = '1.8';
        el.style.color = '#2a2a2a';

        // Resetear posicionamiento que causa superposiciones
        el.style.position = 'relative';
        el.style.top = 'auto';
        el.style.marginBottom = '16px';
    });

    console.log("Fix agresivo completado.");
});
