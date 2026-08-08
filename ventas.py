import json
from pathlib import Path

ARCHIVO_VENTAS = Path("ventas.json")


def cargar_ventas():
    if ARCHIVO_VENTAS.exists():
        with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return []


def guardar_ventas(ventas):
    with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as archivo:
        json.dump(ventas, archivo, indent=4, ensure_ascii=False)


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
            producto = input("Producto o servicio: ")
            monto = input("Monto de la venta: ")

            venta = {
                "cliente": cliente,
                "producto": producto,
                "monto": monto
            }

            ventas.append(venta)
            guardar_ventas(ventas)

            print("Venta registrada correctamente.")

        elif opcion == "2":
            print("\nLista de ventas:")

            if not ventas:
                print("No hay ventas registradas.")

            for venta in ventas:
                print("-" * 30)
                print("Cliente:", venta["cliente"])
                print("Producto:", venta["producto"])
                print("Monto: $", venta["monto"])

        elif opcion == "3":
            break

        else:
            print("Opción incorrecta.")