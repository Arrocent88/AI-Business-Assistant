clientes = []

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

            print("Cliente agregado correctamente.")

        elif opcion == "2":
            print("\nLista de clientes:")

            for cliente in clientes:
                print("-" * 30)
                print("Nombre:", cliente["nombre"])
                print("Teléfono:", cliente["telefono"])
                print("Correo:", cliente["correo"])

        elif opcion == "3":
            break

        else:
            print("Opción incorrecta.")