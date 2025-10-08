# 🎮 Duplicate Mod Cleaner v2.0

Una herramienta simple y elegante creada en **Python** para ayudar a los jugadores de **Los Sims 4** (o a cualquiera con muchos archivos) a **encontrar y mover mods duplicados automáticamente**.  
Diseñada con 💙 usando **CustomTkinter**.

---

## ✨ Características

- 🧠 Detecta duplicados mediante **comparación de hash SHA1**  
- 📦 Mueve **toda la carpeta** que contiene los archivos duplicados a una nueva carpeta llamada `Duplicados`  
- ⏱️ Muestra una **barra de progreso en tiempo real** durante la búsqueda  
- 🔔 Reproduce un **sonido de campana** al finalizar  
- 🖤 Interfaz moderna con **CustomTkinter**

---

## 🚀 Cómo usar

1. Selecciona tu carpeta de **Mods**  
2. Haz clic en **“Buscar y mover duplicados”**  
3. Espera mientras el programa escanea (verás el cronómetro en tiempo real)  
4. Al finalizar:
   - Escucharás una **campanita**
   - Verás cuánto tiempo tomó el proceso
   - Las carpetas duplicadas se moverán a **“Duplicados”**

---

## 🧩 Instalación

```bash
git clone https://github.com/DNSKT/Sims-4-Duplicate-Mod-Cleaner.git
cd Sims-4-Duplicate-Mod-Cleaner
pip install customtkinter
python Duplicate Mod Cleaner.py
````

---

## 🧰 Crear un ejecutable (.EXE)

Si deseas generar un archivo ejecutable para Windows:

```bash
python -m PyInstaller --onefile --noconsole Duplicate Mod Cleaner.py
```

El archivo final estará dentro de la carpeta **/dist**.

---

## 💡 Tecnologías utilizadas

* Python 3.10+
* CustomTkinter
* Hashlib
* Winsound (para la campana al finalizar)
* PyInstaller (para crear el .exe)
