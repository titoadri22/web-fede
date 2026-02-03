#!/bin/bash

# Script para actualizar enlaces en páginas de noticias

cd noticias

for file in *.html; do
    echo "Procesando $file..."
    
    # Enlaces principales de navegación
    sed -i '' 's|href="https://www.fsquash.com/clasificación"|href="../clasificacion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/clasificaci%C3%B3n"|href="../clasificacion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/blank-5"|href="../noticias.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/sobre"|href="../subvencion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/contacto"|href="../contacto.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/"|href="../index.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com"|href="../index.html"|g' "$file"
    
    # Enlaces a otras noticias
    sed -i '' 's|href="https://www.fsquash.com/4ªpruebaautonomica"|href="4ªpruebaautonomica.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/algemesiseptimos-1"|href="algemesiseptimos.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/algemesiseptimos"|href="algemesiseptimos.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/campeonatocvclubes"|href="campeonatocvclubes.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/campeonatoeuropaindividual"|href="campeonatoeuropaindividual.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ferracampeon"|href="ferracampeon.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ikerpajarescampeonpsa"|href="ikerpajarescampeonpsa.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/lodp"|href="lodp.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/martadominguezbronce"|href="martadominguezbronce.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/resultadoscopaespaña"|href="resultadoscopaespaña.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/squashdeporteolimpico2028"|href="squashdeporteolimpico2028.html"|g' "$file"
    
    # Enlaces de idiomas
    sed -i '' 's|href="https://www.fsquash.com/ca"|href="#"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/en"|href="#"|g' "$file"
    
done

cd ..

# Actualizar enlaces en archivos principales para apuntar a carpeta noticias/
for file in index.html clasificacion.html noticias.html subvencion.html contacto.html; do
    sed -i '' 's|href="noticias.html#4ªpruebaautonomica"|href="noticias/4ªpruebaautonomica.html"|g' "$file"
    sed -i '' 's|href="noticias.html#algemesiseptimos"|href="noticias/algemesiseptimos.html"|g' "$file"
    sed -i '' 's|href="noticias.html#campeonatocvclubes"|href="noticias/campeonatocvclubes.html"|g' "$file"
    sed -i '' 's|href="noticias.html#campeonatoeuropaindividual"|href="noticias/campeonatoeuropaindividual.html"|g' "$file"
    sed -i '' 's|href="noticias.html#ferracampeon"|href="noticias/ferracampeon.html"|g' "$file"
    sed -i '' 's|href="noticias.html#ikerpajarescampeonpsa"|href="noticias/ikerpajarescampeonpsa.html"|g' "$file"
    sed -i '' 's|href="noticias.html#lodp"|href="noticias/lodp.html"|g' "$file"
    sed -i '' 's|href="noticias.html#martadominguezbronce"|href="noticias/martadominguezbronce.html"|g' "$file"
    sed -i '' 's|href="noticias.html#resultadoscopaespaña"|href="noticias/resultadoscopaespaña.html"|g' "$file"
    sed -i '' 's|href="noticias.html#squashdeporteolimpico2028"|href="noticias/squashdeporteolimpico2028.html"|g' "$file"
done

echo "¡Enlaces de noticias actualizados!"
