import json
from pathlib import Path

ARCHIVO_INVENTARIO = Path("inventario.json")


def cargar_inventario():
    if ARCHIVO_INVENTARIO.exists():
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return []


def guardar_inventario(inventario):
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


inventario = cargar_inventario()


def mostrar_inventario():

    while True:

        print("\n===== INVENTARIO =====")
        print("1. Agregar producto")
        print("2. Ver inventario")
        print("3. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            producto = input("Nombre del producto: ")
            cantidad = input("Cantidad: ")
            precio = input("Precio: ")

            item = {
                "producto": producto,
                "cantidad": cantidad,
                "precio": precio
            }

            inventario.append(item)
            guardar_inventario(inventario)

            print("Producto agregado correctamente.")

        elif opcion == "2":
            print("\nInventario:")

            if not inventario:
                print("No hay productos registrados.")

            for item in inventario:
                print("-" * 30)
                print("Producto:", item["producto"])
                print("Cantidad:", item["cantidad"])
                print("Precio: $", item["precio"])

        elif opcion == "3":
            break

        else:
            print("Opción incorrecta.")