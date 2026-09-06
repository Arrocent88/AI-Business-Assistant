import tkinter as tk
from datetime import datetime

from dashboard import calcular_dashboard
from ventas import ventas
from cuentas import cuentas_por_cobrar
from inventario import inventario


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


# ==================================================
# UTILIDADES
# ==================================================

def convertir_numero(valor):
    try:
        return float(
            str(valor)
            .replace("$", "")
            .replace(",", "")
            .strip()
        )
    except (ValueError, TypeError):
        return 0.0


def calcular_alertas():
    pendientes = 0
    vencidas = 0
    proximas = 0
    stock_bajo = 0

    hoy = datetime.now().date()

    for cuenta in cuentas_por_cobrar:
        saldo = convertir_numero(
            cuenta.get(
                "saldo_pendiente",
                0
            )
        )

        if saldo <= 0:
            continue

        pendientes += 1

        fecha_texto = str(
            cuenta.get(
                "fecha_vencimiento",
                ""
            )
        ).strip()

        if fecha_texto:
            try:
                fecha = datetime.strptime(
                    fecha_texto,
                    "%Y-%m-%d"
                ).date()

                dias = (
                    fecha - hoy
                ).days

                if dias < 0:
                    vencidas += 1

                elif dias <= 7:
                    proximas += 1

            except ValueError:
                pass

    for item in inventario:
        cantidad = int(
            item.get(
                "cantidad",
                0
            )
        )

        if cantidad <= 5:
            stock_bajo += 1

    return {
        "pendientes": pendientes,
        "vencidas": vencidas,
        "proximas": proximas,
        "stock_bajo": stock_bajo
    }


def obtener_ventas_por_fecha():
    agrupadas = {}

    for venta in ventas:
        fecha = str(
            venta.get(
                "fecha",
                ""
            )
        ).strip()

        if not fecha:
            continue

        try:
            fecha_obj = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )

        except ValueError:
            continue

        monto = convertir_numero(
            venta.get(
                "monto",
                0
            )
        )

        ganancia = convertir_numero(
            venta.get(
                "ganancia",
                0
            )
        )

        clave = fecha_obj.strftime(
            "%Y-%m-%d"
        )

        if clave not in agrupadas:
            agrupadas[clave] = {
                "ventas": 0,
                "ganancia": 0
            }

        agrupadas[clave]["ventas"] += monto
        agrupadas[clave]["ganancia"] += ganancia

    fechas = sorted(
        agrupadas.keys()
    )

    fechas = fechas[-8:]

    resultado = []

    for fecha in fechas:
        resultado.append({
            "fecha": fecha,
            "ventas": agrupadas[
                fecha
            ]["ventas"],
            "ganancia": agrupadas[
                fecha
            ]["ganancia"]
        })

    return resultado


# ==================================================
# DASHBOARD PROFESIONAL
# ==================================================

def abrir_dashboard_profesional(
    ventana_padre
):
    v = tk.Toplevel(
        ventana_padre
    )

    v.title(
        "AI Business Assistant - Executive Dashboard"
    )

    v.geometry(
        "1280x840"
    )

    v.resizable(
        True,
        True
    )

    v.minsize(
        1050,
        650
    )

    v.configure(
        bg=FONDO
    )

    # ==================================================
    # ÁREA GENERAL CON SCROLL
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

    scrollbar_vertical = tk.Scrollbar(
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
        yscrollcommand=scrollbar_vertical.set
    )

    canvas_principal.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_vertical.pack(
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
        pady=(24, 10)
    )

    titulo_contenedor = tk.Frame(
        encabezado,
        bg=FONDO
    )

    titulo_contenedor.pack(
        side="left"
    )

    tk.Label(
        titulo_contenedor,
        text="AI BUSINESS ASSISTANT",
        font=(
            "Segoe UI",
            23,
            "bold"
        ),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        titulo_contenedor,
        text="Executive Financial Intelligence",
        font=(
            "Segoe UI",
            11
        ),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(2, 0)
    )

    estado_superior = tk.Frame(
        encabezado,
        bg=FONDO
    )

    estado_superior.pack(
        side="right"
    )

    tk.Label(
        estado_superior,
        text="● LIVE DATA",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=FONDO,
        fg=VERDE
    ).pack(
        side="left",
        padx=(0, 20)
    )

    boton_actualizar = tk.Button(
        estado_superior,
        text="Refresh",
        width=12,
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    boton_actualizar.pack(
        side="left"
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
        pady=(10, 16)
    )

    etiquetas_kpi = {}

    def crear_kpi(
        columna,
        titulo,
        clave,
        indicador,
        color
    ):
        tarjeta = tk.Frame(
            marco_kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            width=285,
            height=115
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=6,
            sticky="nsew"
        )

        tarjeta.grid_propagate(
            False
        )

        marco_kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        barra = tk.Frame(
            tarjeta,
            bg=color,
            width=5
        )

        barra.pack(
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
            padx=18,
            pady=15
        )

        tk.Label(
            contenido,
            text=titulo,
            font=(
                "Segoe UI",
                9,
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
                22,
                "bold"
            ),
            bg=PANEL,
            fg=TEXTO
        )

        valor.pack(
            anchor="w",
            pady=(7, 2)
        )

        tk.Label(
            contenido,
            text=indicador,
            font=(
                "Segoe UI",
                8
            ),
            bg=PANEL,
            fg=color
        ).pack(
            anchor="w"
        )

        etiquetas_kpi[
            clave
        ] = valor

    crear_kpi(
        0,
        "TOTAL SALES",
        "ventas_totales",
        "Revenue generated",
        AZUL
    )

    crear_kpi(
        1,
        "KNOWN PROFIT",
        "ganancia_conocida",
        "Confirmed margin",
        VERDE
    )

    crear_kpi(
        2,
        "RECEIVABLES",
        "total_por_cobrar",
        "Outstanding balance",
        AMARILLO
    )

    crear_kpi(
        3,
        "CASH FLOW",
        "flujo_caja",
        "Business liquidity",
        CYAN
    )

    # ==================================================
    # CUERPO
    # ==================================================

    cuerpo = tk.Frame(
        contenido_principal,
        bg=FONDO
    )

    cuerpo.pack(
        fill="both",
        expand=True,
        padx=30
    )

    columna_izquierda = tk.Frame(
        cuerpo,
        bg=FONDO
    )

    columna_izquierda.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 8)
    )

    columna_derecha = tk.Frame(
        cuerpo,
        bg=FONDO,
        width=300
    )

    columna_derecha.pack(
        side="right",
        fill="y",
        padx=(8, 0)
    )

    columna_derecha.pack_propagate(
        False
    )

    # ==================================================
    # GRÁFICO
    # ==================================================

    panel_grafico = tk.Frame(
        columna_izquierda,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_grafico.pack(
        fill="both",
        expand=True
    )

    titulo_grafico = tk.Frame(
        panel_grafico,
        bg=PANEL
    )

    titulo_grafico.pack(
        fill="x",
        padx=20,
        pady=(16, 5)
    )

    tk.Label(
        titulo_grafico,
        text="SALES PERFORMANCE",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        side="left"
    )

    tk.Label(
        titulo_grafico,
        text="Sales",
        font=(
            "Segoe UI",
            8
        ),
        bg=PANEL,
        fg=AZUL
    ).pack(
        side="right",
        padx=(10, 5)
    )

    tk.Label(
        titulo_grafico,
        text="●",
        font=(
            "Segoe UI",
            11
        ),
        bg=PANEL,
        fg=AZUL
    ).pack(
        side="right"
    )

    canvas = tk.Canvas(
        panel_grafico,
        bg=PANEL,
        highlightthickness=0,
        height=350
    )

    canvas.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(5, 15)
    )

    # ==================================================
    # PANEL INFERIOR
    # ==================================================

    panel_inferior = tk.Frame(
        columna_izquierda,
        bg=FONDO
    )

    panel_inferior.pack(
        fill="x",
        pady=(14, 0)
    )

    inventario_panel = tk.Frame(
        panel_inferior,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    inventario_panel.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 7)
    )

    cuentas_panel = tk.Frame(
        panel_inferior,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    cuentas_panel.pack(
        side="right",
        fill="both",
        expand=True,
        padx=(7, 0)
    )

    tk.Label(
        inventario_panel,
        text="INVENTORY POSITION",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=18,
        pady=(14, 10)
    )

    etiqueta_inventario = tk.Label(
        inventario_panel,
        text="",
        justify="left",
        font=(
            "Segoe UI",
            10
        ),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    )

    etiqueta_inventario.pack(
        anchor="w",
        padx=18,
        pady=(0, 15)
    )

    tk.Label(
        cuentas_panel,
        text="ACCOUNTS RECEIVABLE",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=18,
        pady=(14, 10)
    )

    etiqueta_cuentas = tk.Label(
        cuentas_panel,
        text="",
        justify="left",
        font=(
            "Segoe UI",
            10
        ),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    )

    etiqueta_cuentas.pack(
        anchor="w",
        padx=18,
        pady=(0, 15)
    )

    # ==================================================
    # ALERTAS
    # ==================================================

    panel_alertas = tk.Frame(
        columna_derecha,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_alertas.pack(
        fill="x"
    )

    tk.Label(
        panel_alertas,
        text="RISK & ALERT CENTER",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=18,
        pady=(16, 15)
    )

    alertas_contenedor = tk.Frame(
        panel_alertas,
        bg=PANEL
    )

    alertas_contenedor.pack(
        fill="x",
        padx=15,
        pady=(0, 15)
    )

    etiquetas_alertas = {}

    def crear_alerta(
        titulo,
        clave,
        color
    ):
        fila = tk.Frame(
            alertas_contenedor,
            bg=PANEL_SECUNDARIO
        )

        fila.pack(
            fill="x",
            pady=4
        )

        tk.Frame(
            fila,
            bg=color,
            width=4,
            height=48
        ).pack(
            side="left",
            fill="y"
        )

        tk.Label(
            fila,
            text=titulo,
            font=(
                "Segoe UI",
                9
            ),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            side="left",
            padx=12,
            pady=12
        )

        valor = tk.Label(
            fila,
            text="0",
            font=(
                "Segoe UI",
                13,
                "bold"
            ),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO
        )

        valor.pack(
            side="right",
            padx=15
        )

        etiquetas_alertas[
            clave
        ] = valor

    crear_alerta(
        "Pending accounts",
        "pendientes",
        AMARILLO
    )

    crear_alerta(
        "Overdue accounts",
        "vencidas",
        ROJO
    )

    crear_alerta(
        "Due within 7 days",
        "proximas",
        CYAN
    )

    crear_alerta(
        "Low stock items",
        "stock_bajo",
        AMARILLO
    )

    # ==================================================
    # FINANCIAL POSITION
    # ==================================================

    posicion_panel = tk.Frame(
        columna_derecha,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    posicion_panel.pack(
        fill="x",
        pady=(14, 0)
    )

    tk.Label(
        posicion_panel,
        text="FINANCIAL POSITION",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=18,
        pady=(16, 15)
    )

    etiqueta_posicion = tk.Label(
        posicion_panel,
        text="",
        justify="left",
        font=(
            "Segoe UI",
            10
        ),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    )

    etiqueta_posicion.pack(
        anchor="w",
        padx=18,
        pady=(0, 18)
    )

    # ==================================================
    # GRÁFICO DE LÍNEA
    # ==================================================

    def dibujar_grafico():
        canvas.delete(
            "all"
        )

        datos = obtener_ventas_por_fecha()

        canvas.update_idletasks()

        ancho = max(
            canvas.winfo_width(),
            700
        )

        alto = max(
            canvas.winfo_height(),
            300
        )

        izquierda = 65
        derecha = ancho - 30
        arriba = 30
        abajo = alto - 55

        if not datos:
            canvas.create_text(
                ancho / 2,
                alto / 2,
                text=(
                    "No dated sales available "
                    "for trend analysis"
                ),
                fill=TEXTO_SECUNDARIO,
                font=(
                    "Segoe UI",
                    12
                )
            )
            return

        maximo = max(
            item[
                "ventas"
            ]
            for item in datos
        )

        if maximo <= 0:
            maximo = 1

        divisiones = 4

        for i in range(
            divisiones + 1
        ):
            y = (
                arriba
                + (
                    abajo
                    - arriba
                )
                * i
                / divisiones
            )

            canvas.create_line(
                izquierda,
                y,
                derecha,
                y,
                fill=BORDE,
                width=1
            )

            valor = (
                maximo
                * (
                    divisiones - i
                )
                / divisiones
            )

            canvas.create_text(
                izquierda - 10,
                y,
                text=f"${valor:.0f}",
                anchor="e",
                fill=TEXTO_SECUNDARIO,
                font=(
                    "Segoe UI",
                    8
                )
            )

        puntos = []

        cantidad = len(
            datos
        )

        if cantidad == 1:
            posiciones_x = [
                (
                    izquierda
                    + derecha
                ) / 2
            ]

        else:
            posiciones_x = [
                izquierda
                + (
                    derecha
                    - izquierda
                )
                * indice
                / (
                    cantidad - 1
                )
                for indice in range(
                    cantidad
                )
            ]

        for indice, item in enumerate(
            datos
        ):
            valor = item[
                "ventas"
            ]

            x = posiciones_x[
                indice
            ]

            y = (
                abajo
                - (
                    valor
                    / maximo
                )
                * (
                    abajo
                    - arriba
                )
            )

            puntos.extend(
                [
                    x,
                    y
                ]
            )

            fecha = datetime.strptime(
                item["fecha"],
                "%Y-%m-%d"
            ).strftime(
                "%b %d"
            )

            canvas.create_text(
                x,
                abajo + 22,
                text=fecha,
                fill=TEXTO_SECUNDARIO,
                font=(
                    "Segoe UI",
                    8
                )
            )

        if len(
            puntos
        ) >= 4:
            canvas.create_line(
                *puntos,
                fill=AZUL,
                width=3,
                smooth=True
            )

        for indice, item in enumerate(
            datos
        ):
            valor = item[
                "ventas"
            ]

            x = posiciones_x[
                indice
            ]

            y = (
                abajo
                - (
                    valor
                    / maximo
                )
                * (
                    abajo
                    - arriba
                )
            )

            canvas.create_oval(
                x - 5,
                y - 5,
                x + 5,
                y + 5,
                fill=AZUL,
                outline=PANEL,
                width=2
            )

            canvas.create_text(
                x,
                y - 18,
                text=f"${valor:.0f}",
                fill=TEXTO,
                font=(
                    "Segoe UI",
                    8,
                    "bold"
                )
            )

    # ==================================================
    # ACTUALIZACIÓN
    # ==================================================

    def actualizar():
        datos = calcular_dashboard()

        for clave, etiqueta in (
            etiquetas_kpi.items()
        ):
            valor = convertir_numero(
                datos.get(
                    clave,
                    0
                )
            )

            etiqueta.config(
                text=f"${valor:,.2f}"
            )

        alertas = calcular_alertas()

        for clave, etiqueta in (
            etiquetas_alertas.items()
        ):
            etiqueta.config(
                text=str(
                    alertas.get(
                        clave,
                        0
                    )
                )
            )

        capital = convertir_numero(
            datos.get(
                "capital_inventario",
                0
            )
        )

        valor_inv = convertir_numero(
            datos.get(
                "valor_inventario",
                0
            )
        )

        potencial = (
            valor_inv - capital
        )

        etiqueta_inventario.config(
            text=(
                f"Capital invested        ${capital:,.2f}\n"
                f"Potential sales value   ${valor_inv:,.2f}\n"
                f"Potential gross profit  ${potencial:,.2f}"
            )
        )

        etiqueta_cuentas.config(
            text=(
                f"Outstanding balance     "
                f"${datos['total_por_cobrar']:,.2f}\n"
                f"Pending accounts        "
                f"{alertas['pendientes']}\n"
                f"Overdue accounts        "
                f"{alertas['vencidas']}"
            )
        )

        etiqueta_posicion.config(
            text=(
                f"Operating expenses\n"
                f"${datos['gastos_totales']:,.2f}\n\n"
                f"Inventory capital\n"
                f"${capital:,.2f}\n\n"
                f"Cash flow\n"
                f"${datos['flujo_caja']:,.2f}"
            )
        )

        dibujar_grafico()

    boton_actualizar.config(
        command=actualizar
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
        pady=(14, 25)
    )

    tk.Label(
        pie,
        text=(
            "AI Business Assistant  •  "
            "Executive Management System"
        ),
        font=(
            "Segoe UI",
            8
        ),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        side="left"
    )

    def cerrar_dashboard():
        canvas_principal.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text="Close dashboard",
        width=16,
        command=cerrar_dashboard,
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
        cerrar_dashboard
    )

    actualizar()
