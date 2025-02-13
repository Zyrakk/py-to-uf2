from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
import os
import subprocess
import shutil

# Cargar variables del entorno
load_dotenv()

# Configuración de autenticación
API_TOKEN = os.getenv("API_TOKEN")
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "true").lower() == "true"  # Habilitar o deshabilitar autenticación

# Definir carpetas
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "input_files")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "converted_files")
LOG_ERROR = os.path.join(BASE_DIR, "error.log")
LOG_CONVERT = os.path.join(BASE_DIR, "convert.log")
CONVERT_SCRIPT = os.path.join(BASE_DIR, "convert.py")

# Crear carpetas si no existen
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Inicializar FastAPI
app = FastAPI(root_path="/api")

# Configuración de autenticación
security = HTTPBearer()

def log_message(log_file: str, message: str):
    """Escribe un mensaje en el archivo de log."""
    with open(log_file, "a") as log:
        log.write(message + "\n")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verifica la API Key si está habilitada la autenticación."""
    if not REQUIRE_AUTH:
        return None  # No requiere autenticación
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return credentials

@app.post("/convert")
async def convert_file(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Depends(verify_token) if REQUIRE_AUTH else None):
    """Sube y convierte un archivo .py a UF2."""
    try:
        input_filepath = os.path.join(INPUT_FOLDER, file.filename)
        output_filepath = os.path.join(OUTPUT_FOLDER, file.filename.replace(".py", ".uf2"))

        # Guardar el archivo .py en la carpeta de entrada
        with open(input_filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Verificar si el archivo se guardó correctamente
        if not os.path.exists(input_filepath):
            log_message(LOG_ERROR, f"❌ ERROR: No se pudo guardar {input_filepath}")
            return JSONResponse(status_code=500, content={"detail": "Error al guardar el archivo"})

        # Ejecutar convert.py
        result = subprocess.run(["python3", CONVERT_SCRIPT, input_filepath], capture_output=True, text=True)

        # Manejo de errores de conversión
        if result.returncode != 0:
            log_message(LOG_ERROR, f"❌ Error en la conversión de {file.filename}:\n{result.stderr}")
            return JSONResponse(status_code=500, content={"detail": "Error en la conversión. Revisa error.log"})

        # Eliminar el archivo .py después de la conversión
        os.remove(input_filepath)

        # Verificar que el archivo .uf2 existe antes de marcar la conversión como exitosa
        if not os.path.exists(output_filepath):
            log_message(LOG_ERROR, f"❌ ERROR: El archivo convertido {output_filepath} no se generó correctamente.")
            return JSONResponse(status_code=500, content={"detail": "Error en la conversión. No se generó el archivo UF2."})

        log_message(LOG_CONVERT, f"✅ Conversión exitosa de {file.filename} -> {output_filepath}")

        return JSONResponse(content={"output_file": f"/download/{os.path.basename(output_filepath)}"})

    except Exception as e:
        log_message(LOG_ERROR, f"❌ ERROR GENERAL: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Descarga un archivo convertido."""
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        log_message(LOG_ERROR, f"❌ ERROR: Archivo {filename} no encontrado.")
        return JSONResponse(status_code=404, content={"detail": "Archivo no encontrado"})
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
