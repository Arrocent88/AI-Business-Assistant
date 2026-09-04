from clientes import clientes
from ventas import ventas
from cuentas import cuentas_por_cobrar


def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def calcular_resumen_cliente(nombre_cliente):
    total_comprado = 0
    cantidad_ventas = 0
    ganancia_conocida = 0

    total_credito = 0
    total_pagado = 0
    saldo_pendiente = 0

    for venta in ventas:
        cliente_venta = str(
            venta.get(
                "cliente",
                ""
            )
        ).strip()

        if cliente_venta.lower() != nombre_cliente.lower():
            continue

        cantidad_ventas += 1

        total_comprado += convertir_numero(
            venta.get(
                "monto",
                0
            )
        )

        if "ganancia" in venta:
            ganancia_conocida += convertir_numero(
                venta.get(
                    "ganancia",
                    0
                )
            )

    for cuenta in cuentas_por_cobrar:
        cliente_cuenta = str(
            cuenta.get(
                "cliente",
                ""
            )
        ).strip()

        if cliente_cuenta.lower() != nombre_cliente.lower():
            continue

        total_credito += convertir_numero(
            cuenta.get(
                "total",
                0
            )
        )

        total_pagado += convertir_numero(
            cuenta.get(
                "monto_pagado",
                0
            )
        )

        saldo_pendiente += convertir_numero(
            cuenta.get(
                "saldo_pendiente",
                0
            )
        )

    return {
        "cliente": nombre_cliente,
        "cantidad_ventas": cantidad_ventas,
        "total_comprado": round(
            total_comprado,
            2
        ),
        "ganancia_conocida": round(
            ganancia_conocida,
            2
        ),
        "total_credito": round(
            total_credito,
            2
        ),
        "total_pagado": round(
            total_pagado,
            2
        ),
        "saldo_pendiente": round(
            saldo_pendiente,
            2
        )
    }


def obtener_resumenes_clientes():
    resumenes = []

    for cliente in clientes:
        nombre = str(
            cliente.get(
                "nombre",
                ""
            )
        ).strip()

        if not nombre:
            continue

        resumenes.append(
            calcular_resumen_cliente(
                nombre
            )
        )

    return resumenes