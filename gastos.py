import json
from pathlib import Path
from datetime import datetime


ARCHIVO_GASTOS = Path("gastos.json")


def cargar_gastos():
    if ARCHIVO_GASTOS.exists():
        try:
            with open(ARCHIVO_GASTOS, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError):
            return []

    return []


def guardar_gastos(lista_gastos):
    with open(ARCHIVO_GASTOS, "w", encoding="utf-8") as archivo:
        json.dump(
            lista_gastos,
            archivo,
            indent=4,
            ensure_ascii=False
        )


gastos = cargar_gastos()


def limpiar_monto(valor):
    valor_limpio = str(valor).replace("$", "").replace(",", "").strip()
    return float(valor_limpio)


def registrar_gasto():
    print("\n===== REGISTRAR GASTO =====")

    descripcion = input("Descripción del gasto: ").strip()

    if not descripcion:
        print("La descripción no puede estar vacía.")
        return

    categoria = input("Categoría del gasto: ").strip()

    if not categoria:
        categoria = "Sin categoría"

    try:
        monto = limpiar_monto(
            input("Monto del gasto: $")
        )

        if monto <= 0:
            print("El monto debe ser mayor que cero.")
            return

    except ValueError:
        print("Debes ingresar un monto válido.")
        return

    fecha = datetime.now().strftime("%Y-%m-%d")

    gasto = {
        "descripcion": descripcion,
        "categoria": categoria,
        "monto": monto,
        "fecha": fecha
    }

    gastos.append(gasto)
    guardar_gastos(gastos)

    print("\nGasto registrado correctamente.")
    print(f"Descripción: {descripcion}")
    print(f"Categoría: {categoria}")
    print(f"Monto: ${monto:.2f}")
    print(f"Fecha: {fecha}")


def mostrar_lista_gastos():
    print("\n===== LISTA DE GASTOS =====")

    if not gastos:
        print("No hay gastos registrados.")
        return

    total_gastos = 0

    for numero, gasto in enumerate(gastos, start=1):

        descripcion = gasto.get(
            "descripcion",
            gasto.get("concepto", "Sin descripción")
        )

        categoria = gasto.get(
            "categoria",
            "Sin categoría"
        )

        fecha = gasto.get(
            "fecha",
            "Sin fecha"
        )

        try:
            monto = limpiar_monto(
                gasto.get("monto", 0)
            )
        except (ValueError, TypeError):
            monto = 0

        total_gastos += monto

        print("-" * 35)
        print(f"{numero}. {descripcion}")
        print(f"Categoría: {categoria}")
        print(f"Monto: ${monto:.2f}")
        print(f"Fecha: {fecha}")

    print("-" * 35)
    print(f"Total de gastos: ${total_gastos:.2f}")


def obtener_total_gastos():
    total = 0

    for gasto in gastos:
        try:
            total += limpiar_monto(
                gasto.get("monto", 0)
            )
        except (ValueError, TypeError):
            continue

    return total


def mostrar_gastos():

    while True:

        print("\n===== GASTOS =====")
        print("1. Registrar gasto")
        print("2. Ver gastos")
        print("3. Regresar")

        opcion = input(
            "Selecciona una opción: "
        )

        if opcion == "1":
            registrar_gasto()

        elif opcion == "2":
            mostrar_lista_gastos()

        elif opcion == "3":
            break

        else:
            print("Opción incorrecta.")