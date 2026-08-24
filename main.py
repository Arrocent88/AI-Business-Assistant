from clientes import mostrar_clientes, clientes
from ventas import mostrar_ventas, ventas
from inventario import mostrar_inventario, inventario


def mostrar_resumen():
    total_clientes = len(clientes)
    total_productos = len(inventario)

    unidades_disponibles = 0

    for item in inventario:
        unidades_disponibles += int(item["cantidad"])

    ingresos_totales = 0

    for venta in ventas:
        monto = str(venta["monto"]).replace("$", "").strip()
        ingresos_totales += float(monto)

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
            monto = str(venta["monto"]).replace("$", "").strip()
            total_comprado += float(monto)

        print("-" * 30)
        print("Cliente:", nombre)
        print("Ventas realizadas:", len(ventas_cliente))
        print(f"Total comprado: ${total_comprado:.2f}")


while True:

    print("=" * 50)
    print("       AI BUSINESS ASSISTANT")
    print("=" * 50)

    print("1. Clientes")
    print("2. Ventas")
    print("3. Inventario")
    print("4. Resumen del negocio")
    print("5. Reporte por cliente")
    print("6. Salir")

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
        print("Hasta luego.")
        break

    else:
        print("Opción incorrecta.")

    input("\nPresiona ENTER para volver al menú...")
    print()