#!/bin/bash

# Crear carpetas necesarias
mkdir -p converted_files
mkdir -p tools

# Instalar dependencias de Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Descargar herramientas necesarias en tools/
cd tools || exit 1
wget -q --show-progress https://raw.githubusercontent.com/microsoft/uf2/master/utils/uf2conv.py
wget -q --show-progress https://raw.githubusercontent.com/microsoft/uf2/master/utils/uf2families.json
chmod +x uf2conv.py
cd ..

echo "--- Instalación y configuración completadas. Proyecto listo para usar. ---"
