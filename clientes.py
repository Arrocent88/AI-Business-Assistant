import json
from pathlib import Path

ARCHIVO = Path("clientes.json")


def cargar_clientes():
    if ARCHIVO.exists():
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return []


def guardar_clientes(clientes):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)


clientes = cargar_clientes()


def mostrar_clientes():

    while True:

        print("\n===== CLIENTES =====")
        print("1. Agregar cliente")
        print("2. Ver clientes")
        print("3. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre del cliente: ")
            telefono = input("Teléfono: ")
            correo = input("Correo: ")

            cliente = {
                "nombre": nombre,
                "telefono": telefono,
                "correo": correo
            }

            clientes.append(cliente)
            guardar_clientes(clientes)

            print("Cliente agregado correctamente.")

        elif opcion == "2":
            print("\nLista de clientes:")

            if not clientes:
                print("No hay clientes registrados.")

            for cliente in clientes:
                print("-" * 30)
                print("Nombre:", cliente["nombre"])
                print("Teléfono:", cliente["telefono"])
                print("Correo:", cliente["correo"])

        elif opcion == "3":
            break

        else:
            print("Opción incorrecta.")