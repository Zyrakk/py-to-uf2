import subprocess
import os

def convert_py_to_uf2(py_file: str, output_dir: str = "converted_files") -> str:
    """
    Convierte un archivo .py a .uf2 utilizando mpy-cross y uf2conv.py.
    """
    uf2conv_path = "tools/uf2conv.py"
    mpy_cross_path = "mpy-cross"  # Asegúrate de que mpy-cross está instalado y en el PATH

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_bin = os.path.join(output_dir, os.path.splitext(os.path.basename(py_file))[0] + ".bin")
    output_uf2 = os.path.join(output_dir, os.path.splitext(os.path.basename(py_file))[0] + ".uf2")

    try:
        # Paso 1: Convertir el archivo .py en un .bin válido para UF2
        result_bin = subprocess.run(
            [mpy_cross_path, "-o", output_bin, py_file],
            capture_output=True, text=True
        )

        if result_bin.returncode != 0:
            print(f"❌ Error al convertir {py_file} a BIN:\n{result_bin.stderr}")
            return ""

        print(f"✅ {py_file} convertido a BIN: {output_bin}")

        # Paso 2: Convertir el .bin a .uf2
        result_uf2 = subprocess.run(
            ["python3", uf2conv_path, "--convert", "--output", output_uf2, output_bin],
            capture_output=True, text=True
        )

        if result_uf2.returncode != 0:
            print(f"❌ Error al convertir BIN a UF2:\n{result_uf2.stderr}")
            return ""

        print(f"✅ {output_bin} convertido a UF2: {output_uf2}")

        return output_uf2

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return ""

if __name__ == "__main__":
    test_file = "test.py"
    output = convert_py_to_uf2(test_file)
    if output:
        print(f"✅ Archivo convertido con éxito: {output}")
