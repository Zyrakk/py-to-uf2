from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from ipaddress import ip_address, ip_network
import os
import subprocess
import shutil
import sys

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

    # Lista de orígenes permitidos (localhost y frontend web)
    allowed_origins = ["127.0.0.1", "localhost", "stefsec.com"]
    # Definir el rango de IPs de la red local
    local_networks = [ip_network("192.168.1.0/24")]

    # Convertir la IP del cliente en formato de red
    try:
        client_ip_obj = ip_address(client_ip)
    except ValueError:
        raise HTTPException(status_code=400, detail="IP no válida")

    # Permitir acceso sin token si la IP es localhost, de la red local o de mi web
    if client_ip in allowed_origins or any(client_ip_obj in net for net in local_networks):
        return None

    # Verificación normal del token para accesos externos
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

    return credentials

# Ruta para convertir el archivo (con autenticación solo para accesos externos)
@app.post("/convert")
async def convert_file(
    request: Request,
    file: UploadFile = File(...),
    # credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    log_file = "/var/www/html/py-to-uf2/convert_debug.log"

    try:
        with open(log_file, "w") as log:
            log.write("🚀 Iniciando conversión de archivo...\n")

        input_filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        output_filepath = os.path.join(UPLOAD_FOLDER, file.filename.replace(".py", ".uf2"))

        with open(log_file, "a") as log:
            log.write(f"📂 Guardando archivo en: {input_filepath}\n")

        with open(input_filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(log_file, "a") as log:
            log.write(f"✅ Archivo guardado exitosamente.\n")

        # Verificar que el script convert.py está en el directorio correcto
        script_path = os.path.abspath("convert.py")

        with open(log_file, "a") as log:
            log.write(f"🔍 Verificando existencia de convert.py en: {script_path}\n")
            log.write(f"📌 Archivos en directorio actual: {os.listdir('.')}\n")

        if not os.path.exists(script_path):
            with open(log_file, "a") as log:
                log.write("❌ ERROR: convert.py no encontrado!\n")
            return JSONResponse(status_code=500, content={"detail": "convert.py no encontrado"})

        # Usar el mismo Python del entorno virtual
        python_exec = sys.executable

        with open(log_file, "a") as log:
            log.write(f"🐍 Usando Python en: {python_exec}\n")
            log.write(f"🚀 Ejecutando comando: {python_exec} {script_path} {input_filepath} {output_filepath}\n")

        result = subprocess.run(
            [python_exec, script_path, input_filepath, output_filepath],
            capture_output=True, text=True
        )

        with open(log_file, "a") as log:
            log.write(f"🔎 STDOUT:\n{result.stdout}\n")
            log.write(f"⚠️ STDERR:\n{result.stderr}\n")
            log.write(f"🔄 Código de salida: {result.returncode}\n")

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Error en la conversión. Revisa convert_debug.log",
                }
            )

        with open(log_file, "a") as log:
            log.write(f"✅ Conversión completada exitosamente. Archivo generado: {output_filepath}\n")

        return JSONResponse(content={"output_file": f"/download/{os.path.basename(output_filepath)}"})

    except Exception as e:
        with open(log_file, "a") as log:
            log.write(f"❌ ERROR: {str(e)}\n")
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Ruta para descargar el archivo convertido (sin autenticación)
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"detail": "Archivo no encontrado"})
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
