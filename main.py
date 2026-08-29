from clientes import mostrar_clientes, clientes
from ventas import mostrar_ventas, ventas
from inventario import (
    mostrar_inventario,
    inventario,
    reposiciones
)


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
        ingresos_totales += convertir_numero(
            venta["monto"]
        )

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
        cantidad = int(
            venta.get("cantidad", 1)
        )
        monto = convertir_numero(
            venta["monto"]
        )

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
        print(
            "Unidades vendidas:",
            datos["cantidad"]
        )
        print(
            f"Ingresos generados: "
            f"${datos['ingresos']:.2f}"
        )


def mostrar_alerta_inventario():
    print("\n===== ALERTA DE INVENTARIO =====")

    limite_bajo = 5
    productos_bajos = []

    for item in inventario:

        cantidad = int(
            item["cantidad"]
        )

        if cantidad <= limite_bajo:
            productos_bajos.append(item)

    if not productos_bajos:
        print("Inventario en buen nivel.")
        return

    print(
        "Productos que necesitan reposición:"
    )

    for item in productos_bajos:

        cantidad = int(
            item["cantidad"]
        )

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

        monto = convertir_numero(
            venta["monto"]
        )

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

    print(
        f"Ingresos totales: "
        f"${ingresos_totales:.2f}"
    )

    print(
        f"Costos registrados: "
        f"${costos_totales:.2f}"
    )

    print(
        f"Ganancia neta conocida: "
        f"${ganancia_conocida:.2f}"
    )

    print()

    print(
        "Ventas con costo registrado:",
        ventas_con_costo
    )

    print(
        "Ventas históricas sin costo:",
        ventas_sin_costo
    )

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

        cantidad = int(
            venta.get("cantidad", 1)
        )

        ingreso = convertir_numero(
            venta["monto"]
        )

        ganancia = convertir_numero(
            venta["ganancia"]
        )

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
        print(
            "No hay ventas con costos registrados."
        )
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

        print(
            "Unidades vendidas con costo:",
            datos["cantidad"]
        )

        print(
            f"Ingresos: "
            f"${datos['ingresos']:.2f}"
        )

        print(
            f"Ganancia: "
            f"${datos['ganancia']:.2f}"
        )

        print(
            f"Margen: "
            f"{margen:.2f}%"
        )


def mostrar_plan_reposicion():
    print("\n===== PLAN DE REPOSICIÓN =====")

    limite_bajo = 5
    stock_objetivo = 10

    productos_reponer = []
    inversion_total = 0

    for item in inventario:

        cantidad_actual = int(
            item["cantidad"]
        )

        if cantidad_actual <= limite_bajo:

            if "costo" not in item:

                productos_reponer.append({
                    "producto": item["producto"],
                    "cantidad_actual": cantidad_actual,
                    "faltantes": (
                        stock_objetivo
                        - cantidad_actual
                    ),
                    "costo": None,
                    "inversion": None
                })

                continue

            costo = convertir_numero(
                item["costo"]
            )

            faltantes = (
                stock_objetivo
                - cantidad_actual
            )

            inversion = (
                faltantes * costo
            )

            inversion_total += inversion

            productos_reponer.append({
                "producto": item["producto"],
                "cantidad_actual": cantidad_actual,
                "faltantes": faltantes,
                "costo": costo,
                "inversion": inversion
            })

    if not productos_reponer:

        print(
            "No hay productos que "
            "necesiten reposición."
        )

        return

    for item in productos_reponer:

        print("-" * 30)
        print(
            "Producto:",
            item["producto"]
        )

        print(
            "Stock actual:",
            item["cantidad_actual"]
        )

        print(
            "Stock objetivo:",
            stock_objetivo
        )

        print(
            "Unidades a comprar:",
            item["faltantes"]
        )

        if item["costo"] is None:

            print(
                "Costo unitario: "
                "NO REGISTRADO"
            )

            print(
                "Inversión necesaria: "
                "NO DISPONIBLE"
            )

        else:

            print(
                f"Costo unitario: "
                f"${item['costo']:.2f}"
            )

            print(
                f"Inversión necesaria: "
                f"${item['inversion']:.2f}"
            )

    print("-" * 30)

    print(
        f"Inversión total conocida para reposición: "
        f"${inversion_total:.2f}"
    )


def mostrar_valor_inventario():
    print("\n===== VALOR DEL INVENTARIO =====")

    if not inventario:
        print(
            "No hay productos registrados."
        )
        return

    costo_total_inventario = 0
    valor_venta_total = 0
    productos_sin_costo = 0

    for item in inventario:

        cantidad = int(
            item["cantidad"]
        )

        precio_venta = convertir_numero(
            item["precio"]
        )

        valor_venta = (
            cantidad * precio_venta
        )

        valor_venta_total += valor_venta

        if "costo" in item:

            costo_unitario = convertir_numero(
                item["costo"]
            )

            costo_total = (
                cantidad * costo_unitario
            )

            costo_total_inventario += costo_total

            print("-" * 30)
            print(
                "Producto:",
                item["producto"]
            )

            print(
                "Unidades:",
                cantidad
            )

            print(
                f"Costo unitario: "
                f"${costo_unitario:.2f}"
            )

            print(
                f"Capital invertido: "
                f"${costo_total:.2f}"
            )

            print(
                f"Valor potencial de venta: "
                f"${valor_venta:.2f}"
            )

        else:

            productos_sin_costo += 1

            print("-" * 30)

            print(
                "Producto:",
                item["producto"]
            )

            print(
                "Unidades:",
                cantidad
            )

            print(
                "Costo unitario: "
                "NO REGISTRADO"
            )

            print(
                f"Valor potencial de venta: "
                f"${valor_venta:.2f}"
            )

    ganancia_potencial = (
        valor_venta_total
        - costo_total_inventario
    )

    print("-" * 30)

    print(
        f"Costo total del inventario conocido: "
        f"${costo_total_inventario:.2f}"
    )

    print(
        f"Valor potencial de venta: "
        f"${valor_venta_total:.2f}"
    )

    if productos_sin_costo == 0:

        print(
            f"Ganancia potencial del inventario: "
            f"${ganancia_potencial:.2f}"
        )

        if valor_venta_total > 0:

            margen = (
                ganancia_potencial
                / valor_venta_total
            ) * 100

            print(
                f"Margen potencial: "
                f"{margen:.2f}%"
            )

    else:

        print(
            "Ganancia potencial: "
            "NO DISPONIBLE para todos los productos."
        )


def mostrar_resumen_ejecutivo():
    print("\n===== RESUMEN EJECUTIVO =====")

    ingresos_totales = 0
    ganancia_conocida = 0
    costos_ventas = 0

    for venta in ventas:

        ingresos_totales += convertir_numero(
            venta["monto"]
        )

        if "ganancia" in venta:

            ganancia_conocida += convertir_numero(
                venta["ganancia"]
            )

        if "costo_total" in venta:

            costos_ventas += convertir_numero(
                venta["costo_total"]
            )

    capital_inventario = 0
    valor_venta_inventario = 0

    for item in inventario:

        cantidad = int(
            item["cantidad"]
        )

        precio = convertir_numero(
            item["precio"]
        )

        valor_venta_inventario += (
            cantidad * precio
        )

        if "costo" in item:

            costo = convertir_numero(
                item["costo"]
            )

            capital_inventario += (
                cantidad * costo
            )

    ganancia_potencial_inventario = (
        valor_venta_inventario
        - capital_inventario
    )

    print(
        f"Ingresos históricos: "
        f"${ingresos_totales:.2f}"
    )

    print(
        f"Costos de ventas registrados: "
        f"${costos_ventas:.2f}"
    )

    print(
        f"Ganancia conocida realizada: "
        f"${ganancia_conocida:.2f}"
    )

    print()

    print(
        f"Capital actual en inventario: "
        f"${capital_inventario:.2f}"
    )

    print(
        f"Valor potencial del inventario: "
        f"${valor_venta_inventario:.2f}"
    )

    print(
        f"Ganancia potencial del inventario: "
        f"${ganancia_potencial_inventario:.2f}"
    )

    print()

    print(
        "Clientes registrados:",
        len(clientes)
    )

    print(
        "Ventas registradas:",
        len(ventas)
    )

    unidades = sum(
        int(item["cantidad"])
        for item in inventario
    )

    print(
        "Unidades disponibles:",
        unidades
    )

    valor_negocio_operativo = (
        ganancia_conocida
        + capital_inventario
    )

    print()

    print(
        f"Valor operativo conocido: "
        f"${valor_negocio_operativo:.2f}"
    )


def mostrar_flujo_caja():
    print("\n===== FLUJO DE CAJA =====")

    entradas_ventas = 0

    for venta in ventas:
        entradas_ventas += convertir_numero(
            venta["monto"]
        )

    salidas_reposicion = 0

    for reposicion in reposiciones:

        if "inversion" in reposicion:

            salidas_reposicion += convertir_numero(
                reposicion["inversion"]
            )

    flujo_neto = (
        entradas_ventas
        - salidas_reposicion
    )

    print(
        f"Entradas por ventas: "
        f"${entradas_ventas:.2f}"
    )

    print(
        f"Salidas por reposiciones: "
        f"${salidas_reposicion:.2f}"
    )

    print("-" * 30)

    print(
        f"Flujo de caja neto registrado: "
        f"${flujo_neto:.2f}"
    )

    print()

    print(
        "Ventas registradas:",
        len(ventas)
    )

    print(
        "Reposiciones registradas:",
        len(reposiciones)
    )

    if flujo_neto > 0:
        print("Estado del flujo: POSITIVO")

    elif flujo_neto < 0:
        print("Estado del flujo: NEGATIVO")

    else:
        print("Estado del flujo: EQUILIBRADO")

    print()

    print(
        "Nota: Este flujo utiliza únicamente "
        "movimientos registrados en el sistema."
    )


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
    print("10. Plan de reposición")
    print("11. Valor del inventario")
    print("12. Resumen ejecutivo")
    print("13. Flujo de caja")
    print("14. Salir")

    opcion = input(
        "Selecciona una opción: "
    )

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
        mostrar_plan_reposicion()

    elif opcion == "11":
        mostrar_valor_inventario()

    elif opcion == "12":
        mostrar_resumen_ejecutivo()

    elif opcion == "13":
        mostrar_flujo_caja()

    elif opcion == "14":
        print("Hasta luego.")
        break

    else:
        print("Opción incorrecta.")

    input(
        "\nPresiona ENTER para volver al menú..."
    )

    print()