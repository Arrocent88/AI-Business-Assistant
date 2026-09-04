import tkinter as tk
from tkinter import ttk

from clientes import clientes
from cliente_resumen import calcular_resumen_cliente


def abrir_resumen_cliente(ventana_padre):
    v = tk.Toplevel(ventana_padre)

    v.title("Resumen por cliente")
    v.geometry("650x520")
    v.resizable(False, False)

    tk.Label(
        v,
        text="RESUMEN POR CLIENTE",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(25, 20)
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
        pady=(5, 20)
    )

    marco_resumen = tk.LabelFrame(
        v,
        text="Información del cliente",
        font=("Arial", 11, "bold"),
        padx=25,
        pady=20
    )

    marco_resumen.pack(
        fill="x",
        padx=45,
        pady=10
    )

    etiqueta_cliente = tk.Label(
        marco_resumen,
        text="Cliente: -"
    )

    etiqueta_cliente.pack(
        anchor="w",
        pady=4
    )

    etiqueta_ventas = tk.Label(
        marco_resumen,
        text="Número de ventas: 0"
    )

    etiqueta_ventas.pack(
        anchor="w",
        pady=4
    )

    etiqueta_comprado = tk.Label(
        marco_resumen,
        text="Total comprado: $0.00"
    )

    etiqueta_comprado.pack(
        anchor="w",
        pady=4
    )

    etiqueta_ganancia = tk.Label(
        marco_resumen,
        text="Ganancia conocida: $0.00"
    )

    etiqueta_ganancia.pack(
        anchor="w",
        pady=4
    )

    etiqueta_credito = tk.Label(
        marco_resumen,
        text="Total vendido a crédito: $0.00"
    )

    etiqueta_credito.pack(
        anchor="w",
        pady=4
    )

    etiqueta_pagado = tk.Label(
        marco_resumen,
        text="Total pagado: $0.00"
    )

    etiqueta_pagado.pack(
        anchor="w",
        pady=4
    )

    etiqueta_pendiente = tk.Label(
        marco_resumen,
        text="Saldo pendiente: $0.00",
        font=("Arial", 11, "bold")
    )

    etiqueta_pendiente.pack(
        anchor="w",
        pady=4
    )

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
        pady=20
    )