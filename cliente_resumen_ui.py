import tkinter as tk
from tkinter import ttk

from clientes import clientes
from ventas import ventas
from cliente_resumen import calcular_resumen_cliente


def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def abrir_resumen_cliente(ventana_padre):
    v = tk.Toplevel(ventana_padre)

    v.title("Resumen por cliente")
    v.geometry("760x720")
    v.resizable(False, False)

    tk.Label(
        v,
        text="RESUMEN POR CLIENTE",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(20, 15)
    )

    tk.Label(
        v,
        text="Selecciona un cliente:"
    ).pack()

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
        v,
        values=opciones_clientes,
        state="readonly",
        width=40
    )

    combo_cliente.pack(
        pady=(5, 15)
    )

    marco_resumen = tk.LabelFrame(
        v,
        text="Información del cliente",
        font=("Arial", 11, "bold"),
        padx=25,
        pady=15
    )

    marco_resumen.pack(
        fill="x",
        padx=40,
        pady=(0, 10)
    )

    etiqueta_cliente = tk.Label(
        marco_resumen,
        text="Cliente: -"
    )

    etiqueta_cliente.pack(
        anchor="w",
        pady=3
    )

    etiqueta_ventas = tk.Label(
        marco_resumen,
        text="Número de ventas: 0"
    )

    etiqueta_ventas.pack(
        anchor="w",
        pady=3
    )

    etiqueta_comprado = tk.Label(
        marco_resumen,
        text="Total comprado: $0.00"
    )

    etiqueta_comprado.pack(
        anchor="w",
        pady=3
    )

    etiqueta_ganancia = tk.Label(
        marco_resumen,
        text="Ganancia conocida: $0.00"
    )

    etiqueta_ganancia.pack(
        anchor="w",
        pady=3
    )

    etiqueta_credito = tk.Label(
        marco_resumen,
        text="Total vendido a crédito: $0.00"
    )

    etiqueta_credito.pack(
        anchor="w",
        pady=3
    )

    etiqueta_pagado = tk.Label(
        marco_resumen,
        text="Total pagado: $0.00"
    )

    etiqueta_pagado.pack(
        anchor="w",
        pady=3
    )

    etiqueta_pendiente = tk.Label(
        marco_resumen,
        text="Saldo pendiente: $0.00",
        font=("Arial", 11, "bold")
    )

    etiqueta_pendiente.pack(
        anchor="w",
        pady=3
    )

    marco_historial = tk.LabelFrame(
        v,
        text="Historial detallado de ventas",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )

    marco_historial.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(0, 10)
    )

    canvas = tk.Canvas(
        marco_historial,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_historial,
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

    def mostrar_historial(nombre):
        for widget in contenido.winfo_children():
            widget.destroy()

        ventas_cliente = []

        for venta in ventas:
            cliente_venta = str(
                venta.get(
                    "cliente",
                    ""
                )
            ).strip()

            if cliente_venta.lower() == nombre.lower():
                ventas_cliente.append(
                    venta
                )

        if not ventas_cliente:
            tk.Label(
                contenido,
                text="No hay ventas registradas para este cliente."
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

            caja = tk.LabelFrame(
                contenido,
                text=f"Venta {numero}",
                padx=15,
                pady=8
            )

            caja.pack(
                fill="x",
                padx=5,
                pady=6
            )

            tk.Label(
                caja,
                text=f"Fecha: {fecha}"
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=f"Código: {codigo}"
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=f"Producto: {producto}"
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=f"Cantidad: {cantidad}"
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=f"Total: ${monto:.2f}",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=f"Tipo de pago: {tipo_pago}"
            ).pack(anchor="w")

    def mostrar_resumen(event=None):
        nombre = combo_cliente.get().strip()

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

        etiqueta_comprado.config(
            text=(
                f"Total comprado: "
                f"${resumen['total_comprado']:.2f}"
            )
        )

        etiqueta_ganancia.config(
            text=(
                f"Ganancia conocida: "
                f"${resumen['ganancia_conocida']:.2f}"
            )
        )

        etiqueta_credito.config(
            text=(
                f"Total vendido a crédito: "
                f"${resumen['total_credito']:.2f}"
            )
        )

        etiqueta_pagado.config(
            text=(
                f"Total pagado: "
                f"${resumen['total_pagado']:.2f}"
            )
        )

        etiqueta_pendiente.config(
            text=(
                f"Saldo pendiente: "
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

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(
        pady=10
    )