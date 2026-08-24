import json
from pathlib import Path

from clientes import obtener_clientes_disponibles
from inventario import (
    descontar_inventario,
    obtener_productos_disponibles
)

ARCHIVO_VENTAS = Path("ventas.json")


def cargar_ventas():
    if ARCHIVO_VENTAS.exists():
        with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return []


def guardar_ventas(ventas):
    with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as archivo:
        json.dump(
            ventas,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def limpiar_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


ventas = cargar_ventas()


def mostrar_ventas():

    while True:

        print("\n===== VENTAS =====")
        print("1. Registrar venta")
        print("2. Ver ventas")
        print("3. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":

            clientes = obtener_clientes_disponibles()

            if not clientes:
                print("No hay clientes registrados.")
                continue

            print("\n===== CLIENTES DISPONIBLES =====")

            for numero, cliente in enumerate(clientes, start=1):
                print(f"{numero}. {cliente['nombre']}")

            try:
                seleccion_cliente = int(
                    input("\nSelecciona el número del cliente: ")
                )

                if (
                    seleccion_cliente < 1
                    or seleccion_cliente > len(clientes)
                ):
                    print("Cliente seleccionado incorrecto.")
                    continue

                cliente_seleccionado = clientes[
                    seleccion_cliente - 1
                ]

                cliente = cliente_seleccionado["nombre"]

            except ValueError:
                print("Debes ingresar un número válido.")
                continue

            productos = obtener_productos_disponibles()

            if not productos:
                print("No hay productos disponibles en inventario.")
                continue

            print("\n===== PRODUCTOS DISPONIBLES =====")

            for numero, item in enumerate(productos, start=1):

                texto = (
                    f"{numero}. {item['producto']} | "
                    f"Stock: {item['cantidad']} | "
                    f"Precio: ${item['precio']:.2f}"
                )

                if item.get("costo") is not None:
                    texto += f" | Costo: ${item['costo']:.2f}"

                print(texto)

            try:
                seleccion_producto = int(
                    input("\nSelecciona el número del producto: ")
                )

                if (
                    seleccion_producto < 1
                    or seleccion_producto > len(productos)
                ):
                    print("Producto seleccionado incorrecto.")
                    continue

                producto_seleccionado = productos[
                    seleccion_producto - 1
                ]

                producto = producto_seleccionado["producto"]
                precio_unitario = producto_seleccionado["precio"]
                costo_unitario = producto_seleccionado.get("costo")

                cantidad = int(
                    input("Cantidad vendida: ")
                )

                if cantidad <= 0:
                    print("La cantidad debe ser mayor que cero.")
                    continue

            except ValueError:
                print("Debes ingresar un número válido.")
                continue

            monto = cantidad * precio_unitario

            costo_total = None
            ganancia = None

            if costo_unitario is not None:
                costo_total = cantidad * costo_unitario
                ganancia = monto - costo_total

            if descontar_inventario(producto, cantidad):

                venta = {
                    "cliente": cliente,
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "monto": monto
                }

                if costo_unitario is not None:
                    venta["costo_unitario"] = costo_unitario
                    venta["costo_total"] = costo_total
                    venta["ganancia"] = ganancia

                ventas.append(venta)
                guardar_ventas(ventas)

                print("\nVenta registrada correctamente.")
                print("Inventario actualizado correctamente.")
                print(f"Cliente: {cliente}")
                print(f"Producto: {producto}")
                print(f"Precio unitario: ${precio_unitario:.2f}")
                print(f"Cantidad: {cantidad}")
                print(f"Total de la venta: ${monto:.2f}")

                if costo_unitario is not None:
                    print(f"Costo unitario: ${costo_unitario:.2f}")
                    print(f"Costo total: ${costo_total:.2f}")
                    print(f"Ganancia de la venta: ${ganancia:.2f}")
                else:
                    print(
                        "Ganancia: NO DISPONIBLE "
                        "(producto sin costo registrado)"
                    )

            else:
                print("\nNo se pudo registrar la venta.")
                print("Inventario insuficiente.")

        elif opcion == "2":

            print("\n===== LISTA DE VENTAS =====")

            if not ventas:
                print("No hay ventas registradas.")
                continue

            for venta in ventas:

                print("-" * 30)
                print("Cliente:", venta["cliente"])
                print("Producto:", venta["producto"])

                if "cantidad" in venta:
                    print("Cantidad:", venta["cantidad"])

                if "precio_unitario" in venta:
                    precio = limpiar_numero(
                        venta["precio_unitario"]
                    )
                    print(f"Precio unitario: ${precio:.2f}")

                monto = limpiar_numero(venta["monto"])
                print(f"Monto: ${monto:.2f}")

                if "costo_unitario" in venta:
                    costo_unitario = limpiar_numero(
                        venta["costo_unitario"]
                    )
                    print(
                        f"Costo unitario: "
                        f"${costo_unitario:.2f}"
                    )

                if "costo_total" in venta:
                    costo_total = limpiar_numero(
                        venta["costo_total"]
                    )
                    print(
                        f"Costo total: "
                        f"${costo_total:.2f}"
                    )

                if "ganancia" in venta:
                    ganancia = limpiar_numero(
                        venta["ganancia"]
                    )
                    print(
                        f"Ganancia: "
                        f"${ganancia:.2f}"
                    )

        elif opcion == "3":
            break

        else:
            print("Opción incorrecta.")