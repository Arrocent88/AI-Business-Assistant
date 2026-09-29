import shutil
from datetime import datetime
from pathlib import Path


# ==================================================
# CONFIGURACIÓN
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
CARPETA_RESPALDOS = BASE_DIR / "backups"

ARCHIVOS_RESPALDO = [
    "clientes.json",
    "ventas.json",
    "inventario.json",
    "gastos.json",
    "cuentas_por_cobrar.json",
    "reposiciones.json",
    "negocio.json",
]


# ==================================================
# CREAR RESPALDO
# ==================================================

def crear_respaldo():
    CARPETA_RESPALDOS.mkdir(
        parents=True,
        exist_ok=True
    )

    fecha_hora = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    carpeta_destino = (
        CARPETA_RESPALDOS
        / f"backup_{fecha_hora}"
    )

    carpeta_destino.mkdir(
        parents=True,
        exist_ok=False
    )

    archivos_copiados = []
    archivos_no_encontrados = []

    for nombre_archivo in ARCHIVOS_RESPALDO:
        origen = BASE_DIR / nombre_archivo

        if origen.exists():
            destino = (
                carpeta_destino
                / nombre_archivo
            )

            shutil.copy2(
                origen,
                destino
            )

            archivos_copiados.append(
                nombre_archivo
            )
        else:
            archivos_no_encontrados.append(
                nombre_archivo
            )

    return {
        "exito": True,
        "carpeta": str(carpeta_destino),
        "archivos_copiados": archivos_copiados,
        "archivos_no_encontrados":
            archivos_no_encontrados,
    }


# ==================================================
# LISTAR RESPALDOS
# ==================================================

def listar_respaldos():
    if not CARPETA_RESPALDOS.exists():
        return []

    respaldos = []

    for carpeta in CARPETA_RESPALDOS.iterdir():
        if (
            carpeta.is_dir()
            and carpeta.name.startswith("backup_")
        ):
            respaldos.append(carpeta)

    respaldos.sort(
        key=lambda ruta: ruta.name,
        reverse=True
    )

    return respaldos


# ==================================================
# RESTAURAR RESPALDO
# ==================================================

def restaurar_respaldo(carpeta_respaldo):
    carpeta_respaldo = Path(
        carpeta_respaldo
    )

    if not carpeta_respaldo.exists():
        raise FileNotFoundError(
            "El respaldo seleccionado no existe."
        )

    if not carpeta_respaldo.is_dir():
        raise ValueError(
            "El respaldo seleccionado no es válido."
        )

    archivos_restaurados = []
    archivos_no_encontrados = []

    for nombre_archivo in ARCHIVOS_RESPALDO:
        origen = (
            carpeta_respaldo
            / nombre_archivo
        )

        if origen.exists():
            destino = (
                BASE_DIR
                / nombre_archivo
            )

            shutil.copy2(
                origen,
                destino
            )

            archivos_restaurados.append(
                nombre_archivo
            )
        else:
            archivos_no_encontrados.append(
                nombre_archivo
            )

    return {
        "exito": True,
        "archivos_restaurados":
            archivos_restaurados,
        "archivos_no_encontrados":
            archivos_no_encontrados,
    }


# ==================================================
# PRUEBA SEGURA
# ==================================================

def probar_modulo():
    print(
        "Módulo de respaldo cargado correctamente."
    )

    respaldos = listar_respaldos()

    print()
    print(
        f"Respaldos encontrados: {len(respaldos)}"
    )

    for respaldo in respaldos:
        print(
            f"  - {respaldo.name}"
        )

    print()
    print(
        "Crear y restaurar respaldo: LISTO"
    )


if __name__ == "__main__":
    probar_modulo()