import subprocess
import os
import shutil

# Definir carpetas
INPUT_FOLDER = os.path.abspath("input_files")
OUTPUT_FOLDER = os.path.abspath("converted_files")
LOG_ERROR = os.path.abspath("error.log")
LOG_CONVERT = os.path.abspath("convert.log")

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
    uf2conv_path = os.path.abspath("tools/uf2conv.py")
    mpy_cross_path = "mpy-cross"  # Asegúrate de que mpy-cross está en el PATH

    if not os.path.exists(py_file):
        log_message(LOG_ERROR, f"❌ ERROR: Archivo {py_file} no encontrado.")
        return ""

    output_bin = os.path.join(OUTPUT_FOLDER, os.path.splitext(os.path.basename(py_file))[0] + ".bin")
    output_uf2 = os.path.join(OUTPUT_FOLDER, os.path.splitext(os.path.basename(py_file))[0] + ".uf2")

    try:
        # Convertir .py a .bin
        result_bin = subprocess.run(
            [mpy_cross_path, "-o", output_bin, py_file],
            capture_output=True, text=True
        )

        if result_bin.returncode != 0:
            log_message(LOG_ERROR, f"❌ Error al convertir {py_file} a BIN:\n{result_bin.stderr}")
            return ""

        log_message(LOG_CONVERT, f"✅ {py_file} convertido a BIN: {output_bin}")

        # Convertir .bin a .uf2
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
    test_file = os.path.join(INPUT_FOLDER, "test.py")
    output = convert_py_to_uf2(test_file)
    if output:
        log_message(LOG_CONVERT, f"✅ Archivo convertido con éxito: {output}")
