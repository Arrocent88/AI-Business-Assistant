from clientes import mostrar_clientes
from ventas import mostrar_ventas
from inventario import mostrar_inventario

while True:

    print("=" * 50)
    print("      AI BUSINESS ASSISTANT")
    print("=" * 50)

    print("1. Clientes")
    print("2. Ventas")
    print("3. Inventario")
    print("4. Salir")

    opcion = input("Selecciona una opción: ")

    print()

    if opcion == "1":
        mostrar_clientes()

    elif opcion == "2":
        mostrar_ventas()

    elif opcion == "3":
        mostrar_inventario()

    elif opcion == "4":
        print("Hasta luego.")
        break

    else:
        print("Opción incorrecta.")

    input("\nPresiona ENTER para volver al menú...")
    print()