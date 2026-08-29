from clientes import mostrar_clientes, clientes
from ventas import mostrar_ventas, ventas
from inventario import mostrar_inventario, inventario


def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def mostrar_resumen():
    total_clientes = len(clientes)
    total_productos = len(inventario)

    unidades_disponibles = 0
    for item in inventario:
        unidades_disponibles += int(item["cantidad"])

    ingresos_totales = 0
    for venta in ventas:
        ingresos_totales += convertir_numero(venta["monto"])

    print("\n===== RESUMEN DEL NEGOCIO =====")
    print("Clientes registrados:", total_clientes)
    print("Productos en inventario:", total_productos)
    print("Unidades disponibles:", unidades_disponibles)
    print("Ventas registradas:", len(ventas))
    print(f"Ingresos totales: ${ingresos_totales:.2f}")


def mostrar_reporte_clientes():
    print("\n===== REPORTE POR CLIENTE =====")

    if not clientes:
        print("No hay clientes registrados.")
        return

    for cliente in clientes:
        nombre = cliente["nombre"]

        ventas_cliente = [
            venta
            for venta in ventas
            if venta["cliente"].lower() == nombre.lower()
        ]

        total_comprado = 0

        for venta in ventas_cliente:
            total_comprado += convertir_numero(
                venta["monto"]
            )

        print("-" * 30)
        print("Cliente:", nombre)
        print("Ventas realizadas:", len(ventas_cliente))
        print(f"Total comprado: ${total_comprado:.2f}")


def mostrar_productos_mas_vendidos():
    print("\n===== PRODUCTOS MÁS VENDIDOS =====")

    if not ventas:
        print("No hay ventas registradas.")
        return

    reporte = {}

    for venta in ventas:
        producto = venta["producto"]
        cantidad = int(venta.get("cantidad", 1))
        monto = convertir_numero(venta["monto"])

        if producto not in reporte:
            reporte[producto] = {
                "cantidad": 0,
                "ingresos": 0
            }

        reporte[producto]["cantidad"] += cantidad
        reporte[producto]["ingresos"] += monto

    productos_ordenados = sorted(
        reporte.items(),
        key=lambda item: item[1]["cantidad"],
        reverse=True
    )

    for posicion, (producto, datos) in enumerate(
        productos_ordenados,
        start=1
    ):
        print("-" * 30)
        print(f"{posicion}. {producto}")
        print("Unidades vendidas:", datos["cantidad"])
        print(
            f"Ingresos generados: "
            f"${datos['ingresos']:.2f}"
        )


def mostrar_alerta_inventario():
    print("\n===== ALERTA DE INVENTARIO =====")

    limite_bajo = 5
    productos_bajos = []

    for item in inventario:
        cantidad = int(item["cantidad"])

        if cantidad <= limite_bajo:
            productos_bajos.append(item)

    if not productos_bajos:
        print("Inventario en buen nivel.")
        return

    print("Productos que necesitan reposición:")

    for item in productos_bajos:
        cantidad = int(item["cantidad"])
        producto = item["producto"]

        print("-" * 30)
        print("Producto:", producto)
        print("Stock actual:", cantidad)

        if cantidad == 0:
            print("Estado: AGOTADO")
        else:
            print("Estado: STOCK BAJO")


def mostrar_reporte_financiero():
    print("\n===== REPORTE FINANCIERO =====")

    if not ventas:
        print("No hay ventas registradas.")
        return

    ingresos_totales = 0
    ingresos_con_costo = 0
    costos_totales = 0
    ganancia_conocida = 0
    ventas_con_costo = 0
    ventas_sin_costo = 0

    for venta in ventas:
        monto = convertir_numero(venta["monto"])
        ingresos_totales += monto

        if (
            "costo_total" in venta
            and "ganancia" in venta
        ):
            costo_total = convertir_numero(
                venta["costo_total"]
            )

            ganancia = convertir_numero(
                venta["ganancia"]
            )

            ingresos_con_costo += monto
            costos_totales += costo_total
            ganancia_conocida += ganancia
            ventas_con_costo += 1

        else:
            ventas_sin_costo += 1

    print(f"Ingresos totales: ${ingresos_totales:.2f}")
    print(f"Costos registrados: ${costos_totales:.2f}")
    print(
        f"Ganancia neta conocida: "
        f"${ganancia_conocida:.2f}"
    )
    print()
    print("Ventas con costo registrado:", ventas_con_costo)
    print("Ventas históricas sin costo:", ventas_sin_costo)

    if ventas_sin_costo > 0:
        print()
        print(
            "Nota: La ganancia neta no incluye las "
            "ventas antiguas que no tienen costo registrado."
        )

    if ingresos_con_costo > 0:
        margen = (
            ganancia_conocida
            / ingresos_con_costo
        ) * 100

        print(
            f"Margen sobre ventas con costo: "
            f"{margen:.2f}%"
        )


def mostrar_ganancia_por_producto():
    print("\n===== GANANCIA POR PRODUCTO =====")

    reporte = {}

    for venta in ventas:

        if "ganancia" not in venta:
            continue

        producto = venta["producto"]
        cantidad = int(venta.get("cantidad", 1))
        ingreso = convertir_numero(venta["monto"])
        ganancia = convertir_numero(venta["ganancia"])

        if producto not in reporte:
            reporte[producto] = {
                "cantidad": 0,
                "ingresos": 0,
                "ganancia": 0
            }

        reporte[producto]["cantidad"] += cantidad
        reporte[producto]["ingresos"] += ingreso
        reporte[producto]["ganancia"] += ganancia

    if not reporte:
        print("No hay ventas con costos registrados.")
        return

    productos_ordenados = sorted(
        reporte.items(),
        key=lambda item: item[1]["ganancia"],
        reverse=True
    )

    for posicion, (producto, datos) in enumerate(
        productos_ordenados,
        start=1
    ):
        margen = 0

        if datos["ingresos"] > 0:
            margen = (
                datos["ganancia"]
                / datos["ingresos"]
            ) * 100

        print("-" * 30)
        print(f"{posicion}. {producto}")
        print("Unidades vendidas con costo:", datos["cantidad"])
        print(f"Ingresos: ${datos['ingresos']:.2f}")
        print(f"Ganancia: ${datos['ganancia']:.2f}")
        print(f"Margen: {margen:.2f}%")


while True:
    print("=" * 50)
    print("       AI BUSINESS ASSISTANT")
    print("=" * 50)

    print("1. Clientes")
    print("2. Ventas")
    print("3. Inventario")
    print("4. Resumen del negocio")
    print("5. Reporte por cliente")
    print("6. Productos más vendidos")
    print("7. Alerta de inventario")
    print("8. Reporte financiero")
    print("9. Ganancia por producto")
    print("10. Salir")

    opcion = input("Selecciona una opción: ")

    print()

    if opcion == "1":
        mostrar_clientes()

    elif opcion == "2":
        mostrar_ventas()

    elif opcion == "3":
        mostrar_inventario()

    elif opcion == "4":
        mostrar_resumen()

    elif opcion == "5":
        mostrar_reporte_clientes()

    elif opcion == "6":
        mostrar_productos_mas_vendidos()

    elif opcion == "7":
        mostrar_alerta_inventario()

    elif opcion == "8":
        mostrar_reporte_financiero()

    elif opcion == "9":
        mostrar_ganancia_por_producto()

    elif opcion == "10":
        print("Hasta luego.")
        break

    else:
        print("Opción incorrecta.")

    input("\nPresiona ENTER para volver al menú...")
    print()