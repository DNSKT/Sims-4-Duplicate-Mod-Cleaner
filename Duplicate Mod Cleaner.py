import hashlib
import shutil
import winsound
from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def calcular_hash(archivo, bloque=65536):
    hash_obj = hashlib.sha1()
    try:
        with open(archivo, "rb") as f:
            while chunk := f.read(bloque):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception:
        return None

def buscar_duplicados(ruta_base, progress_callback=None, running_callback=None):
    archivos_hash = {}
    duplicados = []
    archivos = list(Path(ruta_base).rglob("*"))
    archivos = [f for f in archivos if f.is_file()]

    total = len(archivos)
    for i, archivo in enumerate(archivos):
        if running_callback and not running_callback:
            break

        hash_archivo = calcular_hash(archivo)
        if hash_archivo:
            if hash_archivo in archivos_hash:
                duplicados.append((archivo, archivos_hash[hash_archivo]))
            else:
                archivos_hash[hash_archivo] = archivo
        if progress_callback:
            progress_callback(i + 1, total)

    return duplicados

def obtener_carpetas_duplicadas(duplicados):
    carpetas = set()
    for dup, _ in duplicados:
        carpetas.add(dup.parent)
    return carpetas

def mover_carpetas_duplicadas(carpetas, ruta_base, textbox):
    ruta_base = Path(ruta_base)
    carpeta_destino = ruta_base.parent / "Duplicados"
    carpeta_destino.mkdir(exist_ok=True)

    carpetas_movidas = 0
    for carpeta_mod in carpetas:
        destino = carpeta_destino / carpeta_mod.name
        contador = 1
        while destino.exists():
            destino = carpeta_destino / f"{carpeta_mod.name}_copy{contador}"
            contador += 1

        try:
            shutil.move(str(carpeta_mod), destino)
            carpetas_movidas += 1
            textbox.insert("end", f"📦 Movida carpeta: {carpeta_mod.name}\n")
        except Exception as e:
            textbox.insert("end", f"❌ Error moviendo {carpeta_mod}: {e}\n")

    return carpeta_destino, carpetas_movidas

class DuplicateModCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🧩 Duplicate Mod Cleaner v2 by Souvlaki")
        self.geometry("720x560")
        self.resizable(False, False)

        self.ruta_carpeta = ctk.StringVar(value="")
        self.carpetas_encontradas = set()

        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="🎮 Duplicate Mod Cleaner by Souvlaki", font=("Segoe UI", 24, "bold"))
        title.pack(pady=10)

        desc = ctk.CTkLabel(
            frame,
            text="Detecta mods duplicados en The Sims 4.\nPuedes ver una vista previa antes de moverlos.",
            text_color="gray",
        )
        desc.pack(pady=(0, 10))

        select_btn = ctk.CTkButton(frame, text="📂 Seleccionar carpeta de mods", command=self.seleccionar_carpeta)
        select_btn.pack(pady=10)

        self.label_ruta = ctk.CTkLabel(frame, text="Ninguna carpeta seleccionada", text_color="gray")
        self.label_ruta.pack()

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=15)

        preview_btn = ctk.CTkButton(btn_frame, text="👀 Vista previa", fg_color="#2D9BF0", command=self.vista_previa)
        preview_btn.grid(row=0, column=0, padx=10)

        move_btn = ctk.CTkButton(btn_frame, text="🚚 Mover duplicados", fg_color="green", command=self.mover_duplicados)
        move_btn.grid(row=0, column=1, padx=10)

        self.progressbar = ctk.CTkProgressBar(frame, width=450)
        self.progressbar.set(0)
        self.progressbar.pack(pady=10)

        self.textbox = ctk.CTkTextbox(frame, width=640, height=220)
        self.textbox.pack(pady=5)

        self.label_estado = ctk.CTkLabel(frame, text=" ", text_color="yellow")
        self.label_estado.pack(pady=5)


    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_carpeta.set(carpeta)
            self.label_ruta.configure(text=carpeta, text_color="white")

    def actualizar_progreso(self, actual, total):
        self.progressbar.set(actual / total)
        self.update_idletasks()

    def vista_previa(self):
        ruta = self.ruta_carpeta.get()
        if not ruta:
            self.label_estado.configure(text="⚠️ Selecciona una carpeta primero.", text_color="orange")
            return

        self.textbox.delete("1.0", "end")
        self.label_estado.configure(text="Analizando duplicados...", text_color="yellow")
        self.update()

        duplicados = buscar_duplicados(ruta, self.actualizar_progreso, lambda: self.is_running)
        if not duplicados:
            self.label_estado.configure(text="✅ No se encontraron duplicados.", text_color="green")
            winsound.Beep(1000, 300)
            winsound.Beep(1500, 300)
            return

        carpetas = obtener_carpetas_duplicadas(duplicados)
        self.carpetas_encontradas = carpetas

        self.textbox.insert("end", f"🔎 Se encontraron {len(carpetas)} carpetas duplicadas:\n\n")
        self.is_running=False
        winsound.Beep(1500, 300)
        for carpeta in carpetas:
            self.textbox.insert("end", f"📁 {carpeta}\n")

        self.label_estado.configure(text="👀 Vista previa completa. Revisa las carpetas.", text_color="#00BFFF")

    def mover_duplicados(self):
        if not self.carpetas_encontradas:
            self.label_estado.configure(text="⚠️ Primero haz una vista previa.", text_color="orange")
            return

        ruta = self.ruta_carpeta.get()
        self.textbox.insert("end", "\n🚚 Moviendo carpetas duplicadas...\n\n")
        carpeta_destino, total = mover_carpetas_duplicadas(self.carpetas_encontradas, ruta, self.textbox)

        self.label_estado.configure(
            text=f"🎯 {total} carpetas movidas a: {carpeta_destino}",
            text_color="lightgreen"
            
        )
        self.is_running = False
        winsound.Beep(1000, 300)
        winsound.Beep(1300, 300)
        winsound.Beep(1600, 500)
        self.progressbar.set(0)

if __name__ == "__main__":
    app = DuplicateModCleanerApp()
    app.mainloop()
