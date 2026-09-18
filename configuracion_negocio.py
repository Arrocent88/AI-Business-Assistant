import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_NEGOCIO = BASE_DIR / "negocio.json"

CAMPOS_PERMITIDOS = ("nombre","telefono","correo","direccion","tax_id","logo","moneda","idioma")
MONEDAS_PERMITIDAS = {"USD":"$","EUR":"€","GBP":"£","NIO":"C$","CAD":"C$","MXN":"$"}
IDIOMAS_PERMITIDOS = ("es","en")

def datos_negocio_por_defecto():
    return {"nombre":"AI Business Assistant","telefono":"","correo":"","direccion":"","tax_id":"","logo":"","moneda":"USD","idioma":"es"}

def _texto(valor):
    return "" if valor is None else str(valor).strip()

def normalizar_datos_negocio(datos=None):
    resultado = datos_negocio_por_defecto()
    if isinstance(datos, dict):
        for campo in CAMPOS_PERMITIDOS:
            if campo in datos:
                resultado[campo] = _texto(datos[campo])
    if not resultado["nombre"]:
        resultado["nombre"] = "AI Business Assistant"
    resultado["moneda"] = resultado["moneda"].upper() or "USD"
    if resultado["moneda"] not in MONEDAS_PERMITIDAS:
        resultado["moneda"] = "USD"
    resultado["idioma"] = resultado["idioma"].lower() or "es"
    if resultado["idioma"] not in IDIOMAS_PERMITIDOS:
        resultado["idioma"] = "es"
    return resultado

def cargar_datos_negocio():
    if not ARCHIVO_NEGOCIO.exists():
        return datos_negocio_por_defecto()
    try:
        with ARCHIVO_NEGOCIO.open("r", encoding="utf-8") as archivo:
            return normalizar_datos_negocio(json.load(archivo))
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return datos_negocio_por_defecto()

def guardar_datos_negocio(datos):
    datos_limpios = normalizar_datos_negocio(datos)
    with ARCHIVO_NEGOCIO.open("w", encoding="utf-8") as archivo:
        json.dump(datos_limpios, archivo, ensure_ascii=False, indent=4)
    return datos_limpios

def actualizar_datos_negocio(**cambios):
    actuales = cargar_datos_negocio()
    for campo, valor in cambios.items():
        if campo in CAMPOS_PERMITIDOS:
            actuales[campo] = valor
    return guardar_datos_negocio(actuales)

def obtener_simbolo_moneda(moneda=None):
    if moneda is None:
        moneda = cargar_datos_negocio().get("moneda", "USD")
    return MONEDAS_PERMITIDAS.get(_texto(moneda).upper() or "USD", "$")

def validar_datos_negocio(datos):
    datos = normalizar_datos_negocio(datos)
    errores = []
    correo = datos["correo"]
    if correo and ("@" not in correo or "." not in correo.split("@")[-1]):
        errores.append("El correo electrónico no parece válido.")
    return errores

def probar_modulo():
    datos = cargar_datos_negocio()
    print("Modulo de configuracion del negocio cargado correctamente.")
    print(f"Archivo de configuracion: {ARCHIVO_NEGOCIO}")
    print(f"Nombre actual: {datos['nombre']}")
    print(f"Moneda: {datos['moneda']}")
    print(f"Idioma: {datos['idioma']}")
    print("Configuracion lista para integrarse.")

if __name__ == "__main__":
    probar_modulo()
