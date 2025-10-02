#!/bin/bash

echo "========================================"
echo " Generador de Noticias para LinkedIn"
echo "========================================"
echo

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo
echo "⚙️ Configurando entorno..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado desde plantilla"
    echo "💡 Edita el archivo .env con tus API keys"
else
    echo "✅ Archivo .env ya existe"
fi

echo
echo "🚀 Todo listo! Para ejecutar la aplicación:"
echo "   streamlit run app.py"
echo
echo "📚 Documentación completa en README.md"
echo "💻 Ejemplos en main.ipynb"
echo