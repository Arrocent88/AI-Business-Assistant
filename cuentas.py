import json


ARCHIVO_CUENTAS = "cuentas_por_cobrar.json"


def cargar_cuentas():
    try:
        with open(
            ARCHIVO_CUENTAS,
            "r",
            encoding="utf-8"
        ) as archivo:
            return json.load(archivo)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        return []


def guardar_cuentas(cuentas):
    with open(
        ARCHIVO_CUENTAS,
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            cuentas,
            archivo,
            indent=4,
            ensure_ascii=False
        )


cuentas_por_cobrar = cargar_cuentas()