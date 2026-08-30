import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

from clientes import clientes
from inventario import inventario, reposiciones
from ventas import ventas
from gastos import gastos
from diagnostico import calcular_diagnostico


# ==================================================
# FUNCIONES GENERALES
# ==================================================

def convertir_numero(valor):
    return float(
        str(valor)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )


def guardar_json(archivo, datos):
    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            datos,
            f,
            indent=4,
            ensure_ascii=False
        )


def crear_area_scroll(ventana_padre):
    marco = tk.Frame(ventana_padre)

    marco.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=5
    )

    canvas = tk.Canvas(marco)

    scrollbar = tk.Scrollbar(
        marco,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(canvas)

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    return contenido


# ==================================================
# CLIENTES
# ==================================================

def registrar_cliente(entrada, v):
    nombre = entrada.get().strip()

    if not nombre:
        messagebox.showwarning(
            "Dato requerido",
            "Escribe el nombre del cliente."
        )
        return

    clientes.append({
        "nombre": nombre
    })

    guardar_json(
        "clientes.json",
        clientes
    )

    messagebox.showinfo(
        "Cliente registrado",
        f"{nombre} fue registrado correctamente."
    )

    v.destroy()


def abrir_registro_cliente():
    v = tk.Toplevel(ventana)

    v.title("Registrar cliente")
    v.geometry("450x260")
    v.resizable(False, False)

    tk.Label(
        v,
        text="REGISTRAR CLIENTE",
        font=("Arial", 17, "bold")
    ).pack(pady=(25, 20))

    tk.Label(
        v,
        text="Nombre del cliente:"
    ).pack()

    entrada = tk.Entry(
        v,
        width=35,
        font=("Arial", 11)
    )

    entrada.pack(pady=10)
    entrada.focus()

    tk.Button(
        v,
        text="Guardar cliente",
        width=18,
        command=lambda:
        registrar_cliente(
            entrada,
            v
        )
    ).pack(pady=15)


def abrir_clientes():
    v = tk.Toplevel(ventana)

    v.title("Clientes")
    v.geometry("600x500")
    v.resizable(False, False)

    tk.Label(
        v,
        text="CLIENTES REGISTRADOS",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(
        v,
        text="+ Registrar cliente",
        width=20,
        command=abrir_registro_cliente
    ).pack(pady=(0, 15))

    for numero, cliente in enumerate(
        clientes,
        start=1
    ):
        tk.Label(
            v,
            text=(
                f"{numero}. "
                f"{cliente.get('nombre', 'Sin nombre')}"
            ),
            font=("Arial", 12),
            width=40,
            anchor="w"
        ).pack(pady=5)

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(
        side="bottom",
        pady=25
    )


# ==================================================
# REGISTRAR PRODUCTO
# ==================================================

def registrar_producto(
    entrada_codigo,
    entrada_nombre,
    entrada_cantidad,
    entrada_costo,
    entrada_precio,
    v
):
    codigo = (
        entrada_codigo.get()
        .strip()
        .upper()
    )

    nombre = (
        entrada_nombre.get()
        .strip()
    )

    if not codigo or not nombre:
        messagebox.showwarning(
            "Dato requerido",
            "Código y nombre son obligatorios."
        )
        return

    for item in inventario:
        if (
            str(
                item.get("codigo", "")
            ).strip().upper()
            == codigo
        ):
            messagebox.showwarning(
                "Código duplicado",
                f"Ya existe el código {codigo}."
            )
            return

    try:
        cantidad = int(
            entrada_cantidad.get()
        )

        costo = convertir_numero(
            entrada_costo.get()
        )

        precio = convertir_numero(
            entrada_precio.get()
        )

        if (
            cantidad < 0
            or costo < 0
            or precio <= 0
        ):
            raise ValueError

    except ValueError:
        messagebox.showwarning(
            "Datos incorrectos",
            "Revisa cantidad, costo y precio."
        )
        return

    inventario.append({
        "codigo": codigo,
        "producto": nombre,
        "cantidad": cantidad,
        "costo": costo,
        "precio": precio
    })

    guardar_json(
        "inventario.json",
        inventario
    )

    messagebox.showinfo(
        "Producto registrado",
        (
            "Producto registrado correctamente.\n\n"
            f"Código: {codigo}\n"
            f"Producto: {nombre}\n"
            f"Cantidad: {cantidad}\n"
            f"Costo: ${costo:.2f}\n"
            f"Precio: ${precio:.2f}"
        )
    )

    v.destroy()


def abrir_registro_producto():
    v = tk.Toplevel(ventana)

    v.title("Registrar producto")
    v.geometry("520x600")
    v.resizable(False, False)

    tk.Label(
        v,
        text="REGISTRAR PRODUCTO",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(25, 20)
    )

    campos = {}

    etiquetas = [
        ("codigo", "Código del producto:"),
        ("nombre", "Nombre del producto:"),
        ("cantidad", "Cantidad inicial:"),
        ("costo", "Costo unitario:"),
        ("precio", "Precio de venta:")
    ]

    for clave, texto in etiquetas:
        tk.Label(
            v,
            text=texto
        ).pack()

        entrada = tk.Entry(
            v,
            width=32,
            font=("Arial", 11)
        )

        entrada.pack(
            pady=(5, 15)
        )

        campos[clave] = entrada

    campos["codigo"].focus()

    tk.Button(
        v,
        text="Guardar producto",
        width=20,
        command=lambda:
        registrar_producto(
            campos["codigo"],
            campos["nombre"],
            campos["cantidad"],
            campos["costo"],
            campos["precio"],
            v
        )
    ).pack(pady=10)


# ==================================================
# EDITAR PRODUCTO
# ==================================================

def guardar_edicion_producto(
    indice,
    entrada_codigo,
    entrada_nombre,
    entrada_costo,
    entrada_precio,
    v
):
    codigo = (
        entrada_codigo.get()
        .strip()
        .upper()
    )

    nombre = (
        entrada_nombre.get()
        .strip()
    )

    if not codigo or not nombre:
        messagebox.showwarning(
            "Datos requeridos",
            "Código y nombre son obligatorios."
        )
        return

    try:
        costo = convertir_numero(
            entrada_costo.get()
        )

        precio = convertir_numero(
            entrada_precio.get()
        )

        if costo < 0 or precio <= 0:
            raise ValueError

    except ValueError:
        messagebox.showwarning(
            "Datos incorrectos",
            "Revisa costo y precio."
        )
        return

    for otro_indice, item in enumerate(
        inventario
    ):
        if otro_indice == indice:
            continue

        if (
            str(
                item.get("codigo", "")
            ).strip().upper()
            == codigo
        ):
            messagebox.showwarning(
                "Código duplicado",
                f"Ya existe el código {codigo}."
            )
            return

    producto = inventario[indice]

    producto["codigo"] = codigo
    producto["producto"] = nombre
    producto["costo"] = costo
    producto["precio"] = precio

    guardar_json(
        "inventario.json",
        inventario
    )

    messagebox.showinfo(
        "Producto actualizado",
        (
            "Producto actualizado correctamente.\n\n"
            f"Código: {codigo}\n"
            f"Producto: {nombre}\n"
            f"Costo: ${costo:.2f}\n"
            f"Precio: ${precio:.2f}"
        )
    )

    v.destroy()


def abrir_editor_producto(indice):
    producto = inventario[indice]

    v = tk.Toplevel(ventana)

    v.title("Editar producto")
    v.geometry("520x500")
    v.resizable(False, False)

    tk.Label(
        v,
        text="EDITAR PRODUCTO",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(25, 20)
    )

    tk.Label(v, text="Código:").pack()

    codigo = tk.Entry(
        v,
        width=32
    )

    codigo.pack(
        pady=(5, 15)
    )

    codigo.insert(
        0,
        producto.get("codigo", "")
    )

    tk.Label(
        v,
        text="Nombre del producto:"
    ).pack()

    nombre = tk.Entry(
        v,
        width=32
    )

    nombre.pack(
        pady=(5, 15)
    )

    nombre.insert(
        0,
        producto.get("producto", "")
    )

    tk.Label(
        v,
        text="Costo unitario:"
    ).pack()

    costo = tk.Entry(
        v,
        width=18
    )

    costo.pack(
        pady=(5, 15)
    )

    costo.insert(
        0,
        producto.get("costo", 0)
    )

    tk.Label(
        v,
        text="Precio de venta:"
    ).pack()

    precio = tk.Entry(
        v,
        width=18
    )

    precio.pack(
        pady=(5, 15)
    )

    precio.insert(
        0,
        producto.get("precio", 0)
    )

    tk.Label(
        v,
        text=(
            "Stock actual: "
            f"{producto.get('cantidad', 0)}"
        )
    ).pack(
        pady=(5, 20)
    )

    tk.Button(
        v,
        text="Guardar cambios",
        width=20,
        command=lambda:
        guardar_edicion_producto(
            indice,
            codigo,
            nombre,
            costo,
            precio,
            v
        )
    ).pack()


def abrir_seleccion_editar_producto():
    if not inventario:
        messagebox.showwarning(
            "Sin productos",
            "No hay productos para editar."
        )
        return

    v = tk.Toplevel(ventana)

    v.title("Seleccionar producto")
    v.geometry("550x300")
    v.resizable(False, False)

    tk.Label(
        v,
        text="EDITAR PRODUCTO",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(25, 20)
    )

    opciones = [
        (
            f"{item.get('codigo', 'SIN CÓDIGO')} - "
            f"{item.get('producto', '')}"
        )
        for item in inventario
    ]

    combo = ttk.Combobox(
        v,
        values=opciones,
        state="readonly",
        width=45
    )

    combo.pack(
        pady=(10, 25)
    )

    def continuar():
        indice = combo.current()

        if indice < 0:
            messagebox.showwarning(
                "Producto requerido",
                "Selecciona un producto."
            )
            return

        v.destroy()
        abrir_editor_producto(indice)

    tk.Button(
        v,
        text="Editar producto",
        width=20,
        command=continuar
    ).pack()


# ==================================================
# REPOSICIÓN
# ==================================================

def registrar_reposicion(
    combo,
    entrada_cantidad,
    entrada_costo,
    v
):
    indice = combo.current()

    if indice < 0:
        messagebox.showwarning(
            "Producto requerido",
            "Selecciona un producto."
        )
        return

    try:
        cantidad = int(
            entrada_cantidad.get()
        )

        costo_compra = convertir_numero(
            entrada_costo.get()
        )

        if (
            cantidad <= 0
            or costo_compra <= 0
        ):
            raise ValueError

    except ValueError:
        messagebox.showwarning(
            "Datos incorrectos",
            "Revisa cantidad y costo."
        )
        return

    producto = inventario[indice]

    stock_anterior = int(
        producto.get("cantidad", 0)
    )

    costo_anterior = convertir_numero(
        producto.get("costo", 0)
    )

    nuevo_stock = (
        stock_anterior + cantidad
    )

    costo_promedio = (
        (
            stock_anterior
            * costo_anterior
        )
        +
        (
            cantidad
            * costo_compra
        )
    ) / nuevo_stock

    producto["cantidad"] = nuevo_stock
    producto["costo"] = round(
        costo_promedio,
        2
    )

    inversion = (
        cantidad * costo_compra
    )

    reposiciones.append({
        "codigo": producto.get(
            "codigo",
            ""
        ),
        "producto": producto.get(
            "producto",
            ""
        ),
        "cantidad": cantidad,
        "costo_unitario": costo_compra,
        "inversion": inversion,
        "fecha": datetime.now().strftime(
            "%Y-%m-%d"
        )
    })

    guardar_json(
        "inventario.json",
        inventario
    )

    guardar_json(
        "reposiciones.json",
        reposiciones
    )

    messagebox.showinfo(
        "Reposición registrada",
        (
            "Reposición registrada correctamente.\n\n"
            f"Producto: "
            f"{producto.get('producto', '')}\n"
            f"Unidades: {cantidad}\n"
            f"Inversión: ${inversion:.2f}\n"
            f"Stock nuevo: {nuevo_stock}\n"
            f"Costo promedio: "
            f"${costo_promedio:.2f}"
        )
    )

    v.destroy()


def abrir_reposicion():
    if not inventario:
        messagebox.showwarning(
            "Sin productos",
            "No hay productos registrados."
        )
        return

    v = tk.Toplevel(ventana)

    v.title("Reposición de inventario")
    v.geometry("550x450")
    v.resizable(False, False)

    tk.Label(
        v,
        text="REPOSICIÓN DE INVENTARIO",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(25, 20)
    )

    opciones = [
        (
            f"{item.get('codigo', 'SIN CÓDIGO')} - "
            f"{item.get('producto', '')}"
        )
        for item in inventario
    ]

    tk.Label(v, text="Producto:").pack()

    combo = ttk.Combobox(
        v,
        values=opciones,
        state="readonly",
        width=45
    )

    combo.pack(
        pady=(5, 20)
    )

    tk.Label(
        v,
        text="Cantidad comprada:"
    ).pack()

    cantidad = tk.Entry(
        v,
        width=18
    )

    cantidad.pack(
        pady=(5, 20)
    )

    tk.Label(
        v,
        text="Costo unitario del proveedor:"
    ).pack()

    costo = tk.Entry(
        v,
        width=18
    )

    costo.pack(
        pady=(5, 25)
    )

    tk.Button(
        v,
        text="Registrar reposición",
        width=20,
        command=lambda:
        registrar_reposicion(
            combo,
            cantidad,
            costo,
            v
        )
    ).pack()


# ==================================================
# HISTORIAL DE REPOSICIONES
# ==================================================

def abrir_historial_reposiciones():
    v = tk.Toplevel(ventana)

    v.title("Historial de reposiciones")
    v.geometry("850x650")
    v.resizable(False, False)

    tk.Label(
        v,
        text="HISTORIAL DE REPOSICIONES",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(20, 10)
    )

    contenido = crear_area_scroll(v)

    total = 0

    for numero, reposicion in enumerate(
        reposiciones,
        start=1
    ):
        cantidad = int(
            reposicion.get(
                "cantidad",
                0
            )
        )

        costo = convertir_numero(
            reposicion.get(
                "costo_unitario",
                reposicion.get("costo", 0)
            )
        )

        inversion = convertir_numero(
            reposicion.get(
                "inversion",
                cantidad * costo
            )
        )

        total += inversion

        caja = tk.LabelFrame(
            contenido,
            text=f"Reposición {numero}",
            padx=20,
            pady=10,
            width=740
        )

        caja.pack(
            fill="x",
            padx=5,
            pady=7
        )

        tk.Label(
            caja,
            text=(
                "Código: "
                f"{reposicion.get('codigo', 'SIN CÓDIGO') or 'SIN CÓDIGO'}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                "Producto: "
                f"{reposicion.get('producto', '')}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                "Fecha: "
                f"{reposicion.get('fecha', 'Sin fecha')}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                f"Unidades compradas: "
                f"{cantidad}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                f"Costo proveedor: "
                f"${costo:.2f}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                f"Inversión: "
                f"${inversion:.2f}"
            ),
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

    tk.Label(
        v,
        text=(
            f"Inversión total en reposiciones: "
            f"${total:.2f}"
        ),
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(pady=15)


# ==================================================
# LISTA DE COMPRA AL PROVEEDOR
# ==================================================

def abrir_lista_compra():
    v = tk.Toplevel(ventana)

    v.title("Lista de compra al proveedor")
    v.geometry("850x650")
    v.resizable(False, False)

    tk.Label(
        v,
        text="LISTA DE COMPRA SUGERIDA",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(20, 5)
    )

    tk.Label(
        v,
        text=(
            "Productos con 10 unidades "
            "o menos"
        ),
        font=("Arial", 11)
    ).pack(
        pady=(0, 15)
    )

    stock_minimo = 10
    stock_objetivo = 20

    productos_comprar = []

    for item in inventario:
        stock = int(
            item.get("cantidad", 0)
        )

        if stock <= stock_minimo:
            cantidad_comprar = (
                stock_objetivo - stock
            )

            if cantidad_comprar > 0:
                productos_comprar.append(
                    {
                        "codigo": item.get(
                            "codigo",
                            ""
                        ),
                        "producto": item.get(
                            "producto",
                            ""
                        ),
                        "stock": stock,
                        "cantidad_comprar":
                            cantidad_comprar,
                        "costo":
                            convertir_numero(
                                item.get(
                                    "costo",
                                    0
                                )
                            )
                    }
                )

    contenido = crear_area_scroll(v)

    inversion_total = 0
    texto_copiar = (
        "LISTA DE COMPRA AL PROVEEDOR\n"
        "--------------------------------\n"
    )

    if not productos_comprar:
        tk.Label(
            contenido,
            text=(
                "No hay productos que "
                "necesiten reposición."
            ),
            font=("Arial", 12)
        ).pack(pady=40)

    else:
        for numero, item in enumerate(
            productos_comprar,
            start=1
        ):
            codigo = (
                item["codigo"]
                if item["codigo"]
                else "SIN CÓDIGO"
            )

            inversion = (
                item["cantidad_comprar"]
                * item["costo"]
            )

            inversion_total += inversion

            caja = tk.LabelFrame(
                contenido,
                text=f"Producto {numero}",
                font=("Arial", 11, "bold"),
                padx=20,
                pady=10,
                width=740
            )

            caja.pack(
                fill="x",
                padx=5,
                pady=7
            )

            tk.Label(
                caja,
                text=f"Código: {codigo}",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Producto: "
                    f"{item['producto']}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Stock actual: "
                    f"{item['stock']}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Comprar: "
                    f"{item['cantidad_comprar']} unidades"
                ),
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Costo estimado unitario: "
                    f"${item['costo']:.2f}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Inversión estimada: "
                    f"${inversion:.2f}"
                )
            ).pack(anchor="w")

            texto_copiar += (
                f"\nCódigo: {codigo}\n"
                f"Producto: {item['producto']}\n"
                f"Cantidad: "
                f"{item['cantidad_comprar']}\n"
                f"Costo estimado: "
                f"${item['costo']:.2f}\n"
            )

    texto_copiar += (
        "\n--------------------------------\n"
        f"INVERSIÓN TOTAL ESTIMADA: "
        f"${inversion_total:.2f}"
    )

    tk.Label(
        v,
        text=(
            "Inversión total estimada: "
            f"${inversion_total:.2f}"
        ),
        font=("Arial", 13, "bold")
    ).pack(
        pady=5
    )

    def copiar_lista():
        v.clipboard_clear()
        v.clipboard_append(
            texto_copiar
        )

        messagebox.showinfo(
            "Lista copiada",
            (
                "La lista de compra fue "
                "copiada correctamente."
            )
        )

    botones = tk.Frame(v)

    botones.pack(
        pady=10
    )

    tk.Button(
        botones,
        text="Copiar lista",
        width=18,
        command=copiar_lista
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        botones,
        text="Cerrar",
        width=18,
        command=v.destroy
    ).grid(
        row=0,
        column=1,
        padx=5
    )


# ==================================================
# INVENTARIO
# ==================================================

def abrir_inventario():
    v = tk.Toplevel(ventana)

    v.title("Inventario")
    v.geometry("950x720")
    v.resizable(False, False)

    tk.Label(
        v,
        text="INVENTARIO",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(15, 10)
    )

    botones = tk.Frame(v)

    botones.pack(
        pady=(0, 10)
    )

    opciones_botones = [
        (
            "+ Registrar producto",
            abrir_registro_producto
        ),
        (
            "+ Registrar reposición",
            abrir_reposicion
        ),
        (
            "Editar producto",
            abrir_seleccion_editar_producto
        ),
        (
            "Historial reposiciones",
            abrir_historial_reposiciones
        ),
        (
            "Lista de compra",
            abrir_lista_compra
        )
    ]

    for indice, (
        texto,
        comando
    ) in enumerate(opciones_botones):

        tk.Button(
            botones,
            text=texto,
            width=18,
            command=comando
        ).grid(
            row=indice // 3,
            column=indice % 3,
            padx=4,
            pady=4
        )

    marco_busqueda = tk.Frame(v)

    marco_busqueda.pack(
        pady=(5, 10)
    )

    tk.Label(
        marco_busqueda,
        text="Buscar por código o nombre:",
        font=("Arial", 11, "bold")
    ).pack(
        side="left",
        padx=(0, 10)
    )

    variable_busqueda = tk.StringVar()

    tk.Entry(
        marco_busqueda,
        textvariable=variable_busqueda,
        width=30,
        font=("Arial", 11)
    ).pack(
        side="left"
    )

    contenido = crear_area_scroll(v)

    mensaje = tk.Label(
        v,
        text=""
    )

    mensaje.pack()

    def mostrar_productos():
        for widget in (
            contenido.winfo_children()
        ):
            widget.destroy()

        busqueda = (
            variable_busqueda.get()
            .strip()
            .lower()
        )

        encontrados = []

        for item in inventario:
            codigo = str(
                item.get("codigo", "")
            ).lower()

            nombre = str(
                item.get("producto", "")
            ).lower()

            if (
                not busqueda
                or busqueda in codigo
                or busqueda in nombre
            ):
                encontrados.append(
                    item
                )

        mensaje.config(
            text=(
                "Productos encontrados: "
                f"{len(encontrados)}"
            )
        )

        for item in encontrados:
            codigo = (
                item.get("codigo", "")
                or "SIN CÓDIGO"
            )

            nombre = item.get(
                "producto",
                "Sin nombre"
            )

            cantidad = int(
                item.get("cantidad", 0)
            )

            costo = convertir_numero(
                item.get("costo", 0)
            )

            precio = convertir_numero(
                item.get("precio", 0)
            )

            valor = (
                cantidad * precio
            )

            caja = tk.LabelFrame(
                contenido,
                text=nombre,
                font=("Arial", 12, "bold"),
                padx=20,
                pady=10,
                width=820
            )

            caja.pack(
                fill="x",
                padx=5,
                pady=8
            )

            tk.Label(
                caja,
                text=f"Código: {codigo}",
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Stock disponible: "
                    f"{cantidad}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Costo promedio: "
                    f"${costo:.2f}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Precio de venta: "
                    f"${precio:.2f}"
                )
            ).pack(anchor="w")

            tk.Label(
                caja,
                text=(
                    f"Valor potencial: "
                    f"${valor:.2f}"
                ),
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

    variable_busqueda.trace_add(
        "write",
        lambda *args:
        mostrar_productos()
    )

    mostrar_productos()

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(pady=15)


# ==================================================
# VENTAS
# ==================================================

def registrar_venta(
    combo_cliente,
    combo_producto,
    entrada,
    productos_disponibles,
    v
):
    indice_cliente = combo_cliente.current()
    indice_producto = combo_producto.current()

    if (
        indice_cliente < 0
        or indice_producto < 0
    ):
        messagebox.showwarning(
            "Dato requerido",
            "Selecciona cliente y producto."
        )
        return

    try:
        cantidad = int(
            entrada.get()
        )

        if cantidad <= 0:
            raise ValueError

    except ValueError:
        messagebox.showwarning(
            "Cantidad incorrecta",
            "Escribe una cantidad válida."
        )
        return

    cliente = clientes[indice_cliente]
    producto = productos_disponibles[
        indice_producto
    ]

    stock = int(
        producto.get("cantidad", 0)
    )

    if cantidad > stock:
        messagebox.showwarning(
            "Stock insuficiente",
            f"Solo hay {stock} unidades."
        )
        return

    precio = convertir_numero(
        producto.get("precio", 0)
    )

    costo = convertir_numero(
        producto.get("costo", 0)
    )

    monto = cantidad * precio
    costo_total = cantidad * costo
    ganancia = monto - costo_total

    ventas.append({
        "cliente": cliente.get(
            "nombre",
            ""
        ),
        "producto": producto.get(
            "producto",
            ""
        ),
        "codigo_producto":
            producto.get(
                "codigo",
                ""
            ),
        "cantidad": cantidad,
        "precio_unitario": precio,
        "monto": monto,
        "costo_unitario": costo,
        "costo_total": costo_total,
        "ganancia": ganancia
    })

    producto["cantidad"] = (
        stock - cantidad
    )

    guardar_json(
        "ventas.json",
        ventas
    )

    guardar_json(
        "inventario.json",
        inventario
    )

    messagebox.showinfo(
        "Venta registrada",
        (
            "Venta registrada correctamente.\n\n"
            f"Total: ${monto:.2f}"
        )
    )

    v.destroy()


def abrir_registro_venta():
    productos_disponibles = [
        item
        for item in inventario
        if int(
            item.get("cantidad", 0)
        ) > 0
    ]

    if not clientes:
        messagebox.showwarning(
            "Sin clientes",
            "Primero registra un cliente."
        )
        return

    if not productos_disponibles:
        messagebox.showwarning(
            "Sin inventario",
            "No hay productos disponibles."
        )
        return

    v = tk.Toplevel(ventana)

    v.title("Registrar venta")
    v.geometry("500x420")
    v.resizable(False, False)

    tk.Label(
        v,
        text="REGISTRAR VENTA",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(25, 20)
    )

    tk.Label(v, text="Cliente:").pack()

    combo_cliente = ttk.Combobox(
        v,
        values=[
            c.get("nombre", "")
            for c in clientes
        ],
        state="readonly",
        width=35
    )

    combo_cliente.pack(
        pady=(5, 15)
    )

    tk.Label(v, text="Producto:").pack()

    combo_producto = ttk.Combobox(
        v,
        values=[
            (
                f"{p.get('codigo', 'SIN CÓDIGO')} - "
                f"{p.get('producto', '')}"
            )
            for p in productos_disponibles
        ],
        state="readonly",
        width=40
    )

    combo_producto.pack(
        pady=(5, 15)
    )

    tk.Label(v, text="Cantidad:").pack()

    entrada = tk.Entry(
        v,
        width=15
    )

    entrada.pack(
        pady=(5, 20)
    )

    tk.Button(
        v,
        text="Guardar venta",
        width=18,
        command=lambda:
        registrar_venta(
            combo_cliente,
            combo_producto,
            entrada,
            productos_disponibles,
            v
        )
    ).pack()


def abrir_ventas():
    v = tk.Toplevel(ventana)

    v.title("Ventas")
    v.geometry("750x600")
    v.resizable(False, False)

    tk.Label(
        v,
        text="VENTAS REGISTRADAS",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Button(
        v,
        text="+ Registrar venta",
        width=20,
        command=abrir_registro_venta
    ).pack(
        pady=(0, 10)
    )

    contenido = crear_area_scroll(v)

    total = 0

    for numero, venta in enumerate(
        ventas,
        start=1
    ):
        monto = convertir_numero(
            venta.get("monto", 0)
        )

        total += monto

        caja = tk.LabelFrame(
            contenido,
            text=f"Venta {numero}",
            padx=15,
            pady=8,
            width=620
        )

        caja.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            caja,
            text=(
                f"Cliente: "
                f"{venta.get('cliente', '')}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                f"Producto: "
                f"{venta.get('producto', '')}"
            )
        ).pack(anchor="w")

        codigo = venta.get(
            "codigo_producto",
            ""
        )

        if codigo:
            tk.Label(
                caja,
                text=f"Código: {codigo}"
            ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                f"Cantidad: "
                f"{venta.get('cantidad', 1)}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=f"Total: ${monto:.2f}",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

    tk.Label(
        v,
        text=f"TOTAL DE VENTAS: ${total:.2f}",
        font=("Arial", 13, "bold")
    ).pack(pady=5)

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(pady=15)


# ==================================================
# GASTOS
# ==================================================

def registrar_gasto(
    descripcion,
    categoria,
    monto,
    v
):
    descripcion_texto = (
        descripcion.get()
        .strip()
    )

    categoria_texto = (
        categoria.get()
        .strip()
    )

    try:
        monto_numero = convertir_numero(
            monto.get()
        )

        if (
            not descripcion_texto
            or not categoria_texto
            or monto_numero <= 0
        ):
            raise ValueError

    except ValueError:
        messagebox.showwarning(
            "Datos incorrectos",
            "Completa correctamente los datos."
        )
        return

    gastos.append({
        "descripcion": descripcion_texto,
        "categoria": categoria_texto,
        "monto": monto_numero,
        "fecha": datetime.now().strftime(
            "%Y-%m-%d"
        )
    })

    guardar_json(
        "gastos.json",
        gastos
    )

    messagebox.showinfo(
        "Gasto registrado",
        "Gasto registrado correctamente."
    )

    v.destroy()


def abrir_registro_gasto():
    v = tk.Toplevel(ventana)

    v.title("Registrar gasto")
    v.geometry("500x420")
    v.resizable(False, False)

    tk.Label(
        v,
        text="REGISTRAR GASTO",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(25, 20)
    )

    tk.Label(v, text="Descripción:").pack()

    descripcion = tk.Entry(
        v,
        width=35
    )

    descripcion.pack(
        pady=(5, 15)
    )

    tk.Label(v, text="Categoría:").pack()

    categoria = ttk.Combobox(
        v,
        values=[
            "Transporte",
            "Herramientas",
            "Publicidad",
            "Renta",
            "Servicios",
            "Otros"
        ],
        state="readonly",
        width=32
    )

    categoria.pack(
        pady=(5, 15)
    )

    tk.Label(v, text="Monto:").pack()

    monto = tk.Entry(
        v,
        width=20
    )

    monto.pack(
        pady=(5, 20)
    )

    tk.Button(
        v,
        text="Guardar gasto",
        width=18,
        command=lambda:
        registrar_gasto(
            descripcion,
            categoria,
            monto,
            v
        )
    ).pack()


def abrir_gastos():
    v = tk.Toplevel(ventana)

    v.title("Gastos")
    v.geometry("700x600")
    v.resizable(False, False)

    tk.Label(
        v,
        text="GASTOS OPERATIVOS",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Button(
        v,
        text="+ Registrar gasto",
        width=20,
        command=abrir_registro_gasto
    ).pack(pady=10)

    contenido = crear_area_scroll(v)

    total = 0

    for numero, gasto in enumerate(
        gastos,
        start=1
    ):
        monto = convertir_numero(
            gasto.get("monto", 0)
        )

        total += monto

        caja = tk.LabelFrame(
            contenido,
            text=f"Gasto {numero}",
            padx=20,
            pady=8,
            width=580
        )

        caja.pack(
            fill="x",
            padx=5,
            pady=5
        )

        tk.Label(
            caja,
            text=(
                "Descripción: "
                f"{gasto.get('descripcion', gasto.get('concepto', ''))}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=(
                "Categoría: "
                f"{gasto.get('categoria', '')}"
            )
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=f"Monto: ${monto:.2f}"
        ).pack(anchor="w")

    tk.Label(
        v,
        text=f"TOTAL DE GASTOS: ${total:.2f}",
        font=("Arial", 13, "bold")
    ).pack(pady=5)

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(pady=15)


# ==================================================
# RESUMEN
# ==================================================

def abrir_resumen():
    v = tk.Toplevel(ventana)

    v.title("Resumen del negocio")
    v.geometry("700x600")
    v.resizable(False, False)

    ingresos = sum(
        convertir_numero(
            venta.get("monto", 0)
        )
        for venta in ventas
    )

    gastos_totales = sum(
        convertir_numero(
            gasto.get("monto", 0)
        )
        for gasto in gastos
    )

    capital = 0
    valor_venta = 0

    for item in inventario:
        cantidad = int(
            item.get("cantidad", 0)
        )

        costo = convertir_numero(
            item.get("costo", 0)
        )

        precio = convertir_numero(
            item.get("precio", 0)
        )

        capital += cantidad * costo
        valor_venta += cantidad * precio

    ganancia_potencial = (
        valor_venta - capital
    )

    salidas_reposicion = sum(
        convertir_numero(
            r.get("inversion", 0)
        )
        for r in reposiciones
    )

    flujo = (
        ingresos
        - salidas_reposicion
        - gastos_totales
    )

    if flujo > 0:
        estado = "POSITIVO"

    elif flujo < 0:
        estado = "NEGATIVO"

    else:
        estado = "EQUILIBRADO"

    tk.Label(
        v,
        text="RESUMEN DEL NEGOCIO",
        font=("Arial", 18, "bold")
    ).pack(pady=25)

    caja = tk.LabelFrame(
        v,
        text="Información general",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=20
    )

    caja.pack(
        fill="x",
        padx=60
    )

    datos = [
        f"Clientes registrados: {len(clientes)}",
        f"Ventas registradas: {len(ventas)}",
        f"Ingresos por ventas: ${ingresos:.2f}",
        f"Gastos operativos: ${gastos_totales:.2f}",
        "",
        f"Capital en inventario: ${capital:.2f}",
        f"Valor del inventario: ${valor_venta:.2f}",
        f"Ganancia potencial: ${ganancia_potencial:.2f}",
        "",
        f"Flujo de caja: ${flujo:.2f}",
        f"Estado: {estado}"
    ]

    for dato in datos:
        tk.Label(
            caja,
            text=dato,
            font=("Arial", 11)
        ).pack(
            anchor="w",
            pady=3
        )

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(
        side="bottom",
        pady=25
    )


# ==================================================
# DIAGNÓSTICO
# ==================================================

def abrir_diagnostico():
    resultado = calcular_diagnostico(
        ventas,
        inventario,
        reposiciones,
        gastos
    )

    v = tk.Toplevel(ventana)

    v.title("Diagnóstico inteligente")
    v.geometry("800x650")
    v.resizable(False, False)

    tk.Label(
        v,
        text="DIAGNÓSTICO INTELIGENTE",
        font=("Arial", 20, "bold")
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        v,
        text="Análisis automático del negocio"
    ).pack(
        pady=(0, 20)
    )

    financiero = tk.LabelFrame(
        v,
        text="Estado financiero",
        font=("Arial", 12, "bold"),
        padx=25,
        pady=15
    )

    financiero.pack(
        fill="x",
        padx=60
    )

    tk.Label(
        financiero,
        text=(
            f"Flujo de caja: "
            f"${resultado['flujo_neto']:.2f}"
        )
    ).pack(anchor="w", pady=3)

    tk.Label(
        financiero,
        text=(
            f"Estado: "
            f"{resultado['estado_flujo']}"
        ),
        font=("Arial", 11, "bold")
    ).pack(anchor="w", pady=3)

    tk.Label(
        financiero,
        text=(
            "Ganancia potencial: "
            f"${resultado['ganancia_potencial']:.2f}"
        )
    ).pack(anchor="w", pady=3)

    tk.Label(
        financiero,
        text=(
            "Gastos sobre ventas: "
            f"{resultado['porcentaje_gastos']:.2f}%"
        )
    ).pack(anchor="w", pady=3)

    analisis = tk.LabelFrame(
        v,
        text="Análisis",
        font=("Arial", 12, "bold"),
        padx=25,
        pady=15
    )

    analisis.pack(
        fill="x",
        padx=60,
        pady=10
    )

    for mensaje in resultado[
        "diagnosticos"
    ]:
        tk.Label(
            analisis,
            text=mensaje
        ).pack(
            anchor="w",
            pady=4
        )

    recomendacion = tk.LabelFrame(
        v,
        text="Recomendación",
        font=("Arial", 12, "bold"),
        padx=25,
        pady=15
    )

    recomendacion.pack(
        fill="x",
        padx=60
    )

    tk.Label(
        recomendacion,
        text=resultado["recomendacion"],
        wraplength=620,
        justify="left"
    ).pack(anchor="w")

    tk.Button(
        v,
        text="Cerrar",
        width=15,
        command=v.destroy
    ).pack(
        side="bottom",
        pady=20
    )


# ==================================================
# VENTANA PRINCIPAL
# ==================================================

ventana = tk.Tk()

ventana.title(
    "AI Business Assistant"
)

ventana.geometry(
    "700x520"
)

ventana.resizable(
    False,
    False
)

tk.Label(
    ventana,
    text="AI BUSINESS ASSISTANT",
    font=("Arial", 22, "bold")
).pack(
    pady=(30, 5)
)

tk.Label(
    ventana,
    text="Panel de administración del negocio",
    font=("Arial", 12)
).pack(
    pady=(0, 30)
)

contenedor = tk.Frame(
    ventana
)

contenedor.pack()

botones = [
    ("Clientes", abrir_clientes),
    ("Ventas", abrir_ventas),
    ("Inventario", abrir_inventario),
    ("Gastos", abrir_gastos),
    ("Resumen del negocio", abrir_resumen),
    (
        "Diagnóstico inteligente",
        abrir_diagnostico
    )
]

for indice, (
    texto,
    comando
) in enumerate(botones):

    tk.Button(
        contenedor,
        text=texto,
        width=20,
        height=3,
        command=comando
    ).grid(
        row=indice // 2,
        column=indice % 2,
        padx=10,
        pady=10
    )

tk.Button(
    ventana,
    text="Salir",
    width=15,
    command=ventana.destroy
).pack(pady=30)

ventana.mainloop()