import tkinter as tk
from tkinter import ttk

from clientes import clientes
from ventas import ventas
from cliente_resumen import calcular_resumen_cliente


# ==================================================
# COLORES
# ==================================================

FONDO = "#0B1220"
PANEL = "#111C2E"
PANEL_SECUNDARIO = "#162238"
BORDE = "#24344D"

TEXTO = "#F4F7FB"
TEXTO_SECUNDARIO = "#8FA3BF"

AZUL = "#3B82F6"
VERDE = "#22C55E"
AMARILLO = "#F59E0B"
ROJO = "#EF4444"
CYAN = "#06B6D4"


def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def abrir_resumen_cliente(ventana_padre):
    v = tk.Toplevel(ventana_padre)

    v.title(
        "AI Business Assistant - Resumen por cliente"
    )

    v.geometry(
        "980x760"
    )

    v.minsize(
        820,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    # ==================================================
    # SCROLL GENERAL
    # ==================================================

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True
    )

    canvas_principal = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas_principal.yview
    )

    contenido_principal = tk.Frame(
        canvas_principal,
        bg=FONDO
    )

    ventana_canvas = canvas_principal.create_window(
        (0, 0),
        window=contenido_principal,
        anchor="nw"
    )

    contenido_principal.bind(
        "<Configure>",
        lambda e: canvas_principal.configure(
            scrollregion=canvas_principal.bbox(
                "all"
            )
        )
    )

    def ajustar_ancho(event):
        canvas_principal.itemconfigure(
            ventana_canvas,
            width=event.width
        )

    canvas_principal.bind(
        "<Configure>",
        ajustar_ancho
    )

    canvas_principal.configure(
        yscrollcommand=scrollbar.set
    )

    canvas_principal.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def mover_rueda(event):
        canvas_principal.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas_principal.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    # ==================================================
    # ENCABEZADO
    # ==================================================

    encabezado = tk.Frame(
        contenido_principal,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(25, 15)
    )

    tk.Label(
        encabezado,
        text="CLIENT INTELLIGENCE",
        font=(
            "Segoe UI",
            22,
            "bold"
        ),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text="Customer financial and sales overview",
        font=(
            "Segoe UI",
            10
        ),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    # ==================================================
    # SELECTOR
    # ==================================================

    panel_selector = tk.Frame(
        contenido_principal,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_selector.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    tk.Label(
        panel_selector,
        text="SELECT CLIENT",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )

    opciones_clientes = [
        cliente.get(
            "nombre",
            ""
        )
        for cliente in clientes
        if cliente.get(
            "nombre",
            ""
        )
    ]

    combo_cliente = ttk.Combobox(
        panel_selector,
        values=opciones_clientes,
        state="readonly",
        width=45
    )

    combo_cliente.pack(
        anchor="w",
        padx=20,
        pady=(0, 15)
    )

    # ==================================================
    # KPIs
    # ==================================================

    marco_kpis = tk.Frame(
        contenido_principal,
        bg=FONDO
    )

    marco_kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    etiquetas = {}

    def crear_kpi(
        columna,
        titulo,
        clave,
        color
    ):
        tarjeta = tk.Frame(
            marco_kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            width=210,
            height=100
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(
            False
        )

        marco_kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        contenido = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=12
        )

        tk.Label(
            contenido,
            text=titulo,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w"
        )

        valor = tk.Label(
            contenido,
            text="$0.00",
            font=(
                "Segoe UI",
                17,
                "bold"
            ),
            bg=PANEL,
            fg=TEXTO
        )

        valor.pack(
            anchor="w",
            pady=(6, 0)
        )

        etiquetas[
            clave
        ] = valor

    crear_kpi(
        0,
        "TOTAL PURCHASED",
        "total_comprado",
        AZUL
    )

    crear_kpi(
        1,
        "KNOWN PROFIT",
        "ganancia_conocida",
        VERDE
    )

    crear_kpi(
        2,
        "CREDIT SALES",
        "total_credito",
        AMARILLO
    )

    crear_kpi(
        3,
        "BALANCE DUE",
        "saldo_pendiente",
        CYAN
    )

    # ==================================================
    # INFORMACIÓN DEL CLIENTE
    # ==================================================

    panel_info = tk.Frame(
        contenido_principal,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_info.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    tk.Label(
        panel_info,
        text="CLIENT SUMMARY",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    etiqueta_cliente = tk.Label(
        panel_info,
        text="Cliente: -",
        bg=PANEL,
        fg=TEXTO_SECUNDARIO,
        font=("Segoe UI", 10)
    )

    etiqueta_cliente.pack(
        anchor="w",
        padx=20,
        pady=3
    )

    etiqueta_ventas = tk.Label(
        panel_info,
        text="Número de ventas: 0",
        bg=PANEL,
        fg=TEXTO_SECUNDARIO,
        font=("Segoe UI", 10)
    )

    etiqueta_ventas.pack(
        anchor="w",
        padx=20,
        pady=3
    )

    etiqueta_pagado = tk.Label(
        panel_info,
        text="Total pagado: $0.00",
        bg=PANEL,
        fg=TEXTO_SECUNDARIO,
        font=("Segoe UI", 10)
    )

    etiqueta_pagado.pack(
        anchor="w",
        padx=20,
        pady=(3, 15)
    )

    # ==================================================
    # HISTORIAL
    # ==================================================

    panel_historial = tk.Frame(
        contenido_principal,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_historial.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    tk.Label(
        panel_historial,
        text="DETAILED SALES HISTORY",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    contenido_historial = tk.Frame(
        panel_historial,
        bg=PANEL
    )

    contenido_historial.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )

    def mostrar_historial(nombre):
        for widget in (
            contenido_historial.winfo_children()
        ):
            widget.destroy()

        ventas_cliente = []

        for venta in ventas:
            cliente_venta = str(
                venta.get(
                    "cliente",
                    ""
                )
            ).strip()

            if (
                cliente_venta.lower()
                == nombre.lower()
            ):
                ventas_cliente.append(
                    venta
                )

        if not ventas_cliente:
            tk.Label(
                contenido_historial,
                text=(
                    "No hay ventas registradas "
                    "para este cliente."
                ),
                bg=PANEL,
                fg=TEXTO_SECUNDARIO,
                font=("Segoe UI", 10)
            ).pack(
                anchor="w",
                padx=10,
                pady=10
            )

            return

        for numero, venta in enumerate(
            ventas_cliente,
            start=1
        ):
            monto = convertir_numero(
                venta.get(
                    "monto",
                    0
                )
            )

            cantidad = venta.get(
                "cantidad",
                1
            )

            producto = venta.get(
                "producto",
                "Sin producto"
            )

            codigo = (
                venta.get(
                    "codigo_producto",
                    ""
                )
                or "SIN CÓDIGO"
            )

            fecha = venta.get(
                "fecha",
                "Sin fecha"
            )

            tipo_pago = venta.get(
                "tipo_pago",
                "No registrado"
            )

            tarjeta = tk.Frame(
                contenido_historial,
                bg=PANEL_SECUNDARIO,
                highlightbackground=BORDE,
                highlightthickness=1
            )

            tarjeta.pack(
                fill="x",
                padx=5,
                pady=6
            )

            encabezado_venta = tk.Frame(
                tarjeta,
                bg=PANEL_SECUNDARIO
            )

            encabezado_venta.pack(
                fill="x",
                padx=15,
                pady=(12, 5)
            )

            tk.Label(
                encabezado_venta,
                text=f"SALE #{numero}",
                font=(
                    "Segoe UI",
                    10,
                    "bold"
                ),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO
            ).pack(
                side="left"
            )

            tk.Label(
                encabezado_venta,
                text=f"${monto:.2f}",
                font=(
                    "Segoe UI",
                    11,
                    "bold"
                ),
                bg=PANEL_SECUNDARIO,
                fg=VERDE
            ).pack(
                side="right"
            )

            texto = (
                f"Fecha: {fecha}\n"
                f"Código: {codigo}\n"
                f"Producto: {producto}\n"
                f"Cantidad: {cantidad}\n"
                f"Tipo de pago: {tipo_pago}"
            )

            tk.Label(
                tarjeta,
                text=texto,
                justify="left",
                bg=PANEL_SECUNDARIO,
                fg=TEXTO_SECUNDARIO,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 12)
            )

    def mostrar_resumen(event=None):
        nombre = (
            combo_cliente.get()
            .strip()
        )

        if not nombre:
            return

        resumen = calcular_resumen_cliente(
            nombre
        )

        etiqueta_cliente.config(
            text=(
                f"Cliente: "
                f"{resumen['cliente']}"
            )
        )

        etiqueta_ventas.config(
            text=(
                f"Número de ventas: "
                f"{resumen['cantidad_ventas']}"
            )
        )

        etiqueta_pagado.config(
            text=(
                f"Total pagado: "
                f"${resumen['total_pagado']:.2f}"
            )
        )

        etiquetas[
            "total_comprado"
        ].config(
            text=(
                f"${resumen['total_comprado']:.2f}"
            )
        )

        etiquetas[
            "ganancia_conocida"
        ].config(
            text=(
                f"${resumen['ganancia_conocida']:.2f}"
            )
        )

        etiquetas[
            "total_credito"
        ].config(
            text=(
                f"${resumen['total_credito']:.2f}"
            )
        )

        etiquetas[
            "saldo_pendiente"
        ].config(
            text=(
                f"${resumen['saldo_pendiente']:.2f}"
            )
        )

        mostrar_historial(
            nombre
        )

    combo_cliente.bind(
        "<<ComboboxSelected>>",
        mostrar_resumen
    )

    # ==================================================
    # PIE
    # ==================================================

    pie = tk.Frame(
        contenido_principal,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 25)
    )

    def cerrar():
        canvas_principal.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text="Close",
        width=16,
        command=cerrar,
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2"
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )