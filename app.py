import tkinter as tk

from clientes import clientes
from inventario import inventario, reposiciones
from ventas import ventas
from gastos import gastos
from diagnostico import calcular_diagnostico


def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


# ==================================================
# CLIENTES
# ==================================================

def abrir_clientes():
    ventana_clientes = tk.Toplevel(ventana)
    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("600x450")
    ventana_clientes.resizable(False, False)

    tk.Label(
        ventana_clientes,
        text="CLIENTES REGISTRADOS",
        font=("Arial", 18, "bold")
    ).pack(pady=25)

    if not clientes:
        tk.Label(
            ventana_clientes,
            text="No hay clientes registrados.",
            font=("Arial", 12)
        ).pack(pady=30)

    else:
        for numero, cliente in enumerate(
            clientes,
            start=1
        ):
            nombre = cliente.get(
                "nombre",
                "Sin nombre"
            )

            tk.Label(
                ventana_clientes,
                text=f"{numero}. {nombre}",
                font=("Arial", 12),
                width=40,
                anchor="w"
            ).pack(pady=5)

    tk.Button(
        ventana_clientes,
        text="Cerrar",
        width=15,
        command=ventana_clientes.destroy
    ).pack(
        side="bottom",
        pady=25
    )


# ==================================================
# VENTAS
# ==================================================

def abrir_ventas():
    ventana_ventas = tk.Toplevel(ventana)
    ventana_ventas.title("Ventas")
    ventana_ventas.geometry("750x550")
    ventana_ventas.resizable(False, False)

    tk.Label(
        ventana_ventas,
        text="VENTAS REGISTRADAS",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    if not ventas:
        tk.Label(
            ventana_ventas,
            text="No hay ventas registradas.",
            font=("Arial", 12)
        ).pack(pady=30)

    else:
        contenedor = tk.Frame(
            ventana_ventas
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )

        total_ventas = 0

        for numero, venta in enumerate(
            ventas,
            start=1
        ):
            cliente = venta.get(
                "cliente",
                "Sin cliente"
            )

            producto = venta.get(
                "producto",
                "Sin producto"
            )

            cantidad = int(
                venta.get("cantidad", 1)
            )

            monto = convertir_numero(
                venta.get("monto", 0)
            )

            total_ventas += monto

            marco = tk.LabelFrame(
                contenedor,
                text=f"Venta {numero}",
                font=("Arial", 11, "bold"),
                padx=15,
                pady=8
            )

            marco.pack(
                fill="x",
                pady=5
            )

            tk.Label(
                marco,
                text=f"Cliente: {cliente}",
                font=("Arial", 10)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=f"Producto: {producto}",
                font=("Arial", 10)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=f"Cantidad: {cantidad}",
                font=("Arial", 10)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=f"Total: ${monto:.2f}",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

        tk.Label(
            ventana_ventas,
            text=(
                f"TOTAL DE VENTAS: "
                f"${total_ventas:.2f}"
            ),
            font=("Arial", 13, "bold")
        ).pack(pady=10)

    tk.Button(
        ventana_ventas,
        text="Cerrar",
        width=15,
        command=ventana_ventas.destroy
    ).pack(
        side="bottom",
        pady=20
    )


# ==================================================
# INVENTARIO
# ==================================================

def abrir_inventario():
    ventana_inventario = tk.Toplevel(
        ventana
    )

    ventana_inventario.title(
        "Inventario"
    )

    ventana_inventario.geometry(
        "700x500"
    )

    ventana_inventario.resizable(
        False,
        False
    )

    tk.Label(
        ventana_inventario,
        text="INVENTARIO",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    if not inventario:
        tk.Label(
            ventana_inventario,
            text="No hay productos registrados.",
            font=("Arial", 12)
        ).pack(pady=30)

    else:
        for item in inventario:
            producto = item.get(
                "producto",
                "Sin nombre"
            )

            cantidad = int(
                item.get("cantidad", 0)
            )

            precio = convertir_numero(
                item.get("precio", 0)
            )

            costo = convertir_numero(
                item.get("costo", 0)
            )

            valor_potencial = (
                cantidad * precio
            )

            marco = tk.LabelFrame(
                ventana_inventario,
                text=producto,
                font=("Arial", 12, "bold"),
                padx=20,
                pady=10
            )

            marco.pack(
                fill="x",
                padx=50,
                pady=10
            )

            tk.Label(
                marco,
                text=(
                    f"Stock disponible: "
                    f"{cantidad}"
                ),
                font=("Arial", 11)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=(
                    f"Costo unitario: "
                    f"${costo:.2f}"
                ),
                font=("Arial", 11)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=(
                    f"Precio de venta: "
                    f"${precio:.2f}"
                ),
                font=("Arial", 11)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=(
                    f"Valor potencial: "
                    f"${valor_potencial:.2f}"
                ),
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

    tk.Button(
        ventana_inventario,
        text="Cerrar",
        width=15,
        command=ventana_inventario.destroy
    ).pack(
        side="bottom",
        pady=25
    )


# ==================================================
# GASTOS
# ==================================================

def abrir_gastos():
    ventana_gastos = tk.Toplevel(
        ventana
    )

    ventana_gastos.title("Gastos")
    ventana_gastos.geometry("700x500")

    ventana_gastos.resizable(
        False,
        False
    )

    tk.Label(
        ventana_gastos,
        text="GASTOS OPERATIVOS",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    if not gastos:
        tk.Label(
            ventana_gastos,
            text="No hay gastos registrados.",
            font=("Arial", 12)
        ).pack(pady=30)

    else:
        total_gastos = 0

        for numero, gasto in enumerate(
            gastos,
            start=1
        ):
            descripcion = gasto.get(
                "descripcion",
                gasto.get(
                    "concepto",
                    "Sin descripción"
                )
            )

            categoria = gasto.get(
                "categoria",
                "Sin categoría"
            )

            fecha = gasto.get(
                "fecha",
                "Sin fecha"
            )

            monto = convertir_numero(
                gasto.get("monto", 0)
            )

            total_gastos += monto

            marco = tk.LabelFrame(
                ventana_gastos,
                text=f"Gasto {numero}",
                font=("Arial", 11, "bold"),
                padx=20,
                pady=10
            )

            marco.pack(
                fill="x",
                padx=50,
                pady=8
            )

            tk.Label(
                marco,
                text=(
                    f"Descripción: "
                    f"{descripcion}"
                ),
                font=("Arial", 11)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=(
                    f"Categoría: "
                    f"{categoria}"
                ),
                font=("Arial", 11)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=f"Fecha: {fecha}",
                font=("Arial", 11)
            ).pack(anchor="w")

            tk.Label(
                marco,
                text=f"Monto: ${monto:.2f}",
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

        tk.Label(
            ventana_gastos,
            text=(
                f"TOTAL DE GASTOS: "
                f"${total_gastos:.2f}"
            ),
            font=("Arial", 13, "bold")
        ).pack(pady=15)

    tk.Button(
        ventana_gastos,
        text="Cerrar",
        width=15,
        command=ventana_gastos.destroy
    ).pack(
        side="bottom",
        pady=20
    )


# ==================================================
# RESUMEN
# ==================================================

def abrir_resumen():
    ventana_resumen = tk.Toplevel(
        ventana
    )

    ventana_resumen.title(
        "Resumen del negocio"
    )

    ventana_resumen.geometry(
        "700x600"
    )

    ventana_resumen.resizable(
        False,
        False
    )

    tk.Label(
        ventana_resumen,
        text="RESUMEN DEL NEGOCIO",
        font=("Arial", 18, "bold")
    ).pack(pady=25)

    total_clientes = len(clientes)
    total_ventas = len(ventas)

    ingresos = sum(
        convertir_numero(
            venta.get("monto", 0)
        )
        for venta in ventas
    )

    gastos_totales = sum(
        convertir_numero(
            gasto.get("monto", 0)
        )
        for gasto in gastos
    )

    capital_inventario = 0
    valor_inventario = 0

    for item in inventario:
        cantidad = int(
            item.get("cantidad", 0)
        )

        precio = convertir_numero(
            item.get("precio", 0)
        )

        costo = convertir_numero(
            item.get("costo", 0)
        )

        capital_inventario += (
            cantidad * costo
        )

        valor_inventario += (
            cantidad * precio
        )

    ganancia_potencial = (
        valor_inventario
        - capital_inventario
    )

    salidas_reposicion = sum(
        convertir_numero(
            reposicion.get(
                "inversion",
                0
            )
        )
        for reposicion in reposiciones
    )

    flujo_caja = (
        ingresos
        - salidas_reposicion
        - gastos_totales
    )

    if flujo_caja > 0:
        estado = "POSITIVO"

    elif flujo_caja < 0:
        estado = "NEGATIVO"

    else:
        estado = "EQUILIBRADO"

    marco = tk.LabelFrame(
        ventana_resumen,
        text="Información general",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=20
    )

    marco.pack(
        fill="x",
        padx=60,
        pady=10
    )

    datos = [
        (
            f"Clientes registrados: "
            f"{total_clientes}"
        ),
        (
            f"Ventas registradas: "
            f"{total_ventas}"
        ),
        (
            f"Ingresos por ventas: "
            f"${ingresos:.2f}"
        ),
        (
            f"Gastos operativos: "
            f"${gastos_totales:.2f}"
        ),
        "",
        (
            f"Capital en inventario: "
            f"${capital_inventario:.2f}"
        ),
        (
            f"Valor del inventario: "
            f"${valor_inventario:.2f}"
        ),
        (
            f"Ganancia potencial: "
            f"${ganancia_potencial:.2f}"
        ),
        "",
        (
            f"Flujo de caja: "
            f"${flujo_caja:.2f}"
        ),
        (
            f"Estado: {estado}"
        )
    ]

    for dato in datos:
        tk.Label(
            marco,
            text=dato,
            font=("Arial", 11),
            anchor="w"
        ).pack(
            anchor="w",
            pady=3
        )

    tk.Button(
        ventana_resumen,
        text="Cerrar",
        width=15,
        command=ventana_resumen.destroy
    ).pack(
        side="bottom",
        pady=25
    )


# ==================================================
# DIAGNÓSTICO INTELIGENTE
# ==================================================

def abrir_diagnostico():
    resultado = calcular_diagnostico(
        ventas,
        inventario,
        reposiciones,
        gastos
    )

    ventana_diagnostico = tk.Toplevel(
        ventana
    )

    ventana_diagnostico.title(
        "Diagnóstico inteligente"
    )

    ventana_diagnostico.geometry(
        "800x650"
    )

    ventana_diagnostico.resizable(
        False,
        False
    )

    tk.Label(
        ventana_diagnostico,
        text="DIAGNÓSTICO INTELIGENTE",
        font=("Arial", 20, "bold")
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        ventana_diagnostico,
        text="Análisis automático del negocio",
        font=("Arial", 11)
    ).pack(
        pady=(0, 20)
    )

    marco_financiero = tk.LabelFrame(
        ventana_diagnostico,
        text="Estado financiero",
        font=("Arial", 12, "bold"),
        padx=25,
        pady=15
    )

    marco_financiero.pack(
        fill="x",
        padx=60,
        pady=5
    )

    tk.Label(
        marco_financiero,
        text=(
            f"Flujo de caja: "
            f"${resultado['flujo_neto']:.2f}"
        ),
        font=("Arial", 11)
    ).pack(anchor="w", pady=3)

    tk.Label(
        marco_financiero,
        text=(
            f"Estado del flujo: "
            f"{resultado['estado_flujo']}"
        ),
        font=("Arial", 11, "bold")
    ).pack(anchor="w", pady=3)

    tk.Label(
        marco_financiero,
        text=(
            f"Ganancia potencial del inventario: "
            f"${resultado['ganancia_potencial']:.2f}"
        ),
        font=("Arial", 11)
    ).pack(anchor="w", pady=3)

    tk.Label(
        marco_financiero,
        text=(
            f"Gastos sobre ventas: "
            f"{resultado['porcentaje_gastos']:.2f}%"
        ),
        font=("Arial", 11)
    ).pack(anchor="w", pady=3)

    marco_analisis = tk.LabelFrame(
        ventana_diagnostico,
        text="Análisis",
        font=("Arial", 12, "bold"),
        padx=25,
        pady=15
    )

    marco_analisis.pack(
        fill="x",
        padx=60,
        pady=10
    )

    for mensaje in resultado["diagnosticos"]:
        tk.Label(
            marco_analisis,
            text=mensaje,
            font=("Arial", 11),
            anchor="w"
        ).pack(
            anchor="w",
            pady=4
        )

    marco_recomendacion = tk.LabelFrame(
        ventana_diagnostico,
        text="Recomendación",
        font=("Arial", 12, "bold"),
        padx=25,
        pady=15
    )

    marco_recomendacion.pack(
        fill="x",
        padx=60,
        pady=10
    )

    tk.Label(
        marco_recomendacion,
        text=resultado["recomendacion"],
        font=("Arial", 11),
        wraplength=620,
        justify="left"
    ).pack(anchor="w")

    if resultado["ventas_sin_costo"] > 0:
        tk.Label(
            ventana_diagnostico,
            text=(
                "IMPORTANTE: Hay "
                f"{resultado['ventas_sin_costo']} "
                "venta(s) histórica(s) sin costo "
                "registrado. El diagnóstico "
                "financiero todavía es parcial."
            ),
            font=("Arial", 10, "bold"),
            wraplength=650,
            justify="left"
        ).pack(
            padx=60,
            pady=10
        )

    tk.Button(
        ventana_diagnostico,
        text="Cerrar",
        width=15,
        command=ventana_diagnostico.destroy
    ).pack(
        side="bottom",
        pady=20
    )


# ==================================================
# VENTANA PRINCIPAL
# ==================================================

ventana = tk.Tk()

ventana.title(
    "AI Business Assistant"
)

ventana.geometry(
    "700x520"
)

ventana.resizable(
    False,
    False
)


tk.Label(
    ventana,
    text="AI BUSINESS ASSISTANT",
    font=("Arial", 22, "bold")
).pack(
    pady=(30, 5)
)


tk.Label(
    ventana,
    text="Panel de administración del negocio",
    font=("Arial", 12)
).pack(
    pady=(0, 30)
)


contenedor = tk.Frame(
    ventana
)

contenedor.pack()


tk.Button(
    contenedor,
    text="Clientes",
    width=20,
    height=3,
    command=abrir_clientes
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


tk.Button(
    contenedor,
    text="Ventas",
    width=20,
    height=3,
    command=abrir_ventas
).grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


tk.Button(
    contenedor,
    text="Inventario",
    width=20,
    height=3,
    command=abrir_inventario
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


tk.Button(
    contenedor,
    text="Gastos",
    width=20,
    height=3,
    command=abrir_gastos
).grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


tk.Button(
    contenedor,
    text="Resumen del negocio",
    width=20,
    height=3,
    command=abrir_resumen
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)


tk.Button(
    contenedor,
    text="Diagnóstico inteligente",
    width=20,
    height=3,
    command=abrir_diagnostico
).grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


tk.Button(
    ventana,
    text="Salir",
    width=15,
    command=ventana.destroy
).pack(
    pady=30
)


ventana.mainloop()