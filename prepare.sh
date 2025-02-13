#!/bin/bash

# Definir directorios
INPUT_FOLDER="input_files"
OUTPUT_FOLDER="converted_files"
TOOLS_FOLDER="tools"
VENV_FOLDER="venv"
MPY_CROSS_PATH="/usr/local/bin/mpy-cross"
MICROPYTHON_REPO="https://github.com/micropython/micropython.git"

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

# Instalar y compilar mpy-cross si no está instalado
if [ ! -f "$MPY_CROSS_PATH" ]; then
    echo "--- Clonando MicroPython y compilando mpy-cross ---"
    git clone "$MICROPYTHON_REPO"
    cd micropython/mpy-cross || exit 1

    echo "--- Limpiando compilación previa ---"
    make clean

    echo "--- Compilando mpy-cross (esto puede tardar) ---"
    make -j$(nproc) | pv -lep -s $(nproc) > /dev/null

    sudo mv mpy-cross "$MPY_CROSS_PATH"
    sudo chmod +x "$MPY_CROSS_PATH"
    cd ../..
    rm -rf micropython  # Elimina la carpeta del repositorio para limpiar espacio
fi

# Verificar y corregir el intérprete de Python en mpy-cross
MPY_CROSS_INTERPRETER=$(head -n 1 "$MPY_CROSS_PATH")
if [[ "$MPY_CROSS_INTERPRETER" == "#!/root/mpy-env/bin/python3" ]]; then
    echo "--- Corrigiendo el intérprete de Python en mpy-cross ---"
    sudo sed -i '1s|.*|#!/usr/bin/python3|' "$MPY_CROSS_PATH"
fi

# Verificar que mpy-cross está instalado correctamente
if mpy-cross --help &>/dev/null; then
    echo "--- mpy-cross instalado correctamente ---"
else
    echo "❌ ERROR: mpy-cross no se instaló correctamente"
    exit 1
fi

echo "--- Instalación y configuración completadas. Proyecto listo para usar. ---"
