import tkinter as tk
from tkinter import messagebox, simpledialog

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

    def actualizar_lista():
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