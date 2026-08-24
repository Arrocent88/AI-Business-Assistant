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
        json.dump(
            inventario,
            archivo,
            indent=4,
            ensure_ascii=False
        )


inventario = cargar_inventario()


def limpiar_precio(precio):
    precio_limpio = str(precio).replace("$", "").strip()
    return float(precio_limpio)


def obtener_precio_producto(nombre_producto):
    for item in inventario:
        if item["producto"].lower() == nombre_producto.lower():
            return limpiar_precio(item["precio"])

    return None


def obtener_costo_producto(nombre_producto):
    for item in inventario:
        if item["producto"].lower() == nombre_producto.lower():

            if "costo" not in item:
                return None

            return limpiar_precio(item["costo"])

    return None


def obtener_productos_disponibles():
    productos = []

    for item in inventario:
        cantidad = int(item["cantidad"])

        if cantidad > 0:

            costo = None

            if "costo" in item:
                costo = limpiar_precio(item["costo"])

            productos.append({
                "producto": item["producto"],
                "cantidad": cantidad,
                "precio": limpiar_precio(item["precio"]),
                "costo": costo
            })

    return productos


def descontar_inventario(nombre_producto, cantidad_vendida):
    for item in inventario:

        if item["producto"].lower() == nombre_producto.lower():

            cantidad_actual = int(item["cantidad"])

            if cantidad_actual < cantidad_vendida:
                return False

            item["cantidad"] = str(
                cantidad_actual - cantidad_vendida
            )

            guardar_inventario(inventario)

            return True

    return False


def mostrar_inventario():

    while True:

        print("\n===== INVENTARIO =====")
        print("1. Agregar producto")
        print("2. Ver inventario")
        print("3. Actualizar costo de producto")
        print("4. Regresar")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":

            producto = input("Nombre del producto: ").strip()
            cantidad = input("Cantidad: ").strip()
            costo = input("Costo de compra por unidad: $").strip()
            precio = input("Precio de venta por unidad: $").strip()

            item = {
                "producto": producto,
                "cantidad": cantidad,
                "costo": costo,
                "precio": precio
            }

            inventario.append(item)
            guardar_inventario(inventario)

            print("Producto agregado correctamente.")

        elif opcion == "2":

            print("\nInventario:")

            if not inventario:
                print("No hay productos registrados.")
                continue

            for item in inventario:

                print("-" * 30)
                print("Producto:", item["producto"])
                print("Cantidad:", item["cantidad"])

                if "costo" in item:
                    costo = limpiar_precio(item["costo"])
                    print(f"Costo de compra: ${costo:.2f}")
                else:
                    print("Costo de compra: NO REGISTRADO")

                precio = limpiar_precio(item["precio"])
                print(f"Precio de venta: ${precio:.2f}")

                if "costo" in item:
                    ganancia_unitaria = precio - costo
                    print(
                        f"Ganancia estimada por unidad: "
                        f"${ganancia_unitaria:.2f}"
                    )

        elif opcion == "3":

            if not inventario:
                print("No hay productos registrados.")
                continue

            print("\n===== PRODUCTOS =====")

            for numero, item in enumerate(inventario, start=1):
                print(f"{numero}. {item['producto']}")

            try:
                seleccion = int(
                    input("\nSelecciona el número del producto: ")
                )

                if seleccion < 1 or seleccion > len(inventario):
                    print("Producto seleccionado incorrecto.")
                    continue

                producto_seleccionado = inventario[seleccion - 1]

                nuevo_costo = input(
                    f"Costo de compra de "
                    f"{producto_seleccionado['producto']}: $"
                ).strip()

                nuevo_costo = limpiar_precio(nuevo_costo)

                if nuevo_costo < 0:
                    print("El costo no puede ser negativo.")
                    continue

                producto_seleccionado["costo"] = nuevo_costo

                guardar_inventario(inventario)

                print("\nCosto actualizado correctamente.")
                print(
                    f"Producto: "
                    f"{producto_seleccionado['producto']}"
                )
                print(f"Costo de compra: ${nuevo_costo:.2f}")

            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "4":
            break

        else:
            print("Opción incorrecta.")