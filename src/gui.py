"""
KotlinScope - Interfaz gráfica (Tkinter)
Proyecto Lenguajes de Programación - Avance final

Editor de código a la izquierda y resultados a la derecha.
Cada análisis tiene su botón y su color, y guarda su log en la carpeta logs/.

Uso:
    python main.py
"""

import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from src import lexer as analizador_lexico
from src import parser as analizador_sintactico

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_ALGORITMOS = RAIZ_PROYECTO / "algoritmos"

USUARIOS = ["mateoandraded", "alan-am", "danx111"]

# cada fase tiene su color y se repite en botones y mensajes
COLORES = {
    "Léxico": "#2563eb",
    "Sintáctico": "#d97706",
    "Semántico": "#7c3aed",
}
COLOR_OK = "#15803d"
COLOR_ERROR = "#b91c1c"
FONDO_LINEA_ERROR = "#fde2e2"
FONDO_LINEA_ELEGIDA = "#f9a8a8"
FUENTE_CODIGO = ("Consolas", 11)


# saco el número de línea de un mensaje como "... en la línea 12"
def linea_del_error(mensaje):
    encontrado = re.search(r"l[ií]nea (\d+)", mensaje)
    return int(encontrado.group(1)) if encontrado else None


class VentanaAnalizador:
    def __init__(self, raiz):
        self.raiz = raiz
        self.archivo_actual = None
        self.raiz.title("KotlinScope - Analizador de Kotlin")
        self.raiz.geometry("1280x760")
        self.raiz.minsize(960, 560)

        self.crear_barra_superior()
        self.crear_paneles()
        self.crear_barra_estado()
        self.actualizar_numeros()

    # ------------------------------------------------------------------
    # armado de la ventana
    # ------------------------------------------------------------------

    def crear_barra_superior(self):
        barra = tk.Frame(self.raiz, padx=10, pady=8)
        barra.pack(side="top", fill="x")

        tk.Button(barra, text="Abrir .kt", command=self.abrir_archivo, padx=10).pack(side="left")
        tk.Button(barra, text="Limpiar", command=self.limpiar, padx=10).pack(side="left", padx=(6, 0))

        tk.Label(barra, text="Algoritmo:").pack(side="left", padx=(14, 4))
        self.lista_algoritmos = ttk.Combobox(barra, state="readonly", width=26, values=self.algoritmos_de_prueba())
        self.lista_algoritmos.pack(side="left")
        self.lista_algoritmos.bind("<<ComboboxSelected>>", self.cargar_algoritmo)

        tk.Label(barra, text="Usuario:").pack(side="left", padx=(14, 4))
        self.usuario = ttk.Combobox(barra, width=15, values=USUARIOS)
        self.usuario.set(USUARIOS[0])
        self.usuario.pack(side="left")

        for fase, accion in (
            ("Semántico", self.analizar_semantico),
            ("Sintáctico", self.analizar_sintactico),
            ("Léxico", self.analizar_lexico),
        ):
            tk.Button(
                barra,
                text=f"▶ {fase}",
                command=accion,
                bg=COLORES[fase],
                fg="white",
                activebackground=COLORES[fase],
                activeforeground="white",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                padx=12,
                pady=4,
                cursor="hand2",
            ).pack(side="right", padx=(6, 0))

    def crear_paneles(self):
        paneles = tk.PanedWindow(self.raiz, orient="horizontal", sashwidth=6)
        paneles.pack(side="top", fill="both", expand=True, padx=10)

        # editor con números de línea
        marco_editor = tk.Frame(paneles)
        tk.Label(marco_editor, text="Código Kotlin", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill="x")
        contenedor = tk.Frame(marco_editor, bd=1, relief="solid")
        contenedor.pack(fill="both", expand=True)

        self.numeros = tk.Canvas(contenedor, width=44, bg="#f3f4f6", highlightthickness=0)
        self.numeros.pack(side="left", fill="y")
        barra_vertical = tk.Scrollbar(contenedor, orient="vertical", command=self.mover_editor)
        barra_vertical.pack(side="right", fill="y")
        self.editor = tk.Text(
            contenedor,
            font=FUENTE_CODIGO,
            undo=True,
            wrap="none",
            tabs=("1c",),
            padx=6,
            yscrollcommand=lambda *args: self.al_mover_editor(barra_vertical, *args),
        )
        self.editor.pack(side="left", fill="both", expand=True)
        self.editor.tag_configure("linea_error", background=FONDO_LINEA_ERROR)
        self.editor.tag_configure("linea_elegida", background=FONDO_LINEA_ELEGIDA)
        self.editor.tag_raise("linea_elegida")
        self.editor.bind("<KeyRelease>", lambda e: self.actualizar_numeros())
        self.editor.bind("<Tab>", self.insertar_tab)
        paneles.add(marco_editor, minsize=420, width=640)

        # resultados en pestañas
        marco_resultados = tk.Frame(paneles)
        tk.Label(marco_resultados, text="Resultados", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill="x")
        self.pestanas = ttk.Notebook(marco_resultados)
        self.pestanas.pack(fill="both", expand=True)

        self.tabla_errores = self.crear_tabla(("Fase", "Línea", "Mensaje"), (90, 60, 520))
        for fase, color in COLORES.items():
            self.tabla_errores.tag_configure(fase, foreground=color)
        self.tabla_errores.bind("<<TreeviewSelect>>", self.ir_a_error)
        self.detalle_error = tk.Label(
            self.tabla_errores.master, text="Haz clic en un error para ver su línea en el editor.",
            anchor="w", justify="left", wraplength=560, padx=6, pady=6, bg="#f9fafb",
        )
        self.detalle_error.pack(side="bottom", fill="x", before=self.tabla_errores.master.pack_slaves()[0])
        self.tabla_tokens = self.crear_tabla(("Línea", "Tipo", "Valor"), (60, 180, 300))
        self.texto_log = tk.Text(self.pestanas, font=("Consolas", 10), wrap="word", state="disabled")

        self.pestanas.add(self.tabla_errores.master, text="Errores")
        self.pestanas.add(self.tabla_tokens.master, text="Tokens")
        self.pestanas.add(self.texto_log, text="Log")
        paneles.add(marco_resultados, minsize=380)

    def crear_tabla(self, columnas, anchos):
        marco = tk.Frame(self.pestanas)
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for columna, ancho in zip(columnas, anchos):
            tabla.heading(columna, text=columna, anchor="w")
            tabla.column(columna, width=ancho, anchor="w", stretch=(columna == columnas[-1]))
        barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        tabla.pack(fill="both", expand=True)
        return tabla

    def crear_barra_estado(self):
        barra = tk.Frame(self.raiz, bd=1, relief="sunken")
        barra.pack(side="bottom", fill="x")
        self.estado = tk.Label(barra, text="Escribe o abre un archivo .kt y elige un análisis.", anchor="w", padx=8, pady=4)
        self.estado.pack(side="left", fill="x", expand=True)
        self.ruta_log = tk.Label(barra, text="", anchor="e", padx=8, fg="#4b5563")
        self.ruta_log.pack(side="right")

    # ------------------------------------------------------------------
    # editor
    # ------------------------------------------------------------------

    def mover_editor(self, *args):
        self.editor.yview(*args)
        self.actualizar_numeros()

    def al_mover_editor(self, barra, *args):
        barra.set(*args)
        self.actualizar_numeros()

    def actualizar_numeros(self):
        self.numeros.delete("all")
        indice = self.editor.index("@0,0")
        while True:
            caja = self.editor.dlineinfo(indice)
            if caja is None:
                break
            numero = indice.split(".")[0]
            self.numeros.create_text(38, caja[1], anchor="ne", text=numero, font=FUENTE_CODIGO, fill="#6b7280")
            indice = self.editor.index(f"{indice}+1line")
            if indice == self.editor.index("end"):
                break

    def insertar_tab(self, evento):
        self.editor.insert("insert", "    ")
        return "break"

    def codigo(self):
        return self.editor.get("1.0", "end-1c")

    def poner_codigo(self, texto):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", texto)
        self.limpiar_resultados()
        self.actualizar_numeros()

    def algoritmos_de_prueba(self):
        return sorted(ruta.name for ruta in CARPETA_ALGORITMOS.glob("*.kt"))

    def cargar_algoritmo(self, evento=None):
        ruta = CARPETA_ALGORITMOS / self.lista_algoritmos.get()
        self.archivo_actual = ruta
        self.poner_codigo(ruta.read_text(encoding="utf-8-sig"))
        self.mostrar_estado(f"Archivo cargado: {ruta.name}", "#111827")

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            initialdir=CARPETA_ALGORITMOS,
            filetypes=[("Kotlin", "*.kt"), ("Todos", "*.*")],
        )
        if ruta:
            self.archivo_actual = Path(ruta)
            self.poner_codigo(self.archivo_actual.read_text(encoding="utf-8-sig"))
            self.mostrar_estado(f"Archivo cargado: {self.archivo_actual.name}", "#111827")

    def limpiar(self):
        self.archivo_actual = None
        self.lista_algoritmos.set("")
        self.poner_codigo("")
        self.mostrar_estado("Editor vacío.", "#111827")

    # ------------------------------------------------------------------
    # análisis
    # ------------------------------------------------------------------

    def nombre_usuario(self):
        return self.usuario.get().strip() or "anonimo"

    def nombre_archivo(self):
        return self.archivo_actual.name if self.archivo_actual else "codigo del editor"

    def analizar_lexico(self):
        tokens, errores = analizador_lexico.analizar(self.codigo())
        ruta = analizador_lexico.generar_log(self.nombre_usuario(), tokens, errores, self.nombre_archivo())
        self.mostrar_resultados("Léxico", tokens, [("Léxico", e) for e in errores], ruta)

    def analizar_sintactico(self):
        codigo = self.codigo()
        tokens, _ = analizador_lexico.analizar(codigo)
        lexicos, sintacticos = analizador_sintactico.analizar(codigo)
        ruta = analizador_sintactico.generar_log_sintactico(
            self.nombre_usuario(), lexicos, sintacticos, self.nombre_archivo()
        )
        errores = [("Léxico", e) for e in lexicos] + [("Sintáctico", e) for e in sintacticos]
        self.mostrar_resultados("Sintáctico", tokens, errores, ruta)

    def analizar_semantico(self):
        codigo = self.codigo()
        tokens, _ = analizador_lexico.analizar(codigo)
        lexicos, sintacticos, semanticos = analizador_sintactico.analizar_semantico(codigo)
        ruta = analizador_sintactico.generar_log_semantico(self.nombre_usuario(), semanticos, self.nombre_archivo())
        errores = (
            [("Léxico", e) for e in lexicos]
            + [("Sintáctico", e) for e in sintacticos]
            + [("Semántico", e) for e in semanticos]
        )
        self.mostrar_resultados("Semántico", tokens, errores, ruta)

    # ------------------------------------------------------------------
    # resultados
    # ------------------------------------------------------------------

    def limpiar_resultados(self):
        self.tabla_errores.delete(*self.tabla_errores.get_children())
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        self.editor.tag_remove("linea_error", "1.0", "end")
        self.editor.tag_remove("linea_elegida", "1.0", "end")
        self.escribir_log("")
        self.ruta_log.config(text="")
        self.detalle_error.config(text="Haz clic en un error para ver su línea en el editor.", fg="#111827")

    def mostrar_resultados(self, fase, tokens, errores, ruta_log):
        self.limpiar_resultados()

        for tok in tokens:
            self.tabla_tokens.insert("", "end", values=(tok.lineno, tok.type, repr(tok.value)))

        errores = sorted(errores, key=lambda par: linea_del_error(par[1]) or 0)
        for fase_error, mensaje in errores:
            linea = linea_del_error(mensaje)
            self.tabla_errores.insert("", "end", values=(fase_error, linea or "-", mensaje), tags=(fase_error,))
            if linea:
                self.editor.tag_add("linea_error", f"{linea}.0", f"{linea}.0 lineend+1c")

        self.escribir_log(Path(ruta_log).read_text(encoding="utf-8"))
        self.ruta_log.config(text=f"Log: logs/{Path(ruta_log).name}")

        if errores:
            self.pestanas.select(0)
            lineas = sorted({linea_del_error(m) for _, m in errores if linea_del_error(m)})
            texto_lineas = ", ".join(str(n) for n in lineas[:8]) + ("…" if len(lineas) > 8 else "")
            self.mostrar_estado(
                f"✖ Análisis {fase.lower()}: {len(errores)} error(es) en las líneas {texto_lineas}",
                COLOR_ERROR,
            )
        else:
            self.pestanas.select(1 if fase == "Léxico" else 0)
            self.mostrar_estado(f"✔ Análisis {fase.lower()}: el código es válido ({len(tokens)} tokens)", COLOR_OK)

    def escribir_log(self, texto):
        self.texto_log.config(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.insert("1.0", texto)
        self.texto_log.config(state="disabled")

    def mostrar_estado(self, texto, color):
        self.estado.config(text=texto, fg=color)

    # al hacer clic en un error marco su línea en el editor
    def ir_a_error(self, evento=None):
        seleccion = self.tabla_errores.selection()
        if not seleccion:
            return
        fase, _, mensaje = self.tabla_errores.item(seleccion[0], "values")
        self.detalle_error.config(text=mensaje, fg=COLORES.get(fase, "#111827"))
        linea = linea_del_error(mensaje)
        if not linea:
            return
        self.editor.tag_remove("linea_elegida", "1.0", "end")
        self.editor.tag_add("linea_elegida", f"{linea}.0", f"{linea}.0 lineend+1c")
        self.editor.see(f"{linea}.0")
        self.editor.mark_set("insert", f"{linea}.0")
        self.actualizar_numeros()


def iniciar():
    # en Windows evito que el texto se vea borroso con la pantalla escalada
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    raiz = tk.Tk()
    VentanaAnalizador(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    iniciar()
