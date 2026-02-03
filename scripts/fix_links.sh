#!/bin/bash

# Script para reemplazar todos los enlaces de fsquash.com por archivos locales

FILES="index.html clasificacion.html noticias.html subvencion.html contacto.html"

for file in $FILES; do
    echo "Procesando $file..."
    
    # Enlaces principales de navegación
    sed -i '' 's|href="https://www.fsquash.com/clasificación"|href="clasificacion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/clasificaci%C3%B3n"|href="clasificacion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/blank-5"|href="noticias.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/sobre"|href="subvencion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/contacto"|href="contacto.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/"|href="index.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com"|href="index.html"|g' "$file"
    
    # Enlaces de noticias individuales - mantener como anclas en noticias.html
    sed -i '' 's|href="https://www.fsquash.com/4ªpruebaautonomica"|href="noticias.html#4ªpruebaautonomica"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/algemesiseptimos-1"|href="noticias.html#algemesiseptimos-1"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/algemesiseptimos"|href="noticias.html#algemesiseptimos"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/blank-4"|href="noticias.html#blank-4"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/campeonatocvclubes"|href="noticias.html#campeonatocvclubes"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/campeonatoeuropaindividual"|href="noticias.html#campeonatoeuropaindividual"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/campeonatoeuroparesultados"|href="noticias.html#campeonatoeuroparesultados"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/campeonatoveteranoseuropa"|href="noticias.html#campeonatoveteranoseuropa"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/copaespaña111519"|href="noticias.html#copaespaña111519"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ferracampeon"|href="noticias.html#ferracampeon"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ikerpajarescampeonpsa"|href="noticias.html#ikerpajarescampeonpsa"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/lodp"|href="noticias.html#lodp"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/martadominguezbronce"|href="noticias.html#martadominguezbronce"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/resultadoscopaespaña"|href="noticias.html#resultadoscopaespaña"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/resultadospanish"|href="noticias.html#resultadospanish"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/resultadoveteranos"|href="noticias.html#resultadoveteranos"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/squashdeporteolimpico2028"|href="noticias.html#squashdeporteolimpico2028"|g' "$file"
    
    # Enlaces de idiomas - mantener en la misma página
    sed -i '' 's|href="https://www.fsquash.com/ca"|href="#"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/en"|href="#"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ca/blank-5"|href="noticias.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ca/clasificaci%C3%B3n"|href="clasificacion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ca/contacto"|href="contacto.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/ca/sobre"|href="subvencion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/en/blank-5"|href="noticias.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/en/clasificaci%C3%B3n"|href="clasificacion.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/en/contacto"|href="contacto.html"|g' "$file"
    sed -i '' 's|href="https://www.fsquash.com/en/sobre"|href="subvencion.html"|g' "$file"
    
done

echo "¡Todos los enlaces han sido actualizados!"
