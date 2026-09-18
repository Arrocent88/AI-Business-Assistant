import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# AI BUSINESS ASSISTANT
# Módulo independiente de facturación / recibos
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_NEGOCIO = BASE_DIR / "negocio.json"
CARPETA_FACTURAS = BASE_DIR / "facturas"


# ------------------------------------------------------------
# UTILIDADES
# ------------------------------------------------------------

def _convertir_numero(valor, default=0.0):
    """Convierte números, strings y valores como '$150' a float."""
    if valor is None:
        return default

    if isinstance(valor, (int, float)):
        return float(valor)

    try:
        texto = str(valor).strip()
        texto = texto.replace("$", "").replace(",", "")
        return float(texto)
    except (ValueError, TypeError):
        return default


def _dinero(valor):
    """Devuelve un valor con formato monetario."""
    return f"${_convertir_numero(valor):,.2f}"


def _texto_seguro(valor, default=""):
    if valor is None:
        return default
    texto = str(valor).strip()
    return texto if texto else default


def _limpiar_nombre_archivo(texto):
    texto = _texto_seguro(texto, "documento")
    texto = re.sub(r'[<>:"/\\|?*]', "-", texto)
    texto = re.sub(r"\s+", "_", texto)
    return texto


# ------------------------------------------------------------
# DATOS DEL NEGOCIO
# ------------------------------------------------------------

def datos_negocio_por_defecto():
    return {
        "nombre": "AI Business Assistant",
        "propietario": "",
        "telefono": "",
        "correo": "",
        "direccion": "",
        "ciudad": "",
        "estado": "",
        "zip": "",
        "moneda": "USD",
        "mensaje_recibo": "Gracias por su compra."
    }


def cargar_datos_negocio():
    """
    Carga negocio.json.
    Si todavía no existe, devuelve valores predeterminados
    SIN provocar un error.
    """
    datos = datos_negocio_por_defecto()

    if not ARCHIVO_NEGOCIO.exists():
        return datos

    try:
        with open(ARCHIVO_NEGOCIO, "r", encoding="utf-8") as archivo:
            guardados = json.load(archivo)

        if isinstance(guardados, dict):
            datos.update(guardados)

    except (json.JSONDecodeError, OSError):
        pass

    return datos


def guardar_datos_negocio(datos):
    """
    Guarda la información del negocio en negocio.json.
    """
    if not isinstance(datos, dict):
        raise ValueError("Los datos del negocio deben ser un diccionario.")

    actuales = datos_negocio_por_defecto()
    actuales.update(datos)

    with open(ARCHIVO_NEGOCIO, "w", encoding="utf-8") as archivo:
        json.dump(actuales, archivo, ensure_ascii=False, indent=4)

    return actuales


# ------------------------------------------------------------
# CLIENTES
# ------------------------------------------------------------

def buscar_cliente(venta, clientes):
    """
    Busca los datos del cliente de una venta.

    Compatible con clientes como:
    {
        "nombre": "Pedro Hernandez",
        "telefono": "2068892140",
        "correo": "..."
    }

    También funciona si teléfono o correo no existen.
    """
    if not isinstance(venta, dict):
        return {}

    nombre_venta = _texto_seguro(venta.get("cliente")).lower()

    if not nombre_venta:
        return {}

    if not isinstance(clientes, list):
        return {}

    for cliente in clientes:
        if not isinstance(cliente, dict):
            continue

        nombre = _texto_seguro(cliente.get("nombre")).lower()

        if nombre == nombre_venta:
            return cliente.copy()

    return {}


# ------------------------------------------------------------
# NÚMERO DE DOCUMENTO
# ------------------------------------------------------------

def generar_numero_documento(indice=None, fecha=None):
    """
    Genera un número legible de recibo.

    Ejemplo:
    REC-20260918-001
    """
    if fecha:
        try:
            fecha_obj = datetime.strptime(str(fecha), "%Y-%m-%d")
        except ValueError:
            fecha_obj = datetime.now()
    else:
        fecha_obj = datetime.now()

    if indice is None:
        numero = 1
    else:
        try:
            numero = int(indice) + 1
        except (ValueError, TypeError):
            numero = 1

    return f"REC-{fecha_obj.strftime('%Y%m%d')}-{numero:03d}"


def obtener_numero_documento(venta, indice=None):
    """
    Usa un número existente si la venta ya lo posee.
    Si no, genera uno sin modificar ventas.json.
    """
    if isinstance(venta, dict):
        existente = (
            venta.get("numero_documento")
            or venta.get("numero_recibo")
            or venta.get("recibo")
        )

        if existente:
            return str(existente)

        fecha = venta.get("fecha")
    else:
        fecha = None

    return generar_numero_documento(indice, fecha)


# ------------------------------------------------------------
# DATOS DE LA VENTA
# ------------------------------------------------------------

def preparar_venta(venta):
    """
    Normaliza ventas nuevas y ventas históricas incompletas.
    NO modifica el diccionario original.
    """
    if not isinstance(venta, dict):
        raise ValueError("La venta debe ser un diccionario.")

    cliente = _texto_seguro(venta.get("cliente"), "Cliente")
    producto = _texto_seguro(venta.get("producto"), "Producto o servicio")
    codigo = _texto_seguro(venta.get("codigo_producto"), "N/A")

    cantidad = _convertir_numero(venta.get("cantidad"), 1.0)

    if cantidad <= 0:
        cantidad = 1.0

    monto = _convertir_numero(venta.get("monto"), 0.0)

    precio_unitario_original = venta.get("precio_unitario")

    if precio_unitario_original is not None:
        precio_unitario = _convertir_numero(precio_unitario_original)
    elif cantidad:
        precio_unitario = monto / cantidad
    else:
        precio_unitario = monto

    if monto == 0 and precio_unitario:
        monto = precio_unitario * cantidad

    fecha = _texto_seguro(venta.get("fecha"))

    if not fecha:
        fecha = "Sin fecha"

    return {
        "cliente": cliente,
        "producto": producto,
        "codigo_producto": codigo,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "monto": monto,
        "fecha": fecha,
    }


# ------------------------------------------------------------
# GENERACIÓN DEL PDF
# ------------------------------------------------------------

def generar_recibo_pdf(
    venta,
    clientes=None,
    indice=None,
    idioma="es",
    datos_negocio=None
):
    """
    Genera un recibo profesional PDF.

    Parámetros:
        venta: diccionario con la venta.
        clientes: lista de clientes.
        indice: posición de la venta en ventas.json.
        idioma: "es" o "en".
        datos_negocio: opcional. Si no se envía, carga negocio.json.

    Retorna:
        Ruta completa del PDF generado.
    """

    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            HRFlowable,
        )
    except ImportError as error:
        raise ImportError(
            "ReportLab no está instalado. "
            "Instálalo con: pip install reportlab"
        ) from error

    venta_limpia = preparar_venta(venta)

    if clientes is None:
        clientes = []

    cliente = buscar_cliente(venta, clientes)

    if datos_negocio is None:
        datos_negocio = cargar_datos_negocio()

    numero = obtener_numero_documento(venta, indice)

    idioma = str(idioma).lower()

    if idioma not in ("es", "en"):
        idioma = "es"

    textos = {
        "es": {
            "titulo": "RECIBO",
            "recibo": "Recibo",
            "fecha": "Fecha",
            "cliente": "Cliente",
            "telefono": "Teléfono",
            "correo": "Correo",
            "codigo": "Código",
            "descripcion": "Descripción",
            "cantidad": "Cantidad",
            "precio": "Precio unitario",
            "total": "Total",
            "gracias": "Gracias por su compra.",
            "sin_fecha": "Sin fecha",
        },
        "en": {
            "titulo": "RECEIPT",
            "recibo": "Receipt",
            "fecha": "Date",
            "cliente": "Customer",
            "telefono": "Phone",
            "correo": "Email",
            "codigo": "Code",
            "descripcion": "Description",
            "cantidad": "Qty",
            "precio": "Unit price",
            "total": "Total",
            "gracias": "Thank you for your business.",
            "sin_fecha": "No date",
        },
    }

    t = textos[idioma]

    fecha = venta_limpia["fecha"]

    if fecha == "Sin fecha" and idioma == "en":
        fecha = t["sin_fecha"]

    CARPETA_FACTURAS.mkdir(parents=True, exist_ok=True)

    nombre_archivo = (
        f"{_limpiar_nombre_archivo(numero)}_"
        f"{_limpiar_nombre_archivo(venta_limpia['cliente'])}.pdf"
    )

    ruta_pdf = CARPETA_FACTURAS / nombre_archivo

    documento = SimpleDocTemplate(
        str(ruta_pdf),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    estilos = getSampleStyleSheet()

    estilo_empresa = ParagraphStyle(
        "Empresa",
        parent=estilos["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        spaceAfter=4,
    )

    estilo_titulo = ParagraphStyle(
        "TituloDocumento",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=18,
        alignment=TA_RIGHT,
        spaceAfter=3,
    )

    estilo_normal = ParagraphStyle(
        "NormalFactura",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
    )

    estilo_centro = ParagraphStyle(
        "CentroFactura",
        parent=estilo_normal,
        alignment=TA_CENTER,
    )

    elementos = []

    nombre_empresa = _texto_seguro(
        datos_negocio.get("nombre"),
        "AI Business Assistant"
    )

    direccion = _texto_seguro(datos_negocio.get("direccion"))
    ciudad = _texto_seguro(datos_negocio.get("ciudad"))
    estado = _texto_seguro(datos_negocio.get("estado"))
    zip_code = _texto_seguro(datos_negocio.get("zip"))
    telefono_empresa = _texto_seguro(datos_negocio.get("telefono"))
    correo_empresa = _texto_seguro(datos_negocio.get("correo"))

    ubicacion = ", ".join(
        parte for parte in [ciudad, estado] if parte
    )

    if zip_code:
        ubicacion = f"{ubicacion} {zip_code}".strip()

    datos_empresa_lineas = []

    if direccion:
        datos_empresa_lineas.append(direccion)

    if ubicacion:
        datos_empresa_lineas.append(ubicacion)

    if telefono_empresa:
        datos_empresa_lineas.append(telefono_empresa)

    if correo_empresa:
        datos_empresa_lineas.append(correo_empresa)

    empresa_info = "<br/>".join(datos_empresa_lineas)

    encabezado = Table(
        [
            [
                Paragraph(nombre_empresa, estilo_empresa),
                Paragraph(t["titulo"], estilo_titulo),
            ],
            [
                Paragraph(empresa_info, estilo_normal),
                Paragraph(
                    f"<b>{t['recibo']}:</b> {numero}<br/>"
                    f"<b>{t['fecha']}:</b> {fecha}",
                    estilo_normal,
                ),
            ],
        ],
        colWidths=[4.35 * inch, 2.35 * inch],
    )

    encabezado.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    elementos.append(encabezado)
    elementos.append(Spacer(1, 10))

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#1F3A5F"),
        )
    )

    elementos.append(Spacer(1, 15))

    nombre_cliente = venta_limpia["cliente"]
    telefono_cliente = _texto_seguro(cliente.get("telefono"), "N/A")
    correo_cliente = _texto_seguro(cliente.get("correo"), "N/A")

    bloque_cliente = Table(
        [
            [
                Paragraph(
                    f"<b>{t['cliente']}</b><br/>"
                    f"{nombre_cliente}<br/>"
                    f"{t['telefono']}: {telefono_cliente}<br/>"
                    f"{t['correo']}: {correo_cliente}",
                    estilo_normal,
                )
            ]
        ],
        colWidths=[6.7 * inch],
    )

    bloque_cliente.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F5F8")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D0D9")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )

    elementos.append(bloque_cliente)
    elementos.append(Spacer(1, 18))

    cantidad = venta_limpia["cantidad"]

    if float(cantidad).is_integer():
        cantidad_mostrar = str(int(cantidad))
    else:
        cantidad_mostrar = f"{cantidad:g}"

    tabla_productos = Table(
        [
            [
                t["codigo"],
                t["descripcion"],
                t["cantidad"],
                t["precio"],
                t["total"],
            ],
            [
                venta_limpia["codigo_producto"],
                venta_limpia["producto"],
                cantidad_mostrar,
                _dinero(venta_limpia["precio_unitario"]),
                _dinero(venta_limpia["monto"]),
            ],
        ],
        colWidths=[
            0.9 * inch,
            2.6 * inch,
            0.65 * inch,
            1.25 * inch,
            1.3 * inch,
        ],
    )

    tabla_productos.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F3A5F"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCD3DB")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabla_productos)
    elementos.append(Spacer(1, 18))

    tabla_total = Table(
        [
            [
                "",
                Paragraph(
                    f"<b>{t['total']}: {_dinero(venta_limpia['monto'])}</b>",
                    ParagraphStyle(
                        "TotalFactura",
                        parent=estilo_normal,
                        fontName="Helvetica-Bold",
                        fontSize=13,
                        alignment=TA_RIGHT,
                    ),
                ),
            ]
        ],
        colWidths=[4.7 * inch, 2.0 * inch],
    )

    tabla_total.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("TOPPADDING", (1, 0), (1, 0), 8),
                ("BOTTOMPADDING", (1, 0), (1, 0), 8),
                (
                    "LINEABOVE",
                    (1, 0),
                    (1, 0),
                    1,
                    colors.HexColor("#1F3A5F"),
                ),
            ]
        )
    )

    elementos.append(tabla_total)
    elementos.append(Spacer(1, 28))

    mensaje = _texto_seguro(datos_negocio.get("mensaje_recibo"))

    if not mensaje:
        mensaje = t["gracias"]

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor("#C8D0D9"),
        )
    )

    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(mensaje, estilo_centro))

    documento.build(elementos)

    return str(ruta_pdf)


# ------------------------------------------------------------
# ABRIR PDF
# ------------------------------------------------------------

def abrir_archivo(ruta):
    """
    Abre el PDF con el programa predeterminado del sistema.
    """
    ruta = os.path.abspath(str(ruta))

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    if sys.platform.startswith("win"):
        os.startfile(ruta)

    elif sys.platform == "darwin":
        import subprocess
        subprocess.Popen(["open", ruta])

    else:
        import subprocess
        subprocess.Popen(["xdg-open", ruta])

    return ruta


# ------------------------------------------------------------
# PRUEBA DEL MÓDULO
# ------------------------------------------------------------

def probar_modulo():
    """
    Prueba básica SIN modificar app.py, ventas.json ni clientes.json.
    No genera PDF automáticamente.
    """
    print("==========================================")
    print(" AI BUSINESS ASSISTANT - FACTURACION")
    print("==========================================")
    print("Modulo cargado correctamente.")
    print(f"Carpeta del proyecto: {BASE_DIR}")
    print(f"Carpeta de facturas: {CARPETA_FACTURAS}")
    print()
    print("Facturacion lista para integrarse.")


if __name__ == "__main__":
    probar_modulo()