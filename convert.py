import subprocess
import os
import shutil
import sys

# Definir la carpeta base usando la ubicación real del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Definir carpetas relativas a BASE_DIR
INPUT_FOLDER = os.path.join(BASE_DIR, "input_files")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "converted_files")
LOG_ERROR = os.path.join(BASE_DIR, "error.log")
LOG_CONVERT = os.path.join(BASE_DIR, "convert.log")

# Crear carpetas si no existen
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def log_message(log_file, message):
    """Escribe un mensaje en el archivo de log especificado."""
    with open(log_file, "a") as log:
        log.write(message + "\n")

def convert_py_to_uf2(py_file: str) -> str:
    """
    Convierte un archivo .py a .uf2 utilizando mpy-cross y uf2conv.py.
    """
    uf2conv_path = os.path.join(BASE_DIR, "tools", "uf2conv.py")
    mpy_cross_path = "mpy-cross"  # Asegúrate de que mpy-cross esté en el PATH

    # Verificar existencia de archivos y herramientas
    if not os.path.exists(py_file):
        log_message(LOG_ERROR, f"❌ ERROR: Archivo {py_file} no encontrado.")
        return ""

    if not shutil.which(mpy_cross_path):
        log_message(LOG_ERROR, "❌ ERROR: mpy-cross no está instalado o no está en el PATH.")
        return ""

    if not os.path.exists(uf2conv_path):
        log_message(LOG_ERROR, f"❌ ERROR: No se encontró {uf2conv_path}.")
        return ""

    output_bin = os.path.join(OUTPUT_FOLDER, os.path.splitext(os.path.basename(py_file))[0] + ".bin")
    output_uf2 = os.path.join(OUTPUT_FOLDER, os.path.splitext(os.path.basename(py_file))[0] + ".uf2")

    try:
        # Convertir .py a .bin con mpy-cross
        result_bin = subprocess.run(
            [mpy_cross_path, "-o", output_bin, py_file],
            capture_output=True, text=True
        )

        if result_bin.returncode != 0:
            log_message(LOG_ERROR, f"❌ Error al convertir {py_file} a BIN:\n{result_bin.stderr}")
            return ""

        log_message(LOG_CONVERT, f"✅ {py_file} convertido a BIN: {output_bin}")

        # Convertir .bin a .uf2 con uf2conv.py
        result_uf2 = subprocess.run(
            ["python3", uf2conv_path, "--convert", "--output", output_uf2, output_bin],
            capture_output=True, text=True
        )

        if result_uf2.returncode != 0:
            log_message(LOG_ERROR, f"❌ Error al convertir {output_bin} a UF2:\n{result_uf2.stderr}")
            return ""

        log_message(LOG_CONVERT, f"✅ {output_bin} convertido a UF2: {output_uf2}")

        return output_uf2

    except Exception as e:
        log_message(LOG_ERROR, f"❌ ERROR GENERAL: {str(e)}")
        return ""

if __name__ == "__main__":
    # Verificar que se haya pasado el archivo a convertir
    if len(sys.argv) < 2:
        print("Usage: python3 convert.py <py_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output = convert_py_to_uf2(input_file)

    if output:
        print(f"Conversion exitosa: {output}")
        sys.exit(0)
    else:
        print("Fallo en la conversión.")
        sys.exit(1)
