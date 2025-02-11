# Guía de Instalación para Py to UF2 Converter

Este proyecto convierte archivos `.py` a `.uf2` para su uso en CircuitPython.

## Estructura

```
📦 py-to-uf2
 ┣ 📂 converted_files/        # Carpeta donde se guardarán los archivos .uf2
 ┣ 📂 resources/              # Carpeta de recursos del frontend  
 ┣ 📜 .gitignore              # Ignora archivos innecesarios
 ┣ 📜 requirements.txt        # Dependencias del proyecto
 ┣ 📜 convert.py              # Script de conversión
 ┣ 📜 prepare.sh              # Script de instalacion.
 ┣ 📜 main.py                 # Servidor FastAPI
 ┣ 📜 index.html              # Frontend para manejar el convertidor
```

## 📥 Instalación y Configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Zyrakk/py-to-uf2.git
cd py-to-uf2
```

### 2️⃣ Ejecutar el script de instalación
Ejecuta el siguiente comando para configurar el entorno:

```bash
chmod +x prepare.sh
./prepare.sh
```

Este script realizará automáticamente las siguientes acciones:
- Creará las carpetas necesarias (`converted_files/` y `tools/`).
- Configurará un entorno virtual (`venv/`).
- Instalará todas las dependencias en el entorno virtual.
- Descargará `uf2conv.py` y `uf2families.json` en la carpeta `tools/`.

---

## 🚀 Uso
### 🔹 Convertir un archivo `.py` a `.uf2`
```bash
echo "print('Hello, CircuitPython!')" > test.py
python tools/uf2conv.py --output converted_files/test.uf2 test.py
```

El archivo convertido se guardará en la carpeta `converted_files/`.

---

✅ **El sistema ya está listo para integrar con FastAPI.** 🚀
