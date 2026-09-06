import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

from cuentas import (
    cuentas_por_cobrar,
    guardar_cuentas
)

from idiomas import (
    t,
    obtener_idioma
)


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


def calcular_alerta_vencimiento(cuenta):
    saldo = convertir_numero(
        cuenta.get(
            "saldo_pendiente",
            0
        )
    )

    if saldo <= 0:
        return (
            "Paid"
            if obtener_idioma() == "en"
            else "Pagada"
        )

    fecha_texto = str(
        cuenta.get(
            "fecha_vencimiento",
            ""
        )
    ).strip()

    if not fecha_texto:
        return (
            "No due date"
            if obtener_idioma() == "en"
            else "Sin fecha de vencimiento"
        )

    try:
        fecha_vencimiento = datetime.strptime(
            fecha_texto,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return (
            "Invalid due date"
            if obtener_idioma() == "en"
            else "Fecha de vencimiento inválida"
        )

    hoy = datetime.now().date()
    dias = (
        fecha_vencimiento - hoy
    ).days

    if dias < 0:
        return (
            f"OVERDUE by {abs(dias)} day(s)"
            if obtener_idioma() == "en"
            else f"VENCIDA hace {abs(dias)} día(s)"
        )

    if dias == 0:
        return (
            "DUE TODAY"
            if obtener_idioma() == "en"
            else "VENCE HOY"
        )

    if dias <= 7:
        return (
            f"DUE SOON - {dias} day(s)"
            if obtener_idioma() == "en"
            else f"VENCE PRONTO - faltan {dias} día(s)"
        )

    return (
        f"CURRENT - {dias} day(s)"
        if obtener_idioma() == "en"
        else f"AL DÍA - faltan {dias} día(s)"
    )


def abrir_cuentas_por_cobrar(ventana_padre):
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

    v = tk.Toplevel(
        ventana_padre
    )

    v.title(
        "AI Business Assistant - Accounts Receivable"
    )

    v.geometry(
        "1100x800"
    )

    v.minsize(
        880,
        650
    )

    v.resizable(
        True,
        True
    )

    v.configure(bg=FONDO)

    modo_actual = tk.StringVar(
        value="Pendientes"
    )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 14)
    )

    tk.Label(
        encabezado,
        text=t("receivables_management"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    tk.Label(
        encabezado,
        text=t("receivables_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    filtros = tk.Frame(
        v,
        bg=FONDO
    )

    filtros.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    panel_kpis = tk.Frame(
        v,
        bg=FONDO
    )

    panel_kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    etiquetas_kpi = {}

    def crear_kpi(
        columna,
        titulo,
        clave,
        color
    ):
        tarjeta = tk.Frame(
            panel_kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=95
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(False)
        panel_kpis.grid_columnconfigure(
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

        cuerpo = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(anchor="w")

        valor = tk.Label(
            cuerpo,
            text="$0.00",
            font=("Segoe UI", 16, "bold"),
            bg=PANEL,
            fg=TEXTO
        )

        valor.pack(
            anchor="w",
            pady=(6, 0)
        )

        etiquetas_kpi[
            clave
        ] = valor

    crear_kpi(
        0,
        t("total_pending"),
        "pendiente",
        AMARILLO
    )

    crear_kpi(
        1,
        t("total_overdue"),
        "vencido",
        ROJO
    )

    crear_kpi(
        2,
        t("due_soon"),
        "pronto",
        CYAN
    )

    crear_kpi(
        3,
        t("clients_with_debt"),
        "clientes",
        AZUL
    )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 14)
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
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
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

    def registrar_pago(cuenta):
        saldo_actual = convertir_numero(
            cuenta.get(
                "saldo_pendiente",
                0
            )
        )

        if saldo_actual <= 0:
            messagebox.showinfo(
                "Paid"
                if obtener_idioma() == "en"
                else "Cuenta pagada",
                "This account is already fully paid."
                if obtener_idioma() == "en"
                else "Esta cuenta ya está completamente pagada."
            )
            return

        monto = simpledialog.askfloat(
            t("register_payment"),
            (
                f"{t('clientes')}: "
                f"{cuenta.get('cliente', '')}\n"
                f"{t('balance_due')}: "
                f"${saldo_actual:.2f}\n\n"
                +
                (
                    "Enter payment amount:"
                    if obtener_idioma() == "en"
                    else "Escribe el monto recibido:"
                )
            ),
            parent=v,
            minvalue=0.01
        )

        if monto is None:
            return

        if monto > saldo_actual:
            messagebox.showwarning(
                "Invalid amount"
                if obtener_idioma() == "en"
                else "Monto incorrecto",
                "Payment cannot exceed the outstanding balance."
                if obtener_idioma() == "en"
                else "El pago no puede ser mayor que el saldo pendiente."
            )
            return

        pagado_anterior = convertir_numero(
            cuenta.get(
                "monto_pagado",
                0
            )
        )

        nuevo_pagado = (
            pagado_anterior + monto
        )

        nuevo_saldo = (
            saldo_actual - monto
        )

        if nuevo_saldo < 0.01:
            nuevo_saldo = 0

        cuenta[
            "monto_pagado"
        ] = round(
            nuevo_pagado,
            2
        )

        cuenta[
            "saldo_pendiente"
        ] = round(
            nuevo_saldo,
            2
        )

        cuenta[
            "estado"
        ] = (
            "Pagada"
            if nuevo_saldo == 0
            else "Pendiente"
        )

        if "pagos" not in cuenta:
            cuenta[
                "pagos"
            ] = []

        cuenta[
            "pagos"
        ].append({
            "fecha": datetime.now().strftime(
                "%Y-%m-%d"
            ),
            "monto": round(
                monto,
                2
            )
        })

        guardar_cuentas(
            cuentas_por_cobrar
        )

        messagebox.showinfo(
            "Payment registered"
            if obtener_idioma() == "en"
            else "Pago registrado",
            (
                "Payment registered successfully."
                if obtener_idioma() == "en"
                else "Pago registrado correctamente."
            )
        )

        actualizar_lista()

    def actualizar_resumen():
        total_pendiente = 0
        total_vencido = 0
        total_pronto = 0
        clientes = set()

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

            total_pendiente += saldo

            cliente = str(
                cuenta.get(
                    "cliente",
                    ""
                )
            ).strip()

            if cliente:
                clientes.add(
                    cliente.lower()
                )

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
                        total_vencido += saldo
                    elif dias <= 7:
                        total_pronto += saldo
                except ValueError:
                    pass

        etiquetas_kpi[
            "pendiente"
        ].config(
            text=f"${total_pendiente:,.2f}"
        )

        etiquetas_kpi[
            "vencido"
        ].config(
            text=f"${total_vencido:,.2f}"
        )

        etiquetas_kpi[
            "pronto"
        ].config(
            text=f"${total_pronto:,.2f}"
        )

        etiquetas_kpi[
            "clientes"
        ].config(
            text=str(len(clientes))
        )

    def mostrar_pendientes():
        modo_actual.set(
            "Pendientes"
        )
        actualizar_lista()

    def mostrar_pagadas():
        modo_actual.set(
            "Pagadas"
        )
        actualizar_lista()

    tk.Button(
        filtros,
        text=t("pending"),
        command=mostrar_pendientes,
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=8
    ).pack(
        side="left"
    )

    tk.Button(
        filtros,
        text=t("paid"),
        command=mostrar_pagadas,
        font=("Segoe UI", 10, "bold"),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=8
    ).pack(
        side="left",
        padx=(10, 0)
    )

    def actualizar_lista():
        actualizar_resumen()

        for widget in contenido.winfo_children():
            widget.destroy()

        modo = modo_actual.get()

        if modo == "Pendientes":
            cuentas_mostrar = [
                cuenta
                for cuenta in cuentas_por_cobrar
                if convertir_numero(
                    cuenta.get(
                        "saldo_pendiente",
                        0
                    )
                ) > 0
            ]
        else:
            cuentas_mostrar = [
                cuenta
                for cuenta in cuentas_por_cobrar
                if convertir_numero(
                    cuenta.get(
                        "saldo_pendiente",
                        0
                    )
                ) <= 0
            ]

        for numero, cuenta in enumerate(
            cuentas_mostrar,
            start=1
        ):
            saldo = convertir_numero(
                cuenta.get(
                    "saldo_pendiente",
                    0
                )
            )

            total = convertir_numero(
                cuenta.get(
                    "total",
                    0
                )
            )

            pagado = convertir_numero(
                cuenta.get(
                    "monto_pagado",
                    0
                )
            )

            tarjeta = tk.Frame(
                contenido,
                bg=PANEL_SECUNDARIO,
                highlightbackground=BORDE,
                highlightthickness=1
            )

            tarjeta.pack(
                fill="x",
                pady=6
            )

            cabecera = tk.Frame(
                tarjeta,
                bg=PANEL_SECUNDARIO
            )

            cabecera.pack(
                fill="x",
                padx=16,
                pady=(12, 6)
            )

            tk.Label(
                cabecera,
                text=(
                    f"ACCOUNT #{numero:02d}"
                    if obtener_idioma() == "en"
                    else f"CUENTA #{numero:02d}"
                ),
                font=("Segoe UI", 10, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO
            ).pack(side="left")

            tk.Label(
                cabecera,
                text=f"${saldo:,.2f}",
                font=("Segoe UI", 11, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=(
                    VERDE
                    if saldo <= 0
                    else AMARILLO
                )
            ).pack(side="right")

            alerta = calcular_alerta_vencimiento(
                cuenta
            )

            detalle = (
                f"{t('clientes')}: "
                f"{cuenta.get('cliente', '')}\n"
                f"{t('product')}: "
                f"{cuenta.get('codigo_producto', '')} - "
                f"{cuenta.get('producto', '')}\n"
                f"{t('sale_date')}: "
                f"{cuenta.get('fecha_venta', '')}\n"
                f"{t('due_date')}: "
                f"{cuenta.get('fecha_vencimiento', '')}\n"
                f"Total: ${total:,.2f}\n"
                f"{t('paid_amount')}: ${pagado:,.2f}\n"
                f"{t('balance_due')}: ${saldo:,.2f}\n"
                f"{t('alert')}: {alerta}"
            )

            tk.Label(
                tarjeta,
                text=detalle,
                justify="left",
                font=("Segoe UI", 9),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO_SECUNDARIO
            ).pack(
                anchor="w",
                padx=16,
                pady=(0, 8)
            )

            pagos = cuenta.get(
                "pagos",
                []
            )

            tk.Label(
                tarjeta,
                text=t("payment_history"),
                font=("Segoe UI", 9, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO
            ).pack(
                anchor="w",
                padx=16,
                pady=(4, 4)
            )

            if pagos:
                for numero_pago, pago in enumerate(
                    pagos,
                    start=1
                ):
                    tk.Label(
                        tarjeta,
                        text=(
                            f"{numero_pago}. "
                            f"{pago.get('fecha', '')} - "
                            f"${convertir_numero(pago.get('monto', 0)):,.2f}"
                        ),
                        font=("Segoe UI", 9),
                        bg=PANEL_SECUNDARIO,
                        fg=TEXTO_SECUNDARIO
                    ).pack(
                        anchor="w",
                        padx=16
                    )
            else:
                tk.Label(
                    tarjeta,
                    text=t("no_payments"),
                    font=("Segoe UI", 9),
                    bg=PANEL_SECUNDARIO,
                    fg=TEXTO_SECUNDARIO
                ).pack(
                    anchor="w",
                    padx=16
                )

            if modo == "Pendientes":
                tk.Button(
                    tarjeta,
                    text=t("register_payment"),
                    command=lambda c=cuenta:
                    registrar_pago(c),
                    font=("Segoe UI", 9, "bold"),
                    bg=AZUL,
                    fg="white",
                    activebackground="#2563EB",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    padx=16,
                    pady=7
                ).pack(
                    anchor="w",
                    padx=16,
                    pady=(10, 12)
                )
            else:
                tk.Frame(
                    tarjeta,
                    bg=PANEL_SECUNDARIO,
                    height=10
                ).pack()

        canvas.yview_moveto(0)

    actualizar_lista()

    pie = tk.Frame(
        v,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )
        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(side="right")

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )
