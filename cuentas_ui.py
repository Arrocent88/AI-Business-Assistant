import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

from cuentas import (
    cuentas_por_cobrar,
    guardar_cuentas
)


def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def calcular_alerta_vencimiento(cuenta):
    saldo = convertir_numero(
        cuenta.get(
            "saldo_pendiente",
            0
        )
    )

    if saldo <= 0:
        return "Pagada"

    fecha_texto = str(
        cuenta.get(
            "fecha_vencimiento",
            ""
        )
    ).strip()

    if not fecha_texto:
        return "Sin fecha de vencimiento"

    try:
        fecha_vencimiento = datetime.strptime(
            fecha_texto,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return "Fecha de vencimiento inválida"

    hoy = datetime.now().date()

    dias = (
        fecha_vencimiento - hoy
    ).days

    if dias < 0:
        return f"VENCIDA hace {abs(dias)} día(s)"

    if dias == 0:
        return "VENCE HOY"

    if dias <= 7:
        return f"VENCE PRONTO - faltan {dias} día(s)"

    return f"AL DÍA - faltan {dias} día(s)"


def abrir_cuentas_por_cobrar(ventana_padre):
    v = tk.Toplevel(ventana_padre)

    v.title("Cuentas por cobrar")
    v.geometry("900x720")
    v.resizable(False, False)

    tk.Label(
        v,
        text="CUENTAS POR COBRAR",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(20, 10)
    )

    modo_actual = tk.StringVar(
        value="Pendientes"
    )

    marco_botones = tk.Frame(v)

    marco_botones.pack(
        pady=(0, 10)
    )

    marco = tk.Frame(v)

    marco.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
    )

    canvas = tk.Canvas(marco)

    scrollbar = tk.Scrollbar(
        marco,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(canvas)

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
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

    etiqueta_total = tk.Label(
        v,
        text="",
        font=("Arial", 12, "bold")
    )

    etiqueta_total.pack(
        pady=10
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
                "Cuenta pagada",
                "Esta cuenta ya está completamente pagada."
            )
            return

        monto = simpledialog.askfloat(
            "Registrar pago",
            (
                f"Cliente: {cuenta.get('cliente', '')}\n"
                f"Saldo pendiente: ${saldo_actual:.2f}\n\n"
                "Escribe el monto recibido:"
            ),
            parent=v,
            minvalue=0.01
        )

        if monto is None:
            return

        if monto > saldo_actual:
            messagebox.showwarning(
                "Monto incorrecto",
                (
                    "El pago no puede ser mayor "
                    "que el saldo pendiente."
                )
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

        cuenta["monto_pagado"] = round(
            nuevo_pagado,
            2
        )

        cuenta["saldo_pendiente"] = round(
            nuevo_saldo,
            2
        )

        if nuevo_saldo == 0:
            cuenta["estado"] = "Pagada"
        else:
            cuenta["estado"] = "Pendiente"

        if "pagos" not in cuenta:
            cuenta["pagos"] = []

        cuenta["pagos"].append({
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
            "Pago registrado",
            (
                "Pago registrado correctamente.\n\n"
                f"Monto recibido: ${monto:.2f}\n"
                f"Total pagado: ${nuevo_pagado:.2f}\n"
                f"Saldo pendiente: ${nuevo_saldo:.2f}"
            )
        )

        actualizar_lista()

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
        marco_botones,
        text="Pendientes",
        width=18,
        command=mostrar_pendientes
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        marco_botones,
        text="Pagadas",
        width=18,
        command=mostrar_pagadas
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    marco_resumen = tk.LabelFrame(
        v,
        text="Resumen de cuentas por cobrar",
        font=("Arial", 11, "bold"),
        padx=12,
        pady=8
    )

    marco_resumen.pack(
        fill="x",
        padx=30,
        pady=(0, 8)
    )

    etiqueta_pendiente = tk.Label(
        marco_resumen,
        font=("Arial", 10, "bold")
    )
    etiqueta_pendiente.grid(
        row=0,
        column=0,
        padx=18,
        pady=4
    )

    etiqueta_vencido = tk.Label(
        marco_resumen,
        font=("Arial", 10, "bold")
    )
    etiqueta_vencido.grid(
        row=0,
        column=1,
        padx=18,
        pady=4
    )

    etiqueta_pronto = tk.Label(
        marco_resumen,
        font=("Arial", 10, "bold")
    )
    etiqueta_pronto.grid(
        row=0,
        column=2,
        padx=18,
        pady=4
    )

    etiqueta_clientes = tk.Label(
        marco_resumen,
        font=("Arial", 10, "bold")
    )
    etiqueta_clientes.grid(
        row=0,
        column=3,
        padx=18,
        pady=4
    )

    def actualizar_resumen():
        total_pendiente_resumen = 0
        total_vencido = 0
        total_pronto = 0
        clientes_deudores = set()

        for cuenta in cuentas_por_cobrar:
            saldo = convertir_numero(
                cuenta.get(
                    "saldo_pendiente",
                    0
                )
            )

            if saldo <= 0:
                continue

            total_pendiente_resumen += saldo

            cliente = str(
                cuenta.get(
                    "cliente",
                    ""
                )
            ).strip()

            if cliente:
                clientes_deudores.add(
                    cliente.lower()
                )

            alerta = calcular_alerta_vencimiento(
                cuenta
            )

            if alerta.startswith("VENCIDA"):
                total_vencido += saldo
            elif (
                alerta == "VENCE HOY"
                or alerta.startswith("VENCE PRONTO")
            ):
                total_pronto += saldo

        etiqueta_pendiente.config(
            text=(
                "Total pendiente\n"
                f"${total_pendiente_resumen:.2f}"
            )
        )

        etiqueta_vencido.config(
            text=(
                "Total vencido\n"
                f"${total_vencido:.2f}"
            )
        )

        etiqueta_pronto.config(
            text=(
                "Vence pronto\n"
                f"${total_pronto:.2f}"
            )
        )

        etiqueta_clientes.config(
            text=(
                "Clientes con deuda\n"
                f"{len(clientes_deudores)}"
            )
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

        total_pendiente = 0
        total_pagado = 0

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

            total_pendiente += saldo
            total_pagado += pagado

            caja = tk.LabelFrame(
                contenido,
                text=f"Cuenta {numero}",
                font=("Arial", 11, "bold"),
                padx=20,
                pady=10
            )

            caja.pack(
                fill="x",
                padx=5,
                pady=8
            )

            tk.Label(
                caja,
                text=(
                    f"Cliente: "
                    f"{cuenta.get('cliente', '')}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Producto: "
                    f"{cuenta.get('codigo_producto', '')} - "
                    f"{cuenta.get('producto', '')}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Fecha de venta: "
                    f"{cuenta.get('fecha_venta', '')}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Vencimiento: "
                    f"{cuenta.get('fecha_vencimiento', '')}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=f"Total: ${total:.2f}"
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=f"Pagado: ${pagado:.2f}"
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"SALDO PENDIENTE: "
                    f"${saldo:.2f}"
                ),
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Estado: "
                    f"{cuenta.get('estado', 'Pendiente')}"
                )
            ).pack(anchor="w")

            alerta = calcular_alerta_vencimiento(
                cuenta
            )

            tk.Label(
                caja,
                text=f"Alerta: {alerta}",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

            pagos = cuenta.get(
                "pagos",
                []
            )

            tk.Label(
                caja,
                text="Historial de pagos:",
                font=("Arial", 10, "bold")
            ).pack(
                anchor="w",
                pady=(10, 3)
            )

            if pagos:
                for numero_pago, pago in enumerate(
                    pagos,
                    start=1
                ):
                    monto_pago = convertir_numero(
                        pago.get(
                            "monto",
                            0
                        )
                    )

                    fecha_pago = pago.get(
                        "fecha",
                        "Sin fecha"
                    )

                    tk.Label(
                        caja,
                        text=(
                            f"{numero_pago}. "
                            f"{fecha_pago} - "
                            f"${monto_pago:.2f}"
                        )
                    ).pack(anchor="w")
            else:
                tk.Label(
                    caja,
                    text="Sin pagos registrados."
                ).pack(anchor="w")

            if modo == "Pendientes":
                tk.Button(
                    caja,
                    text="Registrar pago",
                    width=18,
                    command=lambda c=cuenta:
                    registrar_pago(c)
                ).pack(
                    anchor="w",
                    pady=(10, 0)
                )

        if modo == "Pendientes":
            etiqueta_total.config(
                text=(
                    f"Total pendiente por cobrar: "
                    f"${total_pendiente:.2f}"
                )
            )
        else:
            etiqueta_total.config(
                text=(
                    f"Total cobrado en cuentas pagadas: "
                    f"${total_pagado:.2f}"
                )
            )

    actualizar_lista()

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(
        pady=15
    )