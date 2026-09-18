import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from configuracion_negocio import (
    cargar_datos_negocio,
    guardar_datos_negocio,
    validar_datos_negocio,
    MONEDAS_PERMITIDAS,
)


def abrir_configuracion_negocio(ventana_padre=None):
    # ==========================================
    # COLORES
    # ==========================================
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    ROJO = "#EF4444"

    # ==========================================
    # VENTANA
    # ==========================================
    if ventana_padre is not None:
        ventana = tk.Toplevel(ventana_padre)
    else:
        ventana = tk.Tk()

    ventana.title(
        "AI Business Assistant - Configuración del negocio"
    )

    ventana.geometry(
        "850x760"
    )

    ventana.minsize(
        760,
        650
    )

    ventana.configure(
        bg=FONDO
    )

    # ==========================================
    # DATOS ACTUALES
    # ==========================================
    datos = cargar_datos_negocio()

    # ==========================================
    # ENCABEZADO
    # ==========================================
    encabezado = tk.Frame(
        ventana,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=35,
        pady=(28, 15)
    )

    tk.Label(
        encabezado,
        text="CONFIGURACIÓN DEL NEGOCIO",
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=(
            "Personalizá la información que identifica "
            "tu negocio en el sistema y en los recibos."
        ),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    # ==========================================
    # SCROLL
    # ==========================================
    marco_scroll = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=(0, 15)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(
            ventana_canvas,
            width=event.width
        )
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def mover_rueda(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    # ==========================================
    # PANEL PRINCIPAL
    # ==========================================
    panel = tk.Frame(
        contenido,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        panel,
        text="INFORMACIÓN DEL NEGOCIO",
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=24,
        pady=(22, 5)
    )

    tk.Label(
        panel,
        text=(
            "Estos datos podrán aparecer en documentos "
            "y recibos generados por la aplicación."
        ),
        font=("Segoe UI", 9),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=24,
        pady=(0, 20)
    )

    formulario = tk.Frame(
        panel,
        bg=PANEL
    )

    formulario.pack(
        fill="x",
        padx=24,
        pady=(0, 24)
    )

    formulario.grid_columnconfigure(
        0,
        weight=1
    )

    formulario.grid_columnconfigure(
        1,
        weight=1
    )

    # ==========================================
    # VARIABLES
    # ==========================================
    variable_nombre = tk.StringVar(
        value=datos.get("nombre", "")
    )

    variable_telefono = tk.StringVar(
        value=datos.get("telefono", "")
    )

    variable_correo = tk.StringVar(
        value=datos.get("correo", "")
    )

    variable_direccion = tk.StringVar(
        value=datos.get("direccion", "")
    )

    variable_tax_id = tk.StringVar(
        value=datos.get("tax_id", "")
    )

    variable_logo = tk.StringVar(
        value=datos.get("logo", "")
    )

    variable_moneda = tk.StringVar(
        value=datos.get("moneda", "USD")
    )

    variable_idioma = tk.StringVar(
        value=datos.get("idioma", "es")
    )

    # ==========================================
    # FUNCIONES DE CAMPOS
    # ==========================================
    def crear_campo(
        fila,
        columna,
        titulo,
        variable,
        ancho_columnas=1
    ):
        contenedor = tk.Frame(
            formulario,
            bg=PANEL
        )

        contenedor.grid(
            row=fila,
            column=columna,
            columnspan=ancho_columnas,
            sticky="ew",
            padx=6,
            pady=8
        )

        tk.Label(
            contenedor,
            text=titulo,
            font=("Segoe UI", 9, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        entrada = tk.Entry(
            contenedor,
            textvariable=variable,
            font=("Segoe UI", 10),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO,
            insertbackground=TEXTO,
            relief="flat",
            bd=0
        )

        entrada.pack(
            fill="x",
            ipady=9
        )

        return entrada

    # ==========================================
    # CAMPOS
    # ==========================================
    entrada_nombre = crear_campo(
        0,
        0,
        "Nombre del negocio *",
        variable_nombre,
        2
    )

    crear_campo(
        1,
        0,
        "Teléfono",
        variable_telefono
    )

    crear_campo(
        1,
        1,
        "Correo electrónico",
        variable_correo
    )

    crear_campo(
        2,
        0,
        "Dirección",
        variable_direccion,
        2
    )

    crear_campo(
        3,
        0,
        "Tax ID / EIN (opcional)",
        variable_tax_id,
        2
    )

    # ==========================================
    # LOGO
    # ==========================================
    contenedor_logo = tk.Frame(
        formulario,
        bg=PANEL
    )

    contenedor_logo.grid(
        row=4,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=6,
        pady=8
    )

    tk.Label(
        contenedor_logo,
        text="Logo del negocio",
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(0, 6)
    )

    fila_logo = tk.Frame(
        contenedor_logo,
        bg=PANEL
    )

    fila_logo.pack(
        fill="x"
    )

    entrada_logo = tk.Entry(
        fila_logo,
        textvariable=variable_logo,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        insertbackground=TEXTO,
        relief="flat",
        bd=0
    )

    entrada_logo.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=9
    )

    def seleccionar_logo():
        ruta = filedialog.askopenfilename(
            parent=ventana,
            title="Seleccionar logo",
            filetypes=[
                (
                    "Imágenes",
                    "*.png *.jpg *.jpeg"
                ),
                (
                    "PNG",
                    "*.png"
                ),
                (
                    "JPEG",
                    "*.jpg *.jpeg"
                ),
                (
                    "Todos los archivos",
                    "*.*"
                )
            ]
        )

        if ruta:
            variable_logo.set(
                str(Path(ruta))
            )

    tk.Button(
        fila_logo,
        text="Seleccionar",
        command=seleccionar_logo,
        font=("Segoe UI", 9, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=16,
        pady=8
    ).pack(
        side="left",
        padx=(10, 0)
    )

    # ==========================================
    # MONEDA E IDIOMA
    # ==========================================
    contenedor_moneda = tk.Frame(
        formulario,
        bg=PANEL
    )

    contenedor_moneda.grid(
        row=5,
        column=0,
        sticky="ew",
        padx=6,
        pady=8
    )

    tk.Label(
        contenedor_moneda,
        text="Moneda",
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(0, 6)
    )

    combo_moneda = ttk.Combobox(
        contenedor_moneda,
        textvariable=variable_moneda,
        values=list(
            MONEDAS_PERMITIDAS.keys()
        ),
        state="readonly",
        font=("Segoe UI", 10)
    )

    combo_moneda.pack(
        fill="x",
        ipady=5
    )

    contenedor_idioma = tk.Frame(
        formulario,
        bg=PANEL
    )

    contenedor_idioma.grid(
        row=5,
        column=1,
        sticky="ew",
        padx=6,
        pady=8
    )

    tk.Label(
        contenedor_idioma,
        text="Idioma predeterminado",
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(0, 6)
    )

    combo_idioma = ttk.Combobox(
        contenedor_idioma,
        textvariable=variable_idioma,
        values=[
            "es",
            "en"
        ],
        state="readonly",
        font=("Segoe UI", 10)
    )

    combo_idioma.pack(
        fill="x",
        ipady=5
    )

    # ==========================================
    # INFORMACIÓN ADICIONAL
    # ==========================================
    panel_info = tk.Frame(
        contenido,
        bg=PANEL_SECUNDARIO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_info.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        panel_info,
        text="PERSONALIZACIÓN",
        font=("Segoe UI", 10, "bold"),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(16, 5)
    )

    tk.Label(
        panel_info,
        text=(
            "La moneda seleccionada se utilizará como "
            "preferencia del negocio. El idioma define "
            "la configuración predeterminada para futuras "
            "funciones y documentos."
        ),
        justify="left",
        wraplength=650,
        font=("Segoe UI", 9),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=20,
        pady=(0, 16)
    )

    # ==========================================
    # GUARDAR
    # ==========================================
    def guardar():
        nuevos_datos = {
            "nombre": variable_nombre.get(),
            "telefono": variable_telefono.get(),
            "correo": variable_correo.get(),
            "direccion": variable_direccion.get(),
            "tax_id": variable_tax_id.get(),
            "logo": variable_logo.get(),
            "moneda": variable_moneda.get(),
            "idioma": variable_idioma.get(),
        }

        errores = validar_datos_negocio(
            nuevos_datos
        )

        if errores:
            messagebox.showerror(
                "Datos incorrectos",
                "\n".join(errores),
                parent=ventana
            )
            return

        try:
            guardados = guardar_datos_negocio(
                nuevos_datos
            )

            variable_nombre.set(
                guardados["nombre"]
            )

            variable_telefono.set(
                guardados["telefono"]
            )

            variable_correo.set(
                guardados["correo"]
            )

            variable_direccion.set(
                guardados["direccion"]
            )

            variable_tax_id.set(
                guardados["tax_id"]
            )

            variable_logo.set(
                guardados["logo"]
            )

            variable_moneda.set(
                guardados["moneda"]
            )

            variable_idioma.set(
                guardados["idioma"]
            )

            messagebox.showinfo(
                "Configuración guardada",
                (
                    "Los datos del negocio fueron "
                    "guardados correctamente."
                ),
                parent=ventana
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                (
                    "No se pudo guardar la configuración."
                    f"\n\n{error}"
                ),
                parent=ventana
            )

    # ==========================================
    # BOTONES
    # ==========================================
    botones = tk.Frame(
        contenido,
        bg=FONDO
    )

    botones.pack(
        fill="x",
        pady=(0, 25)
    )

    tk.Button(
        botones,
        text="Guardar configuración",
        command=guardar,
        font=("Segoe UI", 10, "bold"),
        bg=VERDE,
        fg="white",
        activebackground="#16A34A",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=10
    ).pack(
        side="left"
    )

    tk.Button(
        botones,
        text="Cerrar",
        command=ventana.destroy,
        font=("Segoe UI", 10, "bold"),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=10
    ).pack(
        side="right"
    )

    entrada_nombre.focus_set()

    if ventana_padre is None:
        ventana.mainloop()


if __name__ == "__main__":
    abrir_configuracion_negocio()