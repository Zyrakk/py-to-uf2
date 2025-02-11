from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
import os
import subprocess
import shutil

# Cargar variables del archivo .env
load_dotenv()

# Obtener el token de autenticación desde el entorno
API_TOKEN = os.getenv("API_TOKEN")

# Validar que API_TOKEN está configurado
if not API_TOKEN:
    raise ValueError("Error: API_TOKEN no está definido en el archivo .env")

# Configuración del servidor
app = FastAPI(root_path="/api")

# Carpeta de archivos convertidos
UPLOAD_FOLDER = "converted_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

security = HTTPBearer()

def verify_token(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    client_ip = request.client.host  # Obtiene la IP del cliente

    # Permitir acceso sin token si la solicitud viene de localhost
    if client_ip in ["127.0.0.1", "localhost"]:
        return None

    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

    return credentials

# Ruta para convertir el archivo (con autenticación solo para accesos externos)
@app.post("/convert")
async def convert_file(
    request: Request,
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    try:
        input_filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        output_filepath = os.path.join(UPLOAD_FOLDER, file.filename.replace(".py", ".uf2"))

        with open(input_filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = subprocess.run(["python3", "convert.py", input_filepath, output_filepath], capture_output=True, text=True)

        if result.returncode != 0:
            return JSONResponse(status_code=500, content={"detail": f"Error en la conversión: {result.stderr}"})

        return JSONResponse(content={"output_file": f"/download/{os.path.basename(output_filepath)}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Ruta para descargar el archivo convertido (sin autenticación)
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"detail": "Archivo no encontrado"})
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
