#!/bin/bash

# Definir directorios
INPUT_FOLDER="input_files"
OUTPUT_FOLDER="converted_files"
TOOLS_FOLDER="tools"
VENV_FOLDER="venv"

# Crear carpetas necesarias
mkdir -p "$INPUT_FOLDER"
mkdir -p "$OUTPUT_FOLDER"
mkdir -p "$TOOLS_FOLDER"

# Configurar el entorno virtual de Python
if [ ! -d "$VENV_FOLDER" ]; then
    python3 -m venv "$VENV_FOLDER"
    echo "--- Entorno virtual creado ---"
fi

# Activar el entorno virtual
source "$VENV_FOLDER/bin/activate"

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Descargar herramientas en la carpeta "tools/"
cd "$TOOLS_FOLDER" || exit 1

# Descargar archivos con barra de progreso
download_with_progress() {
    local url=$1
    local output=$2
    echo "--- Descargando $output ---"
    curl -L --progress-bar -o "$output" "$url"
}

if [ ! -f "uf2conv.py" ]; then
    download_with_progress "https://raw.githubusercontent.com/microsoft/uf2/master/utils/uf2conv.py" "uf2conv.py"
    chmod +x uf2conv.py
fi

if [ ! -f "uf2families.json" ]; then
    download_with_progress "https://raw.githubusercontent.com/microsoft/uf2/master/utils/uf2families.json" "uf2families.json"
fi

cd ..

echo "--- Instalación y configuración completadas. Proyecto listo para usar. ---"
