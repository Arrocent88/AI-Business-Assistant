import json
from pathlib import Path

ARCHIVO_INVENTARIO = Path("inventario.json")
ARCHIVO_REPOSICIONES = Path("reposiciones.json")


def cargar_inventario():
    if ARCHIVO_INVENTARIO.exists():
        with open(
            ARCHIVO_INVENTARIO,
            "r",
            encoding="utf-8"
        ) as archivo:
            return json.load(archivo)

    return []


def guardar_inventario(inventario):
    with open(
        ARCHIVO_INVENTARIO,
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            inventario,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def cargar_reposiciones():
    if ARCHIVO_REPOSICIONES.exists():
        with open(
            ARCHIVO_REPOSICIONES,
            "r",
            encoding="utf-8"
        ) as archivo:
            return json.load(archivo)

    return []


def guardar_reposiciones(reposiciones):
    with open(
        ARCHIVO_REPOSICIONES,
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            reposiciones,
            archivo,
            indent=4,
            ensure_ascii=False
        )


inventario = cargar_inventario()
reposiciones = cargar_reposiciones()


def limpiar_precio(precio):
    precio_limpio = (
        str(precio)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    return float(precio_limpio)


def obtener_precio_producto(nombre_producto):
    for item in inventario:

        if (
            item["producto"].lower()
            == nombre_producto.lower()
        ):
            return limpiar_precio(
                item["precio"]
            )

    return None


def obtener_costo_producto(nombre_producto):
    for item in inventario:

        if (
            item["producto"].lower()
            == nombre_producto.lower()
        ):

            if "costo" not in item:
                return None

            return limpiar_precio(
                item["costo"]
            )

    return None


def obtener_productos_disponibles():
    productos = []

    for item in inventario:

        cantidad = int(item["cantidad"])

        if cantidad > 0:

            costo = None

            if "costo" in item:
                costo = limpiar_precio(
                    item["costo"]
                )

            productos.append({
                "producto": item["producto"],
                "cantidad": cantidad,
                "precio": limpiar_precio(
                    item["precio"]
                ),
                "costo": costo
            })

    return productos


def descontar_inventario(
    nombre_producto,
    cantidad_vendida
):
    for item in inventario:

        if (
            item["producto"].lower()
            == nombre_producto.lower()
        ):

            cantidad_actual = int(
                item["cantidad"]
            )

            if (
                cantidad_actual
                < cantidad_vendida
            ):
                return False

            item["cantidad"] = str(
                cantidad_actual
                - cantidad_vendida
            )

            guardar_inventario(
                inventario
            )

            return True

    return False


def registrar_reposicion():

    if not inventario:
        print(
            "No hay productos registrados."
        )
        return

    print(
        "\n===== REGISTRAR REPOSICIÓN ====="
    )

    for numero, item in enumerate(
        inventario,
        start=1
    ):
        print(
            f"{numero}. "
            f"{item['producto']} | "
            f"Stock: {item['cantidad']}"
        )

    try:
        seleccion = int(
            input(
                "\nSelecciona el número "
                "del producto: "
            )
        )

        if (
            seleccion < 1
            or seleccion > len(inventario)
        ):
            print(
                "Producto seleccionado "
                "incorrecto."
            )
            return

        producto = inventario[
            seleccion - 1
        ]

        cantidad_nueva = int(
            input(
                "Cantidad comprada: "
            )
        )

        if cantidad_nueva <= 0:
            print(
                "La cantidad debe ser "
                "mayor que cero."
            )
            return

        nuevo_costo = limpiar_precio(
            input(
                "Costo de compra por "
                "unidad: $"
            )
        )

        if nuevo_costo < 0:
            print(
                "El costo no puede "
                "ser negativo."
            )
            return

    except ValueError:
        print(
            "Debes ingresar un número válido."
        )
        return

    cantidad_actual = int(
        producto["cantidad"]
    )

    costo_actual = None

    if "costo" in producto:
        costo_actual = limpiar_precio(
            producto["costo"]
        )

    inversion = (
        cantidad_nueva
        * nuevo_costo
    )

    nueva_cantidad = (
        cantidad_actual
        + cantidad_nueva
    )

    if (
        costo_actual is not None
        and cantidad_actual > 0
    ):

        valor_inventario_actual = (
            cantidad_actual
            * costo_actual
        )

        valor_compra_nueva = (
            cantidad_nueva
            * nuevo_costo
        )

        costo_promedio = (
            valor_inventario_actual
            + valor_compra_nueva
        ) / nueva_cantidad

    else:
        costo_promedio = nuevo_costo

    producto["cantidad"] = str(
        nueva_cantidad
    )

    producto["costo"] = round(
        costo_promedio,
        2
    )

    movimiento = {
        "producto": producto["producto"],
        "cantidad_comprada": cantidad_nueva,
        "costo_unitario": nuevo_costo,
        "inversion": inversion,
        "stock_anterior": cantidad_actual,
        "stock_nuevo": nueva_cantidad,
        "costo_promedio_nuevo": round(
            costo_promedio,
            2
        )
    }

    reposiciones.append(
        movimiento
    )

    guardar_inventario(
        inventario
    )

    guardar_reposiciones(
        reposiciones
    )

    print(
        "\nReposición registrada correctamente."
    )

    print(
        f"Producto: "
        f"{producto['producto']}"
    )

    print(
        f"Stock anterior: "
        f"{cantidad_actual}"
    )

    print(
        f"Unidades compradas: "
        f"{cantidad_nueva}"
    )

    print(
        f"Stock nuevo: "
        f"{nueva_cantidad}"
    )

    print(
        f"Inversión realizada: "
        f"${inversion:.2f}"
    )

    print(
        f"Nuevo costo promedio: "
        f"${costo_promedio:.2f}"
    )


def mostrar_reposiciones():

    print(
        "\n===== HISTORIAL DE REPOSICIONES ====="
    )

    if not reposiciones:
        print(
            "No hay reposiciones registradas."
        )
        return

    inversion_total = 0

    for numero, movimiento in enumerate(
        reposiciones,
        start=1
    ):

        inversion_total += limpiar_precio(
            movimiento["inversion"]
        )

        print("-" * 30)
        print(
            f"{numero}. "
            f"{movimiento['producto']}"
        )

        print(
            "Cantidad comprada:",
            movimiento["cantidad_comprada"]
        )

        print(
            f"Costo unitario: "
            f"${limpiar_precio(
                movimiento['costo_unitario']
            ):.2f}"
        )

        print(
            f"Inversión: "
            f"${limpiar_precio(
                movimiento['inversion']
            ):.2f}"
        )

        print(
            "Stock anterior:",
            movimiento["stock_anterior"]
        )

        print(
            "Stock nuevo:",
            movimiento["stock_nuevo"]
        )

    print("-" * 30)

    print(
        f"Inversión total en reposiciones: "
        f"${inversion_total:.2f}"
    )


def mostrar_inventario():

    while True:

        print(
            "\n===== INVENTARIO ====="
        )

        print(
            "1. Agregar producto"
        )

        print(
            "2. Ver inventario"
        )

        print(
            "3. Actualizar costo de producto"
        )

        print(
            "4. Registrar reposición"
        )

        print(
            "5. Ver reposiciones"
        )

        print(
            "6. Regresar"
        )

        opcion = input(
            "Selecciona una opción: "
        )

        if opcion == "1":

            producto = input(
                "Nombre del producto: "
            ).strip()

            cantidad = input(
                "Cantidad: "
            ).strip()

            costo = input(
                "Costo de compra por unidad: $"
            ).strip()

            precio = input(
                "Precio de venta por unidad: $"
            ).strip()

            item = {
                "producto": producto,
                "cantidad": cantidad,
                "costo": costo,
                "precio": precio
            }

            inventario.append(
                item
            )

            guardar_inventario(
                inventario
            )

            print(
                "Producto agregado correctamente."
            )

        elif opcion == "2":

            print(
                "\nInventario:"
            )

            if not inventario:
                print(
                    "No hay productos registrados."
                )
                continue

            for item in inventario:

                print("-" * 30)

                print(
                    "Producto:",
                    item["producto"]
                )

                print(
                    "Cantidad:",
                    item["cantidad"]
                )

                if "costo" in item:

                    costo = limpiar_precio(
                        item["costo"]
                    )

                    print(
                        f"Costo de compra: "
                        f"${costo:.2f}"
                    )

                else:
                    print(
                        "Costo de compra: "
                        "NO REGISTRADO"
                    )

                precio = limpiar_precio(
                    item["precio"]
                )

                print(
                    f"Precio de venta: "
                    f"${precio:.2f}"
                )

                if "costo" in item:

                    ganancia_unitaria = (
                        precio - costo
                    )

                    print(
                        "Ganancia estimada "
                        "por unidad: "
                        f"${ganancia_unitaria:.2f}"
                    )

        elif opcion == "3":

            if not inventario:
                print(
                    "No hay productos registrados."
                )
                continue

            print(
                "\n===== PRODUCTOS ====="
            )

            for numero, item in enumerate(
                inventario,
                start=1
            ):
                print(
                    f"{numero}. "
                    f"{item['producto']}"
                )

            try:
                seleccion = int(
                    input(
                        "\nSelecciona el número "
                        "del producto: "
                    )
                )

                if (
                    seleccion < 1
                    or seleccion > len(inventario)
                ):
                    print(
                        "Producto seleccionado "
                        "incorrecto."
                    )
                    continue

                producto_seleccionado = (
                    inventario[
                        seleccion - 1
                    ]
                )

                nuevo_costo = input(
                    f"Costo de compra de "
                    f"{producto_seleccionado['producto']}: $"
                ).strip()

                nuevo_costo = limpiar_precio(
                    nuevo_costo
                )

                if nuevo_costo < 0:
                    print(
                        "El costo no puede "
                        "ser negativo."
                    )
                    continue

                producto_seleccionado[
                    "costo"
                ] = nuevo_costo

                guardar_inventario(
                    inventario
                )

                print(
                    "\nCosto actualizado correctamente."
                )

                print(
                    f"Producto: "
                    f"{producto_seleccionado['producto']}"
                )

                print(
                    f"Costo de compra: "
                    f"${nuevo_costo:.2f}"
                )

            except ValueError:
                print(
                    "Debes ingresar un "
                    "número válido."
                )

        elif opcion == "4":
            registrar_reposicion()

        elif opcion == "5":
            mostrar_reposiciones()

        elif opcion == "6":
            break

        else:
            print(
                "Opción incorrecta."
            )