from ventas import ventas
from gastos import gastos
from inventario import inventario, reposiciones
from cuentas import cuentas_por_cobrar


def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def calcular_dashboard():
    ventas_totales = sum(
        convertir_numero(
            venta.get(
                "monto",
                0
            )
        )
        for venta in ventas
    )

    ganancia_conocida = sum(
        convertir_numero(
            venta.get(
                "ganancia",
                0
            )
        )
        for venta in ventas
        if "ganancia" in venta
    )

    gastos_totales = sum(
        convertir_numero(
            gasto.get(
                "monto",
                0
            )
        )
        for gasto in gastos
    )

    total_por_cobrar = sum(
        convertir_numero(
            cuenta.get(
                "saldo_pendiente",
                0
            )
        )
        for cuenta in cuentas_por_cobrar
    )

    capital_inventario = 0
    valor_inventario = 0

    for item in inventario:
        cantidad = int(
            item.get(
                "cantidad",
                0
            )
        )

        costo = convertir_numero(
            item.get(
                "costo",
                0
            )
        )

        precio = convertir_numero(
            item.get(
                "precio",
                0
            )
        )

        capital_inventario += (
            cantidad * costo
        )

        valor_inventario += (
            cantidad * precio
        )

    salidas_reposicion = sum(
        convertir_numero(
            reposicion.get(
                "inversion",
                0
            )
        )
        for reposicion in reposiciones
    )

    flujo_caja = (
        ventas_totales
        - gastos_totales
        - salidas_reposicion
    )

    return {
        "ventas_totales": round(
            ventas_totales,
            2
        ),
        "ganancia_conocida": round(
            ganancia_conocida,
            2
        ),
        "gastos_totales": round(
            gastos_totales,
            2
        ),
        "total_por_cobrar": round(
            total_por_cobrar,
            2
        ),
        "capital_inventario": round(
            capital_inventario,
            2
        ),
        "valor_inventario": round(
            valor_inventario,
            2
        ),
        "flujo_caja": round(
            flujo_caja,
            2
        )
    }