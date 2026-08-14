import json
from pathlib import Path

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


ventas = cargar_ventas()


def mostrar_ventas():

    while True:

        print("\n===== VENTAS =====")
        print("1. Registrar venta")
        print("2. Ver ventas")
        print("3. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":

            cliente = input("Nombre del cliente: ")

            productos = obtener_productos_disponibles()

            if not productos:
                print("No hay productos disponibles en inventario.")
                continue

            print("\n===== PRODUCTOS DISPONIBLES =====")

            for numero, item in enumerate(productos, start=1):
                print(
                    f"{numero}. {item['producto']} | "
                    f"Stock: {item['cantidad']} | "
                    f"Precio: ${item['precio']:.2f}"
                )

            try:
                seleccion = int(
                    input("\nSelecciona el número del producto: ")
                )

                if seleccion < 1 or seleccion > len(productos):
                    print("Producto seleccionado incorrecto.")
                    continue

                producto_seleccionado = productos[seleccion - 1]

                producto = producto_seleccionado["producto"]
                precio_unitario = producto_seleccionado["precio"]

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

            if descontar_inventario(producto, cantidad):

                venta = {
                    "cliente": cliente,
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "monto": monto
                }

                ventas.append(venta)
                guardar_ventas(ventas)

                print("\nVenta registrada correctamente.")
                print("Inventario actualizado correctamente.")
                print(f"Precio unitario: ${precio_unitario:.2f}")
                print(f"Total de la venta: ${monto:.2f}")

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
                    print(
                        f"Precio unitario: "
                        f"${float(venta['precio_unitario']):.2f}"
                    )

                monto = str(venta["monto"]).replace("$", "").strip()

                try:
                    print(f"Monto: ${float(monto):.2f}")
                except ValueError:
                    print("Monto:", venta["monto"])

        elif opcion == "3":
            break

        else:
            print("Opción incorrecta.")