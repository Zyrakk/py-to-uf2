import subprocess
import os

def convert_py_to_uf2(py_file: str, output_dir: str = "converted_files") -> str:
    """
    Convierte un archivo .py a .uf2 utilizando uf2conv.py.
    """
    uf2conv_path = "tools/uf2conv.py"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(py_file))[0] + ".uf2")

    try:
        subprocess.run(["python", uf2conv_path, "--output", output_file, py_file], check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir {py_file} a UF2: {e}")
        return ""

if __name__ == "__main__":
    test_file = "test.py"
    output = convert_py_to_uf2(test_file)
    if output:
        print(f"Archivo convertido con éxito: {output}")
