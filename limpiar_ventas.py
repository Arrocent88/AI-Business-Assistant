import json
from pathlib import Path

ARCHIVO_VENTAS = Path("ventas.json")

with open(
    ARCHIVO_VENTAS,
    "r",
    encoding="utf-8"
) as archivo:
    ventas = json.load(archivo)

actualizadas = 0

for venta in ventas:
    producto = str(
        venta.get("producto", "")
    ).strip().lower()

    codigo = str(
        venta.get("codigo_producto", "")
    ).strip()

    if (
        producto == "aceite 15w/40"
        and not codigo
    ):
        venta["codigo_producto"] = "ACE-001"
        actualizadas += 1

with open(
    ARCHIVO_VENTAS,
    "w",
    encoding="utf-8"
) as archivo:
    json.dump(
        ventas,
        archivo,
        indent=4,
        ensure_ascii=False
    )

print(
    f"Ventas actualizadas: {actualizadas}"
)

print(
    "Código ACE-001 agregado correctamente."
)