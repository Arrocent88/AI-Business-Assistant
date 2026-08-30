def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def calcular_diagnostico(
    ventas,
    inventario,
    reposiciones,
    gastos
):
    entradas_ventas = sum(
        convertir_numero(
            venta.get("monto", 0)
        )
        for venta in ventas
    )

    salidas_reposicion = sum(
        convertir_numero(
            reposicion.get("inversion", 0)
        )
        for reposicion in reposiciones
    )

    gastos_totales = sum(
        convertir_numero(
            gasto.get("monto", 0)
        )
        for gasto in gastos
    )

    flujo_neto = (
        entradas_ventas
        - salidas_reposicion
        - gastos_totales
    )

    capital_inventario = 0
    valor_inventario = 0
    productos_stock_bajo = 0

    for item in inventario:
        cantidad = int(
            item.get("cantidad", 0)
        )

        precio = convertir_numero(
            item.get("precio", 0)
        )

        costo = convertir_numero(
            item.get("costo", 0)
        )

        capital_inventario += (
            cantidad * costo
        )

        valor_inventario += (
            cantidad * precio
        )

        if cantidad <= 5:
            productos_stock_bajo += 1

    ganancia_potencial = (
        valor_inventario
        - capital_inventario
    )

    ventas_sin_costo = sum(
        1
        for venta in ventas
        if "costo_total" not in venta
    )

    if entradas_ventas > 0:
        porcentaje_gastos = (
            gastos_totales
            / entradas_ventas
        ) * 100
    else:
        porcentaje_gastos = 0

    if flujo_neto > 0:
        estado_flujo = "POSITIVO"
    elif flujo_neto < 0:
        estado_flujo = "NEGATIVO"
    else:
        estado_flujo = "EQUILIBRADO"

    diagnosticos = []

    if flujo_neto > 0:
        diagnosticos.append(
            "✓ El flujo de caja registrado es positivo."
        )
    elif flujo_neto < 0:
        diagnosticos.append(
            "⚠ El flujo de caja registrado es negativo."
        )
    else:
        diagnosticos.append(
            "⚠ El flujo de caja está equilibrado."
        )

    if ganancia_potencial > 0:
        diagnosticos.append(
            "✓ El inventario tiene ganancia potencial."
        )
    else:
        diagnosticos.append(
            "⚠ Revisar la rentabilidad del inventario."
        )

    if productos_stock_bajo == 0:
        diagnosticos.append(
            "✓ El inventario está en un nivel adecuado."
        )
    else:
        diagnosticos.append(
            f"⚠ Hay {productos_stock_bajo} "
            "producto(s) con stock bajo."
        )

    if flujo_neto < 0:
        recomendacion = (
            "Prioridad: reducir gastos o aumentar "
            "las ventas para recuperar flujo de caja."
        )

    elif productos_stock_bajo > 0:
        recomendacion = (
            "El negocio mantiene flujo positivo, "
            "pero debe reponer los productos con "
            "stock bajo."
        )

    else:
        recomendacion = (
            "El negocio mantiene flujo positivo y "
            "el inventario tiene potencial de ganancia. "
            "Continúa controlando gastos, ventas "
            "y reposiciones."
        )

    return {
        "flujo_neto": flujo_neto,
        "estado_flujo": estado_flujo,
        "ganancia_potencial": ganancia_potencial,
        "porcentaje_gastos": porcentaje_gastos,
        "ventas_sin_costo": ventas_sin_costo,
        "diagnosticos": diagnosticos,
        "recomendacion": recomendacion
    }