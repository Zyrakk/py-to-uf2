# Guía de Instalación para Py to UF2 Converter

Este proyecto convierte archivos `.py` a `.uf2` para su uso en CircuitPython.

## 📂 Estructura del Proyecto

```
📦 py-to-uf2
 ┣ 📂 input_files/            # Carpeta donde se guardarán los archivos .py antes de la conversión
 ┣ 📂 converted_files/        # Carpeta donde se guardarán los archivos .uf2
 ┣ 📂 resources/              # Carpeta de recursos del frontend
 ┣ 📂 tools/                  # Carpeta con herramientas necesarias
 ┣ 📜 .gitignore              # Ignora archivos innecesarios
 ┣ 📜 requirements.txt        # Dependencias del proyecto
 ┣ 📜 convert.py              # Script de conversión
 ┣ 📜 prepare.sh              # Script de instalación.
 ┣ 📜 main.py                 # Servidor FastAPI
 ┣ 📜 index.html              # Frontend para manejar el convertidor
 ```

## 📥 Instalación y Configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Zyrakk/py-to-uf2.git
cd py-to-uf2
```

### 2️⃣ Dar permisos
Añade los siguientes permisos para utilizar los scripts y que la API sea accesible desde una web Apache/Nginx:
```bash
sudo chown -R www-data:www-data /ruta/py-to-uf2
sudo chmod +x prepare.sh main.py convert.py
```

### 3️⃣ Ejecutar el script de instalación
Ejecuta el siguiente comando para configurar el entorno:
```bash
./prepare.sh
```

Este script realizará automáticamente las siguientes acciones:
- Creará las carpetas necesarias (`input_files/`, `converted_files/` y `tools/`).
- Configurará un entorno virtual (`venv/`).
- Instalará todas las dependencias en el entorno virtual.
- Descargará `uf2conv.py` y `uf2families.json` en la carpeta `tools/`.

---

# Instalación de `mpy-cross`

Para convertir archivos `.py` en `.mpy`, es necesario instalar y compilar `mpy-cross`. Sigue estos pasos:

## 1️⃣ **Clonar el repositorio de MicroPython**
```bash
git clone https://github.com/micropython/micropython.git
```

## 2️⃣ **Compilar `mpy-cross`**
```bash
cd micropython/mpy-cross
make clean
make -j$(nproc)  # Usa todos los núcleos disponibles para compilar más rápido
```

## 3️⃣ **Mover `mpy-cross` a `/usr/local/bin/`**
```bash
sudo mv mpy-cross /usr/local/bin/mpy-cross
sudo chmod +x /usr/local/bin/mpy-cross
```

## 4️⃣ **Verificar que la instalación fue exitosa**
```bash
mpy-cross --help
```
Si muestra la ayuda de `mpy-cross`, la instalación fue exitosa.

---

# 🛠 **Corrección de Intérprete en `mpy-cross`**
Si al ejecutar `mpy-cross --help` aparece un error con el intérprete de Python, sigue estos pasos:

## 1️⃣ **Verificar la primera línea del archivo ejecutable:**
```bash
head -n 1 /usr/local/bin/mpy-cross
```
Si muestra:
```
#!/root/mpy-env/bin/python3
```
Entonces es necesario corregir el intérprete.

## 2️⃣ **Editar el archivo `mpy-cross`**:
```bash
sudo nano /usr/local/bin/mpy-cross
```
Cambia la primera línea:
```bash
#!/root/mpy-env/bin/python3
```
Por:
```bash
#!/usr/bin/python3
```
Guarda y sal (`CTRL + X`, luego `Y` y `Enter`).

## 3️⃣ **Verificar que `mpy-cross` funciona correctamente:**
```bash
mpy-cross --help
```
Si muestra la ayuda correctamente, la instalación está lista.

---

## 🚀 Uso

### 🔹 Convertir un archivo `.py` a `.uf2`
```bash
echo "print('Hello, CircuitPython!')" > input_files/test.py
python tools/uf2conv.py --output converted_files/test.uf2 input_files/test.py
```

El archivo convertido se guardará en la carpeta `converted_files/`.

---

✅ **El sistema ya está listo para integrar con FastAPI.** 🚀

