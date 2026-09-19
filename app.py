import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

from clientes import clientes
from inventario import inventario, reposiciones
from ventas import ventas
from gastos import gastos
from diagnostico import calcular_diagnostico
from cuentas import cuentas_por_cobrar, guardar_cuentas
from cuentas_ui import abrir_cuentas_por_cobrar
from cliente_resumen_ui import abrir_resumen_cliente
from dashboard import calcular_dashboard
from dashboard_ui import abrir_dashboard_profesional
from idiomas import t, cambiar_idioma, obtener_idioma
from facturacion import generar_recibo_pdf, abrir_archivo
from configuracion_negocio_ui import abrir_configuracion_negocio


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
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Registrar cliente"
    )

    v.geometry(
        "620x430"
    )

    v.minsize(
        560,
        390
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 16)
    )

    tk.Label(
        encabezado,
        text=t("new_client_title"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=t("new_client_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    tarjeta = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    tarjeta.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    tk.Label(
        tarjeta,
        text=t("client_information"),
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=22,
        pady=(22, 14)
    )

    tk.Label(
        tarjeta,
        text=t("client_name"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=22
    )

    entrada = tk.Entry(
        tarjeta,
        width=40,
        font=("Segoe UI", 11),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        insertbackground=TEXTO,
        relief="flat",
        bd=0
    )

    entrada.pack(
        fill="x",
        padx=22,
        pady=(8, 22),
        ipady=9
    )

    entrada.focus()

    botones = tk.Frame(
        tarjeta,
        bg=PANEL
    )

    botones.pack(
        fill="x",
        padx=22,
        pady=(0, 22)
    )

    tk.Button(
        botones,
        text=t("save_client"),
        command=lambda:
        registrar_cliente(
            entrada,
            v
        ),
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=9
    ).pack(
        side="left"
    )

    tk.Button(
        botones,
        text=t("cancel"),
        command=v.destroy,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=9
    ).pack(
        side="right"
    )


def abrir_clientes():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Clientes"
    )

    v.geometry(
        "900x720"
    )

    v.minsize(
        760,
        580
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    # ==================================================
    # SCROLL GENERAL
    # ==================================================

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )
    )

    def ajustar_ancho(event):
        canvas.itemconfigure(
            ventana_canvas,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        ajustar_ancho
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    # ==================================================
    # ENCABEZADO
    # ==================================================

    encabezado = tk.Frame(
        contenido,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 16)
    )

    tk.Label(
        encabezado,
        text=t("client_management"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=t("client_directory_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    # ==================================================
    # ACCIONES
    # ==================================================

    acciones = tk.Frame(
        contenido,
        bg=FONDO
    )

    acciones.pack(
        fill="x",
        padx=30,
        pady=(0, 16)
    )

    tk.Button(
        acciones,
        text=t("new_client"),
        command=abrir_registro_cliente,
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=9
    ).pack(
        side="left"
    )

    tk.Button(
        acciones,
        text=t("client_intelligence"),
        command=lambda: abrir_resumen_cliente(
            v
        ),
        font=("Segoe UI", 10, "bold"),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=9
    ).pack(
        side="left",
        padx=(10, 0)
    )

    # ==================================================
    # RESUMEN
    # ==================================================

    panel_resumen = tk.Frame(
        contenido,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_resumen.pack(
        fill="x",
        padx=30,
        pady=(0, 16)
    )

    tk.Label(
        panel_resumen,
        text=t("total_clients"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 4)
    )

    tk.Label(
        panel_resumen,
        text=str(
            len(clientes)
        ),
        font=("Segoe UI", 22, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(0, 15)
    )

    # ==================================================
    # LISTA DE CLIENTES
    # ==================================================

    panel_lista = tk.Frame(
        contenido,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_lista.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 18)
    )

    tk.Label(
        panel_lista,
        text=t("client_directory"),
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(16, 12)
    )

    if not clientes:
        tk.Label(
            panel_lista,
            text="No clients registered yet.",
            font=("Segoe UI", 10),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    else:
        for numero, cliente in enumerate(
            clientes,
            start=1
        ):
            tarjeta = tk.Frame(
                panel_lista,
                bg=PANEL_SECUNDARIO,
                highlightbackground=BORDE,
                highlightthickness=1
            )

            tarjeta.pack(
                fill="x",
                padx=16,
                pady=6
            )

            tk.Frame(
                tarjeta,
                bg=AZUL,
                width=5
            ).pack(
                side="left",
                fill="y"
            )

            info = tk.Frame(
                tarjeta,
                bg=PANEL_SECUNDARIO
            )

            info.pack(
                side="left",
                fill="both",
                expand=True,
                padx=16,
                pady=12
            )

            tk.Label(
                info,
                text=(
                    f"{numero:02d}  "
                    f"{cliente.get('nombre', 'Sin nombre')}"
                ),
                font=("Segoe UI", 11, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO
            ).pack(
                anchor="w"
            )

            telefono = str(
                cliente.get(
                    "telefono",
                    ""
                )
            ).strip()

            correo = str(
                cliente.get(
                    "correo",
                    ""
                )
            ).strip()

            detalles = []

            if telefono:
                detalles.append(
                    f"Phone: {telefono}"
                )

            if correo:
                detalles.append(
                    f"Email: {correo}"
                )

            tk.Label(
                info,
                text=(
                    "  •  ".join(detalles)
                    if detalles
                    else "Customer profile"
                ),
                font=("Segoe UI", 9),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO_SECUNDARIO
            ).pack(
                anchor="w",
                pady=(4, 0)
            )

    # ==================================================
    # PIE
    # ==================================================

    pie = tk.Frame(
        contenido,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 25)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )



# ==================================================
# TEMA PROFESIONAL PARA INVENTARIO
# ==================================================

def aplicar_tema_inventario(widget):
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    AZUL = "#3B82F6"

    try:
        if isinstance(widget, tk.Toplevel):
            widget.configure(
                bg=FONDO
            )

        elif isinstance(widget, tk.Frame):
            widget.configure(
                bg=PANEL
            )

        elif isinstance(widget, tk.LabelFrame):
            widget.configure(
                bg=PANEL,
                fg=TEXTO,
                bd=0,
                highlightbackground=BORDE,
                highlightthickness=1
            )

        elif isinstance(widget, tk.Label):
            fondo = PANEL

            try:
                fondo = widget.master.cget("bg")
            except Exception:
                pass

            widget.configure(
                bg=fondo,
                fg=TEXTO
            )

        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg=PANEL_SECUNDARIO,
                fg=TEXTO,
                insertbackground=TEXTO,
                relief="flat",
                bd=0
            )

        elif isinstance(widget, tk.Listbox):
            widget.configure(
                bg=PANEL_SECUNDARIO,
                fg=TEXTO,
                selectbackground=AZUL,
                selectforeground="white",
                relief="flat",
                bd=0
            )

        elif isinstance(widget, tk.Button):
            widget.configure(
                bg=AZUL,
                fg="white",
                activebackground="#2563EB",
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 10, "bold")
            )

    except tk.TclError:
        pass

    for hijo in widget.winfo_children():
        aplicar_tema_inventario(
            hijo
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
        codigo_existente = str(
            item.get("codigo", "")
        ).strip().upper()

        if codigo_existente == codigo:
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

    v.title("AI Business Assistant - Product")
    v.geometry("520x600")
    v.resizable(False, False)

    tk.Label(
        v,
        text=t("register_product"),
        font=("Arial", 18, "bold")
    ).pack(pady=(25, 20))

    campos = {}

    etiquetas = [
        ("codigo", t("product_code") + ":"),
        ("nombre", t("product_name") + ":"),
        ("cantidad", t("initial_quantity") + ":"),
        ("costo", t("unit_cost") + ":"),
        ("precio", t("sale_price") + ":")
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
        text=t("save_product"),
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

    aplicar_tema_inventario(
        v
    )


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

    v.title("AI Business Assistant - Edit Product")
    v.geometry("520x500")
    v.resizable(False, False)

    tk.Label(
        v,
        text=t("edit_product").upper(),
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

    aplicar_tema_inventario(
        v
    )


def abrir_seleccion_editar_producto():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"

    if not inventario:
        messagebox.showwarning(
            "Sin productos",
            "No hay productos para editar."
        )
        return

    v = tk.Toplevel(
        ventana
    )

    v.title(
        "AI Business Assistant - Edit Product"
    )

    v.geometry(
        "700x420"
    )

    v.minsize(
        620,
        380
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 16)
    )

    tk.Label(
        encabezado,
        text=t("edit_product").upper(),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=t("select_product"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    panel = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    tk.Label(
        panel,
        text=t("select_product"),
        font=("Segoe UI", 10, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=22,
        pady=(22, 8)
    )

    opciones = [
        (
            f"{item.get('codigo', 'SIN CÓDIGO')} - "
            f"{item.get('producto', '')}"
        )
        for item in inventario
    ]

    combo = ttk.Combobox(
        panel,
        values=opciones,
        state="readonly",
        width=50
    )

    combo.pack(
        fill="x",
        padx=22,
        pady=(0, 24)
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
        abrir_editor_producto(
            indice
        )

    botones = tk.Frame(
        panel,
        bg=PANEL
    )

    botones.pack(
        fill="x",
        padx=22,
        pady=(0, 22)
    )

    tk.Button(
        botones,
        text=t("continue_edit"),
        command=continuar,
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=9
    ).pack(
        side="left"
    )

    tk.Button(
        botones,
        text=t("cancel"),
        command=v.destroy,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=9
    ).pack(
        side="right"
    )


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
            stock_anterior * costo_anterior
        )
        +
        (
            cantidad * costo_compra
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

    tk.Label(
        v,
        text="Producto:"
    ).pack()

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

    aplicar_tema_inventario(
        v
    )


def abrir_historial_reposiciones():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    VERDE = "#22C55E"
    AZUL = "#3B82F6"

    v = tk.Toplevel(
        ventana
    )

    v.title(
        "AI Business Assistant - Restock History"
    )

    v.geometry(
        "980x760"
    )

    v.minsize(
        820,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 15)
    )

    tk.Label(
        encabezado,
        text=t("restock_history_title"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=t("restock_history"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    total = 0

    for reposicion in reposiciones:
        cantidad = int(
            reposicion.get(
                "cantidad",
                0
            )
        )

        costo = convertir_numero(
            reposicion.get(
                "costo_unitario",
                reposicion.get(
                    "costo",
                    0
                )
            )
        )

        inversion = convertir_numero(
            reposicion.get(
                "inversion",
                cantidad * costo
            )
        )

        total += inversion

    kpi = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    kpi.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Frame(
        kpi,
        bg=AZUL,
        width=5
    ).pack(
        side="left",
        fill="y"
    )

    cuerpo_kpi = tk.Frame(
        kpi,
        bg=PANEL
    )

    cuerpo_kpi.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=14
    )

    tk.Label(
        cuerpo_kpi,
        text=t("total_restock_investment"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w"
    )

    tk.Label(
        cuerpo_kpi,
        text=f"${total:,.2f}",
        font=("Segoe UI", 20, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 14)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

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
                reposicion.get(
                    "costo",
                    0
                )
            )
        )

        inversion = convertir_numero(
            reposicion.get(
                "inversion",
                cantidad * costo
            )
        )

        tarjeta = tk.Frame(
            contenido,
            bg=PANEL_SECUNDARIO,
            highlightbackground=BORDE,
            highlightthickness=1
        )

        tarjeta.pack(
            fill="x",
            pady=6
        )

        cabecera = tk.Frame(
            tarjeta,
            bg=PANEL_SECUNDARIO
        )

        cabecera.pack(
            fill="x",
            padx=16,
            pady=(12, 6)
        )

        tk.Label(
            cabecera,
            text=(
                f"RESTOCK #{numero:02d}"
                if obtener_idioma() == "en"
                else f"REPOSICIÓN #{numero:02d}"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO
        ).pack(
            side="left"
        )

        tk.Label(
            cabecera,
            text=f"${inversion:,.2f}",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=VERDE
        ).pack(
            side="right"
        )

        detalle = (
            f"{t('code')}: "
            f"{reposicion.get('codigo', '') or 'SIN CÓDIGO'}\n"
            f"{t('product')}: "
            f"{reposicion.get('producto', '')}\n"
            f"{t('date')}: "
            f"{reposicion.get('fecha', 'Sin fecha')}\n"
            f"{t('units_purchased')}: {cantidad}\n"
            f"{t('supplier_cost_label')}: ${costo:,.2f}"
        )

        tk.Label(
            tarjeta,
            text=detalle,
            justify="left",
            font=("Segoe UI", 9),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

    pie = tk.Frame(
        v,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )


# ==================================================
# LISTA DE COMPRA
# ==================================================

def abrir_lista_compra():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    VERDE = "#22C55E"
    AMARILLO = "#F59E0B"
    AZUL = "#3B82F6"

    v = tk.Toplevel(
        ventana
    )

    v.title(
        "AI Business Assistant - Purchase List"
    )

    v.geometry(
        "980x760"
    )

    v.minsize(
        820,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    stock_minimo = 10
    stock_objetivo = 20

    productos_comprar = []

    for item in inventario:
        stock = int(
            item.get(
                "cantidad",
                0
            )
        )

        if stock <= stock_minimo:
            cantidad_comprar = (
                stock_objetivo
                - stock
            )

            if cantidad_comprar > 0:
                productos_comprar.append({
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
                })

    inversion_total = 0

    for item in productos_comprar:
        inversion_total += (
            item["cantidad_comprar"]
            * item["costo"]
        )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 15)
    )

    tk.Label(
        encabezado,
        text=t("purchase_list_title"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=t("purchase_list_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    kpi = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    kpi.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Frame(
        kpi,
        bg=AMARILLO,
        width=5
    ).pack(
        side="left",
        fill="y"
    )

    cuerpo_kpi = tk.Frame(
        kpi,
        bg=PANEL
    )

    cuerpo_kpi.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=14
    )

    tk.Label(
        cuerpo_kpi,
        text=t("estimated_total_investment"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w"
    )

    tk.Label(
        cuerpo_kpi,
        text=f"${inversion_total:,.2f}",
        font=("Segoe UI", 20, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 14)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    texto_copiar = (
        "PURCHASE LIST\n"
        if obtener_idioma() == "en"
        else "LISTA DE COMPRA AL PROVEEDOR\n"
    )

    texto_copiar += (
        "--------------------------------\n"
    )

    for numero, item in enumerate(
        productos_comprar,
        start=1
    ):
        codigo = (
            item["codigo"]
            or "SIN CÓDIGO"
        )

        inversion = (
            item["cantidad_comprar"]
            * item["costo"]
        )

        tarjeta = tk.Frame(
            contenido,
            bg=PANEL_SECUNDARIO,
            highlightbackground=BORDE,
            highlightthickness=1
        )

        tarjeta.pack(
            fill="x",
            pady=6
        )

        cabecera = tk.Frame(
            tarjeta,
            bg=PANEL_SECUNDARIO
        )

        cabecera.pack(
            fill="x",
            padx=16,
            pady=(12, 6)
        )

        tk.Label(
            cabecera,
            text=(
                f"{numero:02d}  "
                f"{item['producto']}"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO
        ).pack(
            side="left"
        )

        tk.Label(
            cabecera,
            text=f"${inversion:,.2f}",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=VERDE
        ).pack(
            side="right"
        )

        detalle = (
            f"{t('code')}: {codigo}\n"
            f"{t('current_stock')}: {item['stock']}\n"
            f"{t('buy_units')}: "
            f"{item['cantidad_comprar']}\n"
            f"{t('estimated_unit_cost')}: "
            f"${item['costo']:,.2f}"
        )

        tk.Label(
            tarjeta,
            text=detalle,
            justify="left",
            font=("Segoe UI", 9),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

        texto_copiar += (
            f"\n{t('code')}: {codigo}\n"
            f"{t('product')}: "
            f"{item['producto']}\n"
            f"{t('quantity')}: "
            f"{item['cantidad_comprar']}\n"
            f"{t('estimated_unit_cost')}: "
            f"${item['costo']:.2f}\n"
        )

    texto_copiar += (
        "\n--------------------------------\n"
        f"{t('estimated_total_investment')}: "
        f"${inversion_total:.2f}"
    )

    def copiar_lista():
        v.clipboard_clear()

        v.clipboard_append(
            texto_copiar
        )

        messagebox.showinfo(
            "Lista copiada"
            if obtener_idioma() == "es"
            else "List copied",
            "La lista fue copiada correctamente."
            if obtener_idioma() == "es"
            else "The purchase list was copied successfully."
        )

    pie = tk.Frame(
        v,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    tk.Button(
        pie,
        text=t("copy_list"),
        command=copiar_lista,
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="left"
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )


# ==================================================
# INVENTARIO
# ==================================================

def abrir_inventario():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    AMARILLO = "#F59E0B"
    CYAN = "#06B6D4"

    v = tk.Toplevel(
        ventana
    )

    v.title(
        "AI Business Assistant - Inventory"
    )

    v.geometry(
        "1050x780"
    )

    v.minsize(
        850,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 14)
    )

    tk.Label(
        encabezado,
        text=t("inventory_management"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=t("inventory_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    acciones = tk.Frame(
        v,
        bg=FONDO
    )

    acciones.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    opciones = [
        (
            t("new_product"),
            abrir_registro_producto,
            AZUL
        ),
        (
            t("new_restock"),
            abrir_reposicion,
            VERDE
        ),
        (
            t("edit_product"),
            abrir_seleccion_editar_producto,
            PANEL_SECUNDARIO
        ),
        (
            t("restock_history"),
            abrir_historial_reposiciones,
            PANEL_SECUNDARIO
        ),
        (
            t("purchase_list"),
            abrir_lista_compra,
            PANEL_SECUNDARIO
        )
    ]

    for texto_boton, comando, color in opciones:
        tk.Button(
            acciones,
            text=texto_boton,
            command=comando,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            activebackground="#24344D",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=(0, 8)
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

    ganancia_potencial = (
        valor_inventario
        - capital_inventario
    )

    marco_kpis = tk.Frame(
        v,
        bg=FONDO
    )

    marco_kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    datos_kpi = [
        (
            t("inventory_capital"),
            f"${capital_inventario:,.2f}",
            AZUL
        ),
        (
            t("inventory_value"),
            f"${valor_inventario:,.2f}",
            CYAN
        ),
        (
            t("potential_profit"),
            f"${ganancia_potencial:,.2f}",
            VERDE
        )
    ]

    for columna, (
        titulo,
        valor,
        color
    ) in enumerate(datos_kpi):
        tarjeta = tk.Frame(
            marco_kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=95
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(
            False
        )

        marco_kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        cuerpo_kpi = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo_kpi.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo_kpi,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w"
        )

        tk.Label(
            cuerpo_kpi,
            text=valor,
            font=("Segoe UI", 17, "bold"),
            bg=PANEL,
            fg=TEXTO
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    panel_busqueda = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_busqueda.pack(
        fill="x",
        padx=30,
        pady=(0, 12)
    )

    tk.Label(
        panel_busqueda,
        text=t("inventory_search"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=18,
        pady=(12, 5)
    )

    variable_busqueda = tk.StringVar()

    entrada_busqueda = tk.Entry(
        panel_busqueda,
        textvariable=variable_busqueda,
        font=("Segoe UI", 11),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        insertbackground=TEXTO,
        relief="flat",
        bd=0
    )

    entrada_busqueda.pack(
        fill="x",
        padx=18,
        pady=(0, 12),
        ipady=8
    )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 12)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    def mostrar_productos(*args):
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
                item.get(
                    "codigo",
                    ""
                )
            ).lower()

            nombre = str(
                item.get(
                    "producto",
                    ""
                )
            ).lower()

            if (
                not busqueda
                or busqueda in codigo
                or busqueda in nombre
            ):
                encontrados.append(
                    item
                )

        for numero, item in enumerate(
            encontrados,
            start=1
        ):
            codigo = (
                item.get(
                    "codigo",
                    ""
                )
                or "SIN CÓDIGO"
            )

            nombre = item.get(
                "producto",
                "Sin nombre"
            )

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

            valor = (
                cantidad * precio
            )

            tarjeta = tk.Frame(
                contenido,
                bg=PANEL_SECUNDARIO,
                highlightbackground=BORDE,
                highlightthickness=1
            )

            tarjeta.pack(
                fill="x",
                pady=6
            )

            cabecera = tk.Frame(
                tarjeta,
                bg=PANEL_SECUNDARIO
            )

            cabecera.pack(
                fill="x",
                padx=16,
                pady=(12, 6)
            )

            tk.Label(
                cabecera,
                text=(
                    f"{numero:02d}  {nombre}"
                ),
                font=("Segoe UI", 10, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO
            ).pack(
                side="left"
            )

            tk.Label(
                cabecera,
                text=f"${valor:,.2f}",
                font=("Segoe UI", 11, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=VERDE
            ).pack(
                side="right"
            )

            detalle = (
                f"Code: {codigo}\n"
                f"{t('stock_available')}: {cantidad}\n"
                f"{t('average_cost')}: ${costo:,.2f}\n"
                f"{t('sale_price')}: ${precio:,.2f}"
            )

            tk.Label(
                tarjeta,
                text=detalle,
                justify="left",
                font=("Segoe UI", 9),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO_SECUNDARIO
            ).pack(
                anchor="w",
                padx=16,
                pady=(0, 12)
            )

        canvas.yview_moveto(
            0
        )

    variable_busqueda.trace_add(
        "write",
        mostrar_productos
    )

    mostrar_productos()

    pie = tk.Frame(
        v,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    etiqueta_encontrados = tk.Label(
        pie,
        text=(
            f"{t('products_found')}: "
            f"{len(inventario)}"
        ),
        font=("Segoe UI", 9),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    )

    etiqueta_encontrados.pack(
        side="left"
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )

    entrada_busqueda.focus()


# ==================================================
# TEMA PROFESIONAL PARA VENTAS
# ==================================================

def aplicar_tema_ventas(widget):
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"

    try:
        if isinstance(widget, (tk.Toplevel, tk.Frame)):
            widget.configure(
                bg=FONDO
                if isinstance(widget, tk.Toplevel)
                else PANEL
            )

        elif isinstance(widget, tk.LabelFrame):
            widget.configure(
                bg=PANEL,
                fg=TEXTO,
                highlightbackground=BORDE,
                highlightthickness=1,
                bd=0
            )

        elif isinstance(widget, tk.Label):
            fondo_padre = PANEL

            try:
                fondo_padre = widget.master.cget("bg")
            except Exception:
                pass

            widget.configure(
                bg=fondo_padre,
                fg=TEXTO
            )

        elif isinstance(widget, tk.Button):
            widget.configure(
                bg=AZUL,
                fg="white",
                activebackground="#2563EB",
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 10, "bold")
            )

        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg=PANEL_SECUNDARIO,
                fg=TEXTO,
                insertbackground=TEXTO,
                relief="flat",
                bd=0
            )

        elif isinstance(widget, tk.Listbox):
            widget.configure(
                bg=PANEL_SECUNDARIO,
                fg=TEXTO,
                selectbackground=AZUL,
                selectforeground="white",
                relief="flat",
                bd=0
            )

        elif isinstance(widget, tk.Canvas):
            widget.configure(
                bg=FONDO,
                highlightthickness=0
            )

        if isinstance(widget, ttk.Combobox):
            estilo = ttk.Style()

            try:
                estilo.theme_use(
                    "clam"
                )
            except Exception:
                pass

            estilo.configure(
                "Ventas.TCombobox",
                fieldbackground=PANEL_SECUNDARIO,
                background=PANEL_SECUNDARIO,
                foreground=TEXTO,
                arrowcolor=TEXTO,
                bordercolor=BORDE,
                lightcolor=BORDE,
                darkcolor=BORDE
            )

            estilo.map(
                "Ventas.TCombobox",
                fieldbackground=[
                    ("readonly", PANEL_SECUNDARIO)
                ],
                foreground=[
                    ("readonly", TEXTO)
                ],
                selectbackground=[
                    ("readonly", PANEL_SECUNDARIO)
                ],
                selectforeground=[
                    ("readonly", TEXTO)
                ]
            )

            widget.configure(
                style="Ventas.TCombobox"
            )

    except tk.TclError:
        pass

    for hijo in widget.winfo_children():
        aplicar_tema_ventas(
            hijo
        )

# ==================================================
# REGISTRAR VENTA
# ==================================================

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

    v.title("AI Business Assistant - New Sale")
    v.geometry("820x820")
    v.minsize(720, 650)
    v.resizable(True, True)
    v.configure(bg="#0B1220")

    marco_scroll = tk.Frame(v)

    marco_scroll.pack(
        fill="both",
        expand=True
    )

    canvas_venta = tk.Canvas(
        marco_scroll,
        highlightthickness=0
    )

    scrollbar_venta = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas_venta.yview
    )

    contenido_venta = tk.Frame(
        canvas_venta
    )

    contenido_venta.bind(
        "<Configure>",
        lambda e: canvas_venta.configure(
            scrollregion=canvas_venta.bbox("all")
        )
    )

    ventana_canvas = canvas_venta.create_window(
        (0, 0),
        window=contenido_venta,
        anchor="nw"
    )

    canvas_venta.bind(
        "<Configure>",
        lambda e: canvas_venta.itemconfigure(
            ventana_canvas,
            width=e.width
        )
    )

    canvas_venta.configure(
        yscrollcommand=scrollbar_venta.set
    )

    canvas_venta.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_venta.pack(
        side="right",
        fill="y"
    )

    def mover_rueda(event):
        canvas_venta.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas_venta.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    tk.Label(
        contenido_venta,
        text="NEW SALE",
        font=("Segoe UI", 22, "bold"),
        bg="#0B1220",
        fg="#F4F7FB"
    ).pack(
        pady=(25, 20)
    )

    tk.Label(
        contenido_venta,
        text="Sales transaction and payment registration",
        font=("Segoe UI", 10),
        bg="#0B1220",
        fg="#8FA3BF"
    ).pack(
        pady=(0, 18)
    )

    tk.Label(
        contenido_venta,
        text="Cliente:"
    ).pack()

    combo_cliente = ttk.Combobox(
        contenido_venta,
        values=[
            c.get("nombre", "")
            for c in clientes
        ],
        state="readonly",
        width=40
    )

    combo_cliente.pack(
        pady=(5, 15)
    )

    tk.Label(
        contenido_venta,
        text="Escribe código o nombre para filtrar la lista:"
    ).pack()

    variable_busqueda = tk.StringVar()

    entrada_busqueda = tk.Entry(
        contenido_venta,
        textvariable=variable_busqueda,
        width=40,
        font=("Arial", 11)
    )

    entrada_busqueda.pack(
        pady=(5, 10)
    )

    tk.Label(
        contenido_venta,
        text="Lista de productos (código - nombre):"
    ).pack()

    lista_productos = tk.Listbox(
        contenido_venta,
        width=50,
        height=4,
        font=("Arial", 10)
    )

    lista_productos.pack(
        pady=(5, 10)
    )

    tk.Label(
        contenido_venta,
        text="Producto seleccionado:"
    ).pack()

    combo_producto = ttk.Combobox(
        contenido_venta,
        state="readonly",
        width=45
    )

    combo_producto.pack(
        pady=(5, 10)
    )

    etiqueta_info = tk.Label(
        contenido_venta,
        text="",
        font=("Arial", 11, "bold")
    )

    etiqueta_info.pack(
        pady=(0, 15)
    )

    tk.Label(
        contenido_venta,
        text="Cantidad:"
    ).pack()

    variable_cantidad = tk.StringVar()

    entrada_cantidad = tk.Entry(
        contenido_venta,
        textvariable=variable_cantidad,
        width=15,
        font=("Arial", 11)
    )

    entrada_cantidad.pack(
        pady=(5, 15)
    )

    tk.Label(
        contenido_venta,
        text="Tipo de venta:"
    ).pack()

    variable_tipo_venta = tk.StringVar(
        value="Pagada"
    )

    combo_tipo_venta = ttk.Combobox(
        contenido_venta,
        textvariable=variable_tipo_venta,
        values=[
            "Pagada",
            "A crédito"
        ],
        state="readonly",
        width=20
    )

    combo_tipo_venta.pack(
        pady=(5, 12)
    )

    tk.Label(
        contenido_venta,
        text="Fecha de vencimiento si es a crédito (YYYY-MM-DD):"
    ).pack()

    entrada_vencimiento = tk.Entry(
        contenido_venta,
        width=18,
        font=("Arial", 11)
    )

    entrada_vencimiento.pack(
        pady=(5, 15)
    )

    marco_calculo = tk.LabelFrame(
        contenido_venta,
        text="Cálculo de la venta",
        font=("Arial", 11, "bold"),
        padx=25,
        pady=15
    )

    marco_calculo.pack(
        fill="x",
        padx=70,
        pady=10
    )

    etiqueta_precio = tk.Label(
        marco_calculo,
        text="Precio unitario: $0.00"
    )

    etiqueta_precio.pack(
        anchor="w",
        pady=3
    )

    etiqueta_costo = tk.Label(
        marco_calculo,
        text="Costo unitario: $0.00"
    )

    etiqueta_costo.pack(
        anchor="w",
        pady=3
    )

    etiqueta_costo_total = tk.Label(
        marco_calculo,
        text="Costo total: $0.00"
    )

    etiqueta_costo_total.pack(
        anchor="w",
        pady=3
    )

    etiqueta_total = tk.Label(
        marco_calculo,
        text="TOTAL A COBRAR: $0.00",
        font=("Arial", 13, "bold")
    )

    etiqueta_total.pack(
        anchor="w",
        pady=(8, 3)
    )

    etiqueta_ganancia = tk.Label(
        marco_calculo,
        text="GANANCIA REAL: $0.00",
        font=("Arial", 12, "bold")
    )

    etiqueta_ganancia.pack(
        anchor="w",
        pady=3
    )

    productos_filtrados = []

    def producto_actual():
        indice = combo_producto.current()

        if indice < 0:
            return None

        if indice >= len(
            productos_filtrados
        ):
            return None

        return productos_filtrados[
            indice
        ]

    def calcular_venta(*args):
        producto = producto_actual()

        if producto is None:
            etiqueta_precio.config(
                text="Precio unitario: $0.00"
            )

            etiqueta_costo.config(
                text="Costo unitario: $0.00"
            )

            etiqueta_costo_total.config(
                text="Costo total: $0.00"
            )

            etiqueta_total.config(
                text="TOTAL A COBRAR: $0.00"
            )

            etiqueta_ganancia.config(
                text="GANANCIA REAL: $0.00"
            )

            return

        precio = convertir_numero(
            producto.get("precio", 0)
        )

        costo = convertir_numero(
            producto.get("costo", 0)
        )

        etiqueta_precio.config(
            text=(
                f"Precio unitario: "
                f"${precio:.2f}"
            )
        )

        etiqueta_costo.config(
            text=(
                f"Costo unitario: "
                f"${costo:.2f}"
            )
        )

        try:
            cantidad = int(
                variable_cantidad.get()
            )

            if cantidad <= 0:
                raise ValueError

        except ValueError:
            etiqueta_costo_total.config(
                text="Costo total: $0.00"
            )

            etiqueta_total.config(
                text="TOTAL A COBRAR: $0.00"
            )

            etiqueta_ganancia.config(
                text="GANANCIA REAL: $0.00"
            )

            return

        total = (
            cantidad * precio
        )

        costo_total = (
            cantidad * costo
        )

        ganancia = (
            total - costo_total
        )

        etiqueta_costo_total.config(
            text=(
                f"Costo total: "
                f"${costo_total:.2f}"
            )
        )

        etiqueta_total.config(
            text=(
                f"TOTAL A COBRAR: "
                f"${total:.2f}"
            )
        )

        etiqueta_ganancia.config(
            text=(
                f"GANANCIA REAL: "
                f"${ganancia:.2f}"
            )
        )

    def mostrar_info_producto(event=None):
        producto = producto_actual()

        if producto is None:
            etiqueta_info.config(
                text=""
            )
            calcular_venta()
            return

        stock = int(
            producto.get("cantidad", 0)
        )

        precio = convertir_numero(
            producto.get("precio", 0)
        )

        etiqueta_info.config(
            text=(
                f"Stock: {stock}    |    "
                f"Precio: ${precio:.2f}"
            )
        )

        calcular_venta()

    def actualizar_productos(*args):
        nonlocal productos_filtrados

        busqueda = (
            variable_busqueda.get()
            .strip()
            .lower()
        )

        productos_filtrados = []

        for item in productos_disponibles:
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
                productos_filtrados.append(
                    item
                )

        opciones = [
            (
                f"{item.get('codigo', 'SIN CÓDIGO')} - "
                f"{item.get('producto', '')}"
            )
            for item in productos_filtrados
        ]

        combo_producto[
            "values"
        ] = opciones

        combo_producto.set("")

        lista_productos.delete(
            0,
            tk.END
        )

        for opcion in opciones:
            lista_productos.insert(
                tk.END,
                opcion
            )

        etiqueta_info.config(
            text=""
        )

        calcular_venta()

        if len(
            productos_filtrados
        ) == 1:
            combo_producto.current(0)
            lista_productos.selection_set(0)
            mostrar_info_producto()

    variable_busqueda.trace_add(
        "write",
        actualizar_productos
    )

    entrada_busqueda.bind(
        "<KeyRelease>",
        actualizar_productos
    )

    variable_cantidad.trace_add(
        "write",
        calcular_venta
    )

    combo_producto.bind(
        "<<ComboboxSelected>>",
        mostrar_info_producto
    )

    def seleccionar_desde_lista(event=None):
        seleccion = lista_productos.curselection()

        if not seleccion:
            return

        indice = seleccion[0]

        combo_producto.current(
            indice
        )

        mostrar_info_producto()

    lista_productos.bind(
        "<<ListboxSelect>>",
        seleccionar_desde_lista
    )

    actualizar_productos()

    def guardar_venta():
        indice_cliente = (
            combo_cliente.current()
        )

        producto = producto_actual()

        if indice_cliente < 0:
            messagebox.showwarning(
                "Cliente requerido",
                "Selecciona un cliente."
            )
            return

        if producto is None:
            messagebox.showwarning(
                "Producto requerido",
                "Busca y selecciona un producto."
            )
            return

        try:
            cantidad = int(
                variable_cantidad.get()
            )

            if cantidad <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Cantidad incorrecta",
                "Escribe una cantidad válida."
            )
            return

        stock = int(
            producto.get("cantidad", 0)
        )

        if cantidad > stock:
            messagebox.showwarning(
                "Stock insuficiente",
                (
                    f"Solo hay {stock} "
                    "unidad(es) disponibles."
                )
            )
            return

        cliente = clientes[
            indice_cliente
        ]

        tipo_venta = (
            variable_tipo_venta.get()
            .strip()
        )

        fecha_vencimiento = (
            entrada_vencimiento.get()
            .strip()
        )

        if tipo_venta == "A crédito":
            if not fecha_vencimiento:
                messagebox.showwarning(
                    "Fecha requerida",
                    (
                        "Escribe la fecha de vencimiento "
                        "para la venta a crédito."
                    )
                )
                return

            try:
                datetime.strptime(
                    fecha_vencimiento,
                    "%Y-%m-%d"
                )
            except ValueError:
                messagebox.showwarning(
                    "Fecha incorrecta",
                    (
                        "Usa el formato YYYY-MM-DD.\n"
                        "Ejemplo: 2026-09-30"
                    )
                )
                return

        precio = convertir_numero(
            producto.get("precio", 0)
        )

        costo = convertir_numero(
            producto.get("costo", 0)
        )

        total_venta = (
            cantidad * precio
        )

        costo_total = (
            cantidad * costo
        )

        ganancia_real = (
            total_venta - costo_total
        )

        ventas.append({
            "cliente": cliente.get(
                "nombre",
                ""
            ),
            "codigo_producto":
                producto.get(
                    "codigo",
                    ""
                ),
            "producto":
                producto.get(
                    "producto",
                    ""
                ),
            "cantidad": cantidad,
            "costo_unitario": costo,
            "precio_unitario": precio,
            "costo_total": costo_total,
            "monto": total_venta,
            "ganancia": ganancia_real,
            "tipo_pago": tipo_venta,
            "estado_pago": (
                "Pagada"
                if tipo_venta == "Pagada"
                else "Pendiente"
            ),
            "fecha": datetime.now().strftime(
                "%Y-%m-%d"
            )
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

        if tipo_venta == "A crédito":
            cuenta = {
                "id": datetime.now().strftime(
                    "%Y%m%d%H%M%S%f"
                ),
                "cliente": cliente.get(
                    "nombre",
                    ""
                ),
                "codigo_producto": producto.get(
                    "codigo",
                    ""
                ),
                "producto": producto.get(
                    "producto",
                    ""
                ),
                "cantidad": cantidad,
                "total": total_venta,
                "monto_pagado": 0,
                "saldo_pendiente": total_venta,
                "fecha_venta": datetime.now().strftime(
                    "%Y-%m-%d"
                ),
                "fecha_vencimiento": fecha_vencimiento,
                "estado": "Pendiente"
            }

            cuentas_por_cobrar.append(
                cuenta
            )

            guardar_cuentas(
                cuentas_por_cobrar
            )

        messagebox.showinfo(
            "Venta registrada",
            (
                "Venta registrada correctamente.\n\n"
                f"Código: "
                f"{producto.get('codigo', '')}\n"
                f"Producto: "
                f"{producto.get('producto', '')}\n"
                f"Cantidad: {cantidad}\n"
                f"Costo total: "
                f"${costo_total:.2f}\n"
                f"Total vendido: "
                f"${total_venta:.2f}\n"
                f"Ganancia real: "
                f"${ganancia_real:.2f}\n"
                f"Tipo de venta: {tipo_venta}"
                + (
                    f"\nVence: {fecha_vencimiento}"
                    if tipo_venta == "A crédito"
                    else ""
                )
            )
        )

        canvas_venta.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        contenido_venta,
        text="Guardar venta",
        width=18,
        command=guardar_venta
    ).pack(
        pady=15
    )

    def cerrar_ventana_venta():
        canvas_venta.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar_ventana_venta
    )

    aplicar_tema_ventas(
        v
    )

    entrada_busqueda.focus()


# ==================================================
# HISTORIAL DE VENTAS
# ==================================================

def abrir_historial_ventas():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Sales History"
    )

    v.geometry(
        "980x760"
    )

    v.minsize(
        820,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(26, 12)
    )

    tk.Label(
        encabezado,
        text=t("sales_history"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text="Search and review every registered transaction",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    panel_busqueda = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_busqueda.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Label(
        panel_busqueda,
        text=t("search_sales"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=18,
        pady=(14, 6)
    )

    variable_busqueda = tk.StringVar()

    entrada = tk.Entry(
        panel_busqueda,
        textvariable=variable_busqueda,
        font=("Segoe UI", 11),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        insertbackground=TEXTO,
        relief="flat",
        bd=0
    )

    entrada.pack(
        fill="x",
        padx=18,
        pady=(0, 14),
        ipady=8
    )

    panel_totales = tk.Frame(
        v,
        bg=FONDO
    )

    panel_totales.pack(
        fill="x",
        padx=30,
        pady=(0, 12)
    )

    etiquetas_totales = {}

    def crear_kpi(columna, titulo, clave, color):
        tarjeta = tk.Frame(
            panel_totales,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=90
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(
            False
        )

        panel_totales.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        cuerpo = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w"
        )

        valor = tk.Label(
            cuerpo,
            text="0",
            font=("Segoe UI", 16, "bold"),
            bg=PANEL,
            fg=TEXTO
        )

        valor.pack(
            anchor="w",
            pady=(5, 0)
        )

        etiquetas_totales[
            clave
        ] = valor

    crear_kpi(
        0,
        t("sales_found"),
        "cantidad",
        AZUL
    )

    crear_kpi(
        1,
        t("total_sold"),
        "total",
        VERDE
    )

    crear_kpi(
        2,
        t("known_profit"),
        "ganancia",
        "#22C55E"
    )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 15)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    def mostrar_historial(*args):
        for widget in contenido.winfo_children():
            widget.destroy()

        busqueda = (
            variable_busqueda.get()
            .strip()
            .lower()
        )

        encontradas = []
        total_filtrado = 0
        ganancia_filtrada = 0

        for indice_venta, venta in enumerate(ventas):
            cliente = str(
                venta.get(
                    "cliente",
                    ""
                )
            )

            codigo = str(
                venta.get(
                    "codigo_producto",
                    ""
                )
            )

            producto = str(
                venta.get(
                    "producto",
                    ""
                )
            )

            fecha = str(
                venta.get(
                    "fecha",
                    ""
                )
            )

            texto = (
                cliente.lower()
                + " "
                + codigo.lower()
                + " "
                + producto.lower()
                + " "
                + fecha.lower()
            )

            if (
                not busqueda
                or busqueda in texto
            ):
                encontradas.append(
                    (indice_venta, venta)
                )

        for numero, (indice_venta, venta) in enumerate(
            encontradas,
            start=1
        ):
            monto = convertir_numero(
                venta.get(
                    "monto",
                    0
                )
            )

            total_filtrado += monto

            tarjeta = tk.Frame(
                contenido,
                bg=PANEL_SECUNDARIO,
                highlightbackground=BORDE,
                highlightthickness=1
            )

            tarjeta.pack(
                fill="x",
                pady=6
            )

            cabecera = tk.Frame(
                tarjeta,
                bg=PANEL_SECUNDARIO
            )

            cabecera.pack(
                fill="x",
                padx=16,
                pady=(12, 6)
            )

            tk.Label(
                cabecera,
                text=f"SALE #{numero}",
                font=("Segoe UI", 10, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO
            ).pack(
                side="left"
            )

            tk.Label(
                cabecera,
                text=f"${monto:,.2f}",
                font=("Segoe UI", 11, "bold"),
                bg=PANEL_SECUNDARIO,
                fg=VERDE
            ).pack(
                side="right"
            )

            ganancia_texto = ""

            if "ganancia" in venta:
                ganancia = convertir_numero(
                    venta.get(
                        "ganancia",
                        0
                    )
                )

                ganancia_filtrada += ganancia

                ganancia_texto = (
                    f"\nKnown profit: ${ganancia:,.2f}"
                )

            detalle = (
                f"Client: {venta.get('cliente', '')}\n"
                f"Code: {venta.get('codigo_producto', '') or 'SIN CÓDIGO'}\n"
                f"Product: {venta.get('producto', '')}\n"
                f"Quantity: {venta.get('cantidad', 1)}\n"
                f"Date: {venta.get('fecha', '') or 'Sin fecha'}"
                f"{ganancia_texto}"
            )

            tk.Label(
                tarjeta,
                text=detalle,
                justify="left",
                font=("Segoe UI", 9),
                bg=PANEL_SECUNDARIO,
                fg=TEXTO_SECUNDARIO
            ).pack(
                anchor="w",
                padx=16,
                pady=(0, 8)
            )

            def generar_recibo(venta_actual=venta, indice_actual=indice_venta):
                try:
                    ruta = generar_recibo_pdf(
                        venta_actual,
                        clientes,
                        indice_actual,
                        obtener_idioma()
                    )
                    abrir_archivo(ruta)
                except Exception as error:
                    messagebox.showerror(
                        "Error al generar recibo" if obtener_idioma() == "es" else "Receipt generation error",
                        ("No se pudo generar el recibo PDF.\n\n" if obtener_idioma() == "es" else "The PDF receipt could not be generated.\n\n") + str(error)
                    )

            tk.Button(
                tarjeta,
                text="Generar recibo PDF" if obtener_idioma() == "es" else "Generate PDF receipt",
                command=generar_recibo,
                font=("Segoe UI", 9, "bold"),
                bg=AZUL,
                fg="white",
                activebackground="#2563EB",
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=14,
                pady=7
            ).pack(
                anchor="w",
                padx=16,
                pady=(0, 12)
            )

        etiquetas_totales[
            "cantidad"
        ].config(
            text=str(
                len(encontradas)
            )
        )

        etiquetas_totales[
            "total"
        ].config(
            text=f"${total_filtrado:,.2f}"
        )

        etiquetas_totales[
            "ganancia"
        ].config(
            text=f"${ganancia_filtrada:,.2f}"
        )

        canvas.yview_moveto(
            0
        )

    variable_busqueda.trace_add(
        "write",
        mostrar_historial
    )

    mostrar_historial()

    pie = tk.Frame(
        v,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )

    entrada.focus()


# ==================================================
# REPORTE DE GANANCIAS
# ==================================================

def abrir_reporte_ganancias():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    AMARILLO = "#F59E0B"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Profit Report"
    )

    v.geometry(
        "980x760"
    )

    v.minsize(
        820,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    ventas_con_costo = 0
    ventas_historicas = 0
    ingresos_conocidos = 0
    costos_conocidos = 0
    ganancia_total = 0
    resumen = {}

    for venta in ventas:
        if (
            "ganancia" not in venta
            or "costo_total" not in venta
        ):
            ventas_historicas += 1
            continue

        ventas_con_costo += 1

        codigo = venta.get(
            "codigo_producto",
            ""
        )

        producto = venta.get(
            "producto",
            "Sin producto"
        )

        cantidad = int(
            venta.get(
                "cantidad",
                0
            )
        )

        ingreso = convertir_numero(
            venta.get(
                "monto",
                0
            )
        )

        costo = convertir_numero(
            venta.get(
                "costo_total",
                0
            )
        )

        ganancia = convertir_numero(
            venta.get(
                "ganancia",
                0
            )
        )

        ingresos_conocidos += ingreso
        costos_conocidos += costo
        ganancia_total += ganancia

        clave = (
            codigo
            if codigo
            else producto
        )

        if clave not in resumen:
            resumen[
                clave
            ] = {
                "codigo": codigo,
                "producto": producto,
                "cantidad": 0,
                "ingresos": 0,
                "costos": 0,
                "ganancia": 0
            }

        resumen[
            clave
        ]["cantidad"] += cantidad

        resumen[
            clave
        ]["ingresos"] += ingreso

        resumen[
            clave
        ]["costos"] += costo

        resumen[
            clave
        ]["ganancia"] += ganancia

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(26, 14)
    )

    tk.Label(
        encabezado,
        text=t("profit_analytics"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text="Known revenue, cost and profitability overview",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    kpis = tk.Frame(
        v,
        bg=FONDO
    )

    kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    datos_kpi = [
        (
            t("known_revenue"),
            f"${ingresos_conocidos:,.2f}",
            AZUL
        ),
        (
            t("known_costs"),
            f"${costos_conocidos:,.2f}",
            AMARILLO
        ),
        (
            t("known_profit"),
            f"${ganancia_total:,.2f}",
            VERDE
        )
    ]

    for columna, (
        titulo,
        valor,
        color
    ) in enumerate(datos_kpi):
        tarjeta = tk.Frame(
            kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=95
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(
            False
        )

        kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        cuerpo = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w"
        )

        tk.Label(
            cuerpo,
            text=valor,
            font=("Segoe UI", 17, "bold"),
            bg=PANEL,
            fg=TEXTO
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 14)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    productos_ordenados = sorted(
        resumen.values(),
        key=lambda x: x[
            "ganancia"
        ],
        reverse=True
    )

    if not productos_ordenados:
        tk.Label(
            contenido,
            text="No known-cost sales available yet.",
            font=("Segoe UI", 10),
            bg=FONDO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            pady=15
        )

    for numero, datos in enumerate(
        productos_ordenados,
        start=1
    ):
        tarjeta = tk.Frame(
            contenido,
            bg=PANEL_SECUNDARIO,
            highlightbackground=BORDE,
            highlightthickness=1
        )

        tarjeta.pack(
            fill="x",
            pady=6
        )

        cabecera = tk.Frame(
            tarjeta,
            bg=PANEL_SECUNDARIO
        )

        cabecera.pack(
            fill="x",
            padx=16,
            pady=(12, 6)
        )

        tk.Label(
            cabecera,
            text=(
                f"{numero:02d}  "
                f"{datos['producto']}"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO
        ).pack(
            side="left"
        )

        tk.Label(
            cabecera,
            text=(
                f"${datos['ganancia']:,.2f}"
            ),
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=VERDE
        ).pack(
            side="right"
        )

        detalle = (
            f"Code: {datos['codigo'] or 'SIN CÓDIGO'}\n"
            f"Units sold: {datos['cantidad']}\n"
            f"Revenue: ${datos['ingresos']:,.2f}\n"
            f"Cost of goods sold: ${datos['costos']:,.2f}"
        )

        tk.Label(
            tarjeta,
            text=detalle,
            justify="left",
            font=("Segoe UI", 9),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

    if ventas_historicas > 0:
        alerta = tk.Frame(
            contenido,
            bg=PANEL,
            highlightbackground=AMARILLO,
            highlightthickness=1
        )

        alerta.pack(
            fill="x",
            pady=(10, 5)
        )

        tk.Label(
            alerta,
            text=(
                f"IMPORTANT: {ventas_historicas} historical sale(s) "
                "do not have cost data and are excluded from known profit."
            ),
            font=("Segoe UI", 9, "bold"),
            wraplength=820,
            justify="left",
            bg=PANEL,
            fg=AMARILLO
        ).pack(
            anchor="w",
            padx=16,
            pady=12
        )

    pie = tk.Frame(
        v,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    tk.Label(
        pie,
        text=(
            f"Sales with registered cost: "
            f"{ventas_con_costo}"
        ),
        font=("Segoe UI", 9),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        side="left"
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )


# ==================================================
# VENTAS
# ==================================================

def abrir_ventas():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Sales"
    )

    v.geometry(
        "1000x760"
    )

    v.minsize(
        820,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    total_ventas = 0
    ganancia_conocida = 0

    for venta in ventas:
        total_ventas += convertir_numero(
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

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 15)
    )

    tk.Label(
        encabezado,
        text=t("sales_management"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=t("sales_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    acciones = tk.Frame(
        v,
        bg=FONDO
    )

    acciones.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    tk.Button(
        acciones,
        text=t("new_sale"),
        command=abrir_registro_venta,
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=9
    ).pack(
        side="left"
    )

    tk.Button(
        acciones,
        text=t("sales_history"),
        command=abrir_historial_ventas,
        font=("Segoe UI", 10, "bold"),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=9
    ).pack(
        side="left",
        padx=(10, 0)
    )

    tk.Button(
        acciones,
        text=t("profit_analytics"),
        command=abrir_reporte_ganancias,
        font=("Segoe UI", 10, "bold"),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=9
    ).pack(
        side="left",
        padx=(10, 0)
    )

    kpis = tk.Frame(
        v,
        bg=FONDO
    )

    kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    datos_kpi = [
        (
            t("total_sales"),
            f"${total_ventas:,.2f}",
            AZUL
        ),
        (
            t("known_profit"),
            f"${ganancia_conocida:,.2f}",
            VERDE
        ),
        (
            t("transactions"),
            str(
                len(ventas)
            ),
            "#06B6D4"
        )
    ]

    for columna, (
        titulo,
        valor,
        color
    ) in enumerate(datos_kpi):
        tarjeta = tk.Frame(
            kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=95
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(
            False
        )

        kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        cuerpo = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w"
        )

        tk.Label(
            cuerpo,
            text=valor,
            font=("Segoe UI", 17, "bold"),
            bg=PANEL,
            fg=TEXTO
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 15)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    if not ventas:
        tk.Label(
            contenido,
            text="No sales registered yet.",
            font=("Segoe UI", 10),
            bg=FONDO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            pady=15
        )

    for numero, venta in enumerate(
        ventas,
        start=1
    ):
        monto = convertir_numero(
            venta.get(
                "monto",
                0
            )
        )

        tarjeta = tk.Frame(
            contenido,
            bg=PANEL_SECUNDARIO,
            highlightbackground=BORDE,
            highlightthickness=1
        )

        tarjeta.pack(
            fill="x",
            pady=6
        )

        cabecera = tk.Frame(
            tarjeta,
            bg=PANEL_SECUNDARIO
        )

        cabecera.pack(
            fill="x",
            padx=16,
            pady=(12, 6)
        )

        tk.Label(
            cabecera,
            text=f"SALE #{numero:02d}",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO
        ).pack(
            side="left"
        )

        tk.Label(
            cabecera,
            text=f"${monto:,.2f}",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=VERDE
        ).pack(
            side="right"
        )

        detalle = (
            f"Client: {venta.get('cliente', '')}\n"
            f"Product: {venta.get('producto', '')}\n"
            f"Code: {venta.get('codigo_producto', '') or 'SIN CÓDIGO'}\n"
            f"Quantity: {venta.get('cantidad', 1)}\n"
            f"Date: {venta.get('fecha', '') or 'Sin fecha'}"
        )

        tk.Label(
            tarjeta,
            text=detalle,
            justify="left",
            font=("Segoe UI", 9),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

    pie = tk.Frame(
        v,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )

        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(
        side="right"
    )

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )


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
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Expense"
    )

    v.geometry(
        "650x520"
    )

    v.minsize(
        580,
        470
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 16)
    )

    tk.Label(
        encabezado,
        text=t("register_expense"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    tk.Label(
        encabezado,
        text=t("expense_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    panel = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    tk.Label(
        panel,
        text=t("description"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=22,
        pady=(22, 6)
    )

    descripcion = tk.Entry(
        panel,
        font=("Segoe UI", 11),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        insertbackground=TEXTO,
        relief="flat",
        bd=0
    )

    descripcion.pack(
        fill="x",
        padx=22,
        ipady=8
    )

    tk.Label(
        panel,
        text=t("category"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=22,
        pady=(16, 6)
    )

    categorias = (
        [
            "Transporte",
            "Herramientas",
            "Publicidad",
            "Renta",
            "Servicios",
            "Otros"
        ]
        if obtener_idioma() == "es"
        else
        [
            "Transportation",
            "Tools",
            "Advertising",
            "Rent",
            "Services",
            "Other"
        ]
    )

    categoria = ttk.Combobox(
        panel,
        values=categorias,
        state="readonly"
    )

    categoria.pack(
        fill="x",
        padx=22
    )

    tk.Label(
        panel,
        text=t("amount"),
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=22,
        pady=(16, 6)
    )

    monto = tk.Entry(
        panel,
        font=("Segoe UI", 11),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        insertbackground=TEXTO,
        relief="flat",
        bd=0
    )

    monto.pack(
        fill="x",
        padx=22,
        ipady=8
    )

    botones = tk.Frame(
        panel,
        bg=PANEL
    )

    botones.pack(
        fill="x",
        padx=22,
        pady=22
    )

    tk.Button(
        botones,
        text=t("save_expense"),
        command=lambda:
        registrar_gasto(
            descripcion,
            categoria,
            monto,
            v
        ),
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=9
    ).pack(side="left")

    tk.Button(
        botones,
        text=t("cancel"),
        command=v.destroy,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=9
    ).pack(side="right")

    descripcion.focus()


def abrir_gastos():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    ROJO = "#EF4444"
    CYAN = "#06B6D4"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Expenses"
    )

    v.geometry(
        "980x760"
    )

    v.minsize(
        820,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(
        bg=FONDO
    )

    total = sum(
        convertir_numero(
            gasto.get(
                "monto",
                0
            )
        )
        for gasto in gastos
    )

    encabezado = tk.Frame(v, bg=FONDO)
    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 14)
    )

    tk.Label(
        encabezado,
        text=t("expense_management"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    tk.Label(
        encabezado,
        text=t("expense_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    acciones = tk.Frame(v, bg=FONDO)
    acciones.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Button(
        acciones,
        text=t("new_expense"),
        command=abrir_registro_gasto,
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=9
    ).pack(side="left")

    kpis = tk.Frame(v, bg=FONDO)
    kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    datos_kpi = [
        (
            t("total_expenses"),
            f"${total:,.2f}",
            ROJO
        ),
        (
            t("expense_count"),
            str(len(gastos)),
            CYAN
        )
    ]

    for columna, (titulo, valor, color) in enumerate(
        datos_kpi
    ):
        tarjeta = tk.Frame(
            kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=95
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(False)
        kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        cuerpo = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(anchor="w")

        tk.Label(
            cuerpo,
            text=valor,
            font=("Segoe UI", 17, "bold"),
            bg=PANEL,
            fg=TEXTO
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 14)
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    for numero, gasto in enumerate(
        gastos,
        start=1
    ):
        monto = convertir_numero(
            gasto.get(
                "monto",
                0
            )
        )

        tarjeta = tk.Frame(
            contenido,
            bg=PANEL_SECUNDARIO,
            highlightbackground=BORDE,
            highlightthickness=1
        )

        tarjeta.pack(
            fill="x",
            pady=6
        )

        cabecera = tk.Frame(
            tarjeta,
            bg=PANEL_SECUNDARIO
        )

        cabecera.pack(
            fill="x",
            padx=16,
            pady=(12, 6)
        )

        tk.Label(
            cabecera,
            text=(
                f"EXPENSE #{numero:02d}"
                if obtener_idioma() == "en"
                else f"GASTO #{numero:02d}"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO
        ).pack(side="left")

        tk.Label(
            cabecera,
            text=f"${monto:,.2f}",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_SECUNDARIO,
            fg=ROJO
        ).pack(side="right")

        detalle = (
            f"{t('description')}: "
            f"{gasto.get('descripcion', gasto.get('concepto', ''))}\n"
            f"{t('category')}: "
            f"{gasto.get('categoria', '')}"
        )

        tk.Label(
            tarjeta,
            text=detalle,
            justify="left",
            font=("Segoe UI", 9),
            bg=PANEL_SECUNDARIO,
            fg=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )

    pie = tk.Frame(v, bg=FONDO)
    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )
        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(side="right")

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )


# ==================================================
# RESUMEN
# ==================================================

def abrir_resumen():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    ROJO = "#EF4444"
    CYAN = "#06B6D4"
    AMARILLO = "#F59E0B"

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Business Summary"
    )

    v.geometry(
        "1050x780"
    )

    v.minsize(
        850,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(bg=FONDO)

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

    ganancia_real_conocida = sum(
        convertir_numero(
            venta.get("ganancia", 0)
        )
        for venta in ventas
        if "ganancia" in venta
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
        estado = t("positive")
        color_estado = VERDE

    elif flujo < 0:
        estado = t("negative")
        color_estado = ROJO

    else:
        estado = t("balanced")
        color_estado = AMARILLO

    marco_scroll = tk.Frame(v, bg=FONDO)
    marco_scroll.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    encabezado = tk.Frame(
        contenido,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 15)
    )

    tk.Label(
        encabezado,
        text=t("business_summary_title"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    tk.Label(
        encabezado,
        text=t("business_summary_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    kpis = tk.Frame(
        contenido,
        bg=FONDO
    )

    kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    datos_kpi = [
        (
            t("sales_revenue"),
            f"${ingresos:,.2f}",
            AZUL
        ),
        (
            t("known_profit"),
            f"${ganancia_real_conocida:,.2f}",
            VERDE
        ),
        (
            t("operating_expenses"),
            f"${gastos_totales:,.2f}",
            ROJO
        ),
        (
            t("cash_flow"),
            f"${flujo:,.2f}",
            CYAN
        )
    ]

    for columna, (titulo, valor, color) in enumerate(
        datos_kpi
    ):
        tarjeta = tk.Frame(
            kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=100
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(False)
        kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        cuerpo = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(anchor="w")

        tk.Label(
            cuerpo,
            text=valor,
            font=("Segoe UI", 16, "bold"),
            bg=PANEL,
            fg=TEXTO
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    panel_general = tk.Frame(
        contenido,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_general.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Label(
        panel_general,
        text=t("financial_status"),
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(16, 10)
    )

    resumen_texto = (
        f"{t('registered_clients')}: {len(clientes)}\n"
        f"{t('registered_sales')}: {len(ventas)}\n"
        f"{t('financial_status')}: {estado}"
    )

    tk.Label(
        panel_general,
        text=resumen_texto,
        justify="left",
        font=("Segoe UI", 10),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=20,
        pady=(0, 16)
    )

    tk.Label(
        panel_general,
        text=estado,
        font=("Segoe UI", 14, "bold"),
        bg=PANEL,
        fg=color_estado
    ).pack(
        anchor="e",
        padx=20,
        pady=(0, 16)
    )

    panel_inv = tk.Frame(
        contenido,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_inv.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Label(
        panel_inv,
        text=t("inventory_position"),
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(16, 10)
    )

    tk.Label(
        panel_inv,
        text=(
            f"{t('inventory_capital')}: ${capital:,.2f}\n"
            f"{t('inventory_value')}: ${valor_venta:,.2f}\n"
            f"{t('potential_profit')}: ${ganancia_potencial:,.2f}"
        ),
        justify="left",
        font=("Segoe UI", 10),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        padx=20,
        pady=(0, 16)
    )

    pie = tk.Frame(
        contenido,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 25)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )
        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(side="right")

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )


# ==================================================
# DIAGNÓSTICO
# ==================================================

def abrir_diagnostico():
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    ROJO = "#EF4444"
    AMARILLO = "#F59E0B"

    resultado = calcular_diagnostico(
        ventas,
        inventario,
        reposiciones,
        gastos
    )

    v = tk.Toplevel(ventana)

    v.title(
        "AI Business Assistant - Diagnosis"
    )

    v.geometry(
        "1050x780"
    )

    v.minsize(
        850,
        620
    )

    v.resizable(
        True,
        True
    )

    v.configure(bg=FONDO)

    marco_scroll = tk.Frame(
        v,
        bg=FONDO
    )

    marco_scroll.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        marco_scroll,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        marco_scroll,
        orient="vertical",
        command=canvas.yview
    )

    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(
            ventana_canvas,
            width=e.width
        )
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

    def mover_rueda(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mover_rueda
    )

    encabezado = tk.Frame(
        contenido,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=30,
        pady=(28, 15)
    )

    tk.Label(
        encabezado,
        text=t("diagnosis_title"),
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    tk.Label(
        encabezado,
        text=t("diagnosis_subtitle"),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    flujo = resultado[
        "flujo_neto"
    ]

    estado_original = str(
        resultado[
            "estado_flujo"
        ]
    ).upper()

    if "POSIT" in estado_original:
        estado = t("positive")
        color_estado = VERDE
    elif "NEGAT" in estado_original:
        estado = t("negative")
        color_estado = ROJO
    else:
        estado = t("balanced")
        color_estado = AMARILLO

    kpis = tk.Frame(
        contenido,
        bg=FONDO
    )

    kpis.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    datos_kpi = [
        (
            t("cash_flow"),
            f"${flujo:,.2f}",
            AZUL
        ),
        (
            t("financial_status"),
            estado,
            color_estado
        ),
        (
            t("potential_profit"),
            f"${resultado['ganancia_potencial']:,.2f}",
            VERDE
        ),
        (
            t("expense_ratio"),
            f"{resultado['porcentaje_gastos']:.2f}%",
            AMARILLO
        )
    ]

    for columna, (titulo, valor, color) in enumerate(
        datos_kpi
    ):
        tarjeta = tk.Frame(
            kpis,
            bg=PANEL,
            highlightbackground=BORDE,
            highlightthickness=1,
            height=100
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        tarjeta.grid_propagate(False)
        kpis.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Frame(
            tarjeta,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        cuerpo = tk.Frame(
            tarjeta,
            bg=PANEL
        )

        cuerpo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        tk.Label(
            cuerpo,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).pack(anchor="w")

        tk.Label(
            cuerpo,
            text=valor,
            font=("Segoe UI", 16, "bold"),
            bg=PANEL,
            fg=TEXTO
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    panel_analisis = tk.Frame(
        contenido,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_analisis.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Label(
        panel_analisis,
        text=t("analysis"),
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(16, 10)
    )

    for mensaje in resultado[
        "diagnosticos"
    ]:
        tk.Label(
            panel_analisis,
            text=mensaje,
            font=("Segoe UI", 10),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO,
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

    tk.Frame(
        panel_analisis,
        bg=PANEL,
        height=10
    ).pack()

    panel_recomendacion = tk.Frame(
        contenido,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_recomendacion.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )

    tk.Label(
        panel_recomendacion,
        text=t("recommendation"),
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=20,
        pady=(16, 10)
    )

    tk.Label(
        panel_recomendacion,
        text=resultado["recomendacion"],
        font=("Segoe UI", 10),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO,
        wraplength=900,
        justify="left"
    ).pack(
        anchor="w",
        padx=20,
        pady=(0, 16)
    )

    pie = tk.Frame(
        contenido,
        bg=FONDO
    )

    pie.pack(
        fill="x",
        padx=30,
        pady=(0, 25)
    )

    def cerrar():
        canvas.unbind_all(
            "<MouseWheel>"
        )
        v.destroy()

    tk.Button(
        pie,
        text=t("close"),
        command=cerrar,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        activebackground=BORDE,
        activeforeground=TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(side="right")

    v.protocol(
        "WM_DELETE_WINDOW",
        cerrar
    )


# ==================================================
# VENTANA PRINCIPAL
# ==================================================

ventana = tk.Tk()

ventana.title(
    "AI Business Assistant"
)

ventana.geometry(
    "1280x840"
)

ventana.minsize(
    1100,
    700
)

ventana.configure(
    bg="#0B1220"
)

# ==================================================
# PANEL PRINCIPAL PROFESIONAL
# ==================================================

barra_lateral = tk.Frame(
    ventana,
    bg="#111C2E",
    width=235
)

barra_lateral.pack(
    side="left",
    fill="y"
)

barra_lateral.pack_propagate(
    False
)

contenido_principal = tk.Frame(
    ventana,
    bg="#0B1220"
)

contenido_principal.pack(
    side="right",
    fill="both",
    expand=True
)

tk.Label(
    barra_lateral,
    text="AI BUSINESS\nASSISTANT",
    font=("Segoe UI", 18, "bold"),
    bg="#111C2E",
    fg="#F4F7FB",
    justify="left"
).pack(
    anchor="w",
    padx=20,
    pady=(28, 8)
)

etiqueta_management = tk.Label(
    barra_lateral,
    text="Executive Management",
    font=("Segoe UI", 9),
    bg="#111C2E",
    fg="#8FA3BF"
)

etiqueta_management.pack(
    anchor="w",
    padx=20,
    pady=(0, 20)
)

botones_menu = {}


def abrir_desde_menu(comando):
    comando()


def crear_boton_menu(
    clave,
    comando
):
    boton = tk.Button(
        barra_lateral,
        text=t(clave),
        command=lambda: abrir_desde_menu(
            comando
        ),
        anchor="w",
        padx=18,
        font=("Segoe UI", 10, "bold"),
        bg="#111C2E",
        fg="#DCE6F5",
        activebackground="#162238",
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        cursor="hand2",
        height=2
    )

    boton.pack(
        fill="x",
        padx=10,
        pady=3
    )

    botones_menu[
        clave
    ] = boton


crear_boton_menu(
    "dashboard",
    lambda: abrir_dashboard_profesional(
        ventana
    )
)

crear_boton_menu(
    "clientes",
    abrir_clientes
)

crear_boton_menu(
    "ventas",
    abrir_ventas
)

crear_boton_menu(
    "inventario",
    abrir_inventario
)

crear_boton_menu(
    "gastos",
    abrir_gastos
)

crear_boton_menu(
    "cuentas_por_cobrar",
    lambda: abrir_cuentas_por_cobrar(
        ventana
    )
)

crear_boton_menu(
    "resumen_negocio",
    abrir_resumen
)

crear_boton_menu(
    "diagnostico",
    abrir_diagnostico
)

boton_configuracion_negocio = tk.Button(
    barra_lateral,
    text=(
        "Business Settings"
        if obtener_idioma() == "en"
        else "Configuración del negocio"
    ),
    command=lambda: abrir_configuracion_negocio(
        ventana
    ),
    anchor="w",
    padx=18,
    font=("Segoe UI", 10, "bold"),
    bg="#111C2E",
    fg="#DCE6F5",
    activebackground="#162238",
    activeforeground="#FFFFFF",
    relief="flat",
    bd=0,
    cursor="hand2",
    height=2
)

boton_configuracion_negocio.pack(
    fill="x",
    padx=10,
    pady=3
)

# ==================================================
# SELECTOR DE IDIOMA
# ==================================================

separador_idioma = tk.Frame(
    barra_lateral,
    bg="#24344D",
    height=1
)

separador_idioma.pack(
    fill="x",
    padx=15,
    pady=(18, 12)
)

etiqueta_idioma = tk.Label(
    barra_lateral,
    text=t("idioma"),
    font=("Segoe UI", 9, "bold"),
    bg="#111C2E",
    fg="#8FA3BF"
)

etiqueta_idioma.pack(
    anchor="w",
    padx=20,
    pady=(0, 6)
)

selector_idioma = ttk.Combobox(
    barra_lateral,
    values=[
        "Español",
        "English"
    ],
    state="readonly",
    width=20
)

selector_idioma.pack(
    padx=18,
    pady=(0, 12)
)

if obtener_idioma() == "en":
    selector_idioma.set(
        "English"
    )
else:
    selector_idioma.set(
        "Español"
    )

tk.Frame(
    barra_lateral,
    bg="#24344D",
    height=1
).pack(
    fill="x",
    padx=15,
    pady=(6, 12)
)

boton_salir = tk.Button(
    barra_lateral,
    text=t("salir"),
    command=ventana.destroy,
    anchor="w",
    padx=18,
    font=("Segoe UI", 10, "bold"),
    bg="#111C2E",
    fg="#EF4444",
    activebackground="#162238",
    activeforeground="#EF4444",
    relief="flat",
    bd=0,
    cursor="hand2",
    height=2
)

boton_salir.pack(
    fill="x",
    padx=10,
    pady=3
)


# ==================================================
# CONTENIDO DE INICIO
# ==================================================

encabezado = tk.Frame(
    contenido_principal,
    bg="#0B1220"
)

encabezado.pack(
    fill="x",
    padx=35,
    pady=(30, 15)
)

etiqueta_overview = tk.Label(
    encabezado,
    text=t("executive_overview"),
    font=("Segoe UI", 22, "bold"),
    bg="#0B1220",
    fg="#F4F7FB"
)

etiqueta_overview.pack(
    anchor="w"
)

etiqueta_business_overview = tk.Label(
    encabezado,
    text=t("business_overview"),
    font=("Segoe UI", 10),
    bg="#0B1220",
    fg="#8FA3BF"
)

etiqueta_business_overview.pack(
    anchor="w",
    pady=(4, 0)
)

marco_inicio = tk.Frame(
    contenido_principal,
    bg="#111C2E",
    highlightbackground="#24344D",
    highlightthickness=1
)

marco_inicio.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=(0, 35)
)

etiqueta_dashboard_inicio = tk.Label(
    marco_inicio,
    text="Financial Dashboard",
    font=("Segoe UI", 20, "bold"),
    bg="#111C2E",
    fg="#F4F7FB"
)

etiqueta_dashboard_inicio.pack(
    pady=(45, 10)
)

etiqueta_descripcion_dashboard = tk.Label(
    marco_inicio,
    text="",
    font=("Segoe UI", 11),
    bg="#111C2E",
    fg="#8FA3BF",
    wraplength=650,
    justify="center"
)

etiqueta_descripcion_dashboard.pack(
    pady=(0, 25)
)

boton_dashboard_inicio = tk.Button(
    marco_inicio,
    text=t("open_dashboard"),
    command=lambda: abrir_dashboard_profesional(
        ventana
    ),
    font=("Segoe UI", 11, "bold"),
    bg="#3B82F6",
    fg="white",
    activebackground="#2563EB",
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=30,
    pady=12
)

boton_dashboard_inicio.pack()


def actualizar_textos_principales():
    for clave, boton in (
        botones_menu.items()
    ):
        boton.config(
            text=t(clave)
        )

    etiqueta_idioma.config(
        text=t("idioma")
    )

    boton_salir.config(
        text=t("salir")
    )

    boton_configuracion_negocio.config(
        text=(
            "Business Settings"
            if obtener_idioma() == "en"
            else "Configuración del negocio"
        )
    )

    etiqueta_overview.config(
        text=t(
            "executive_overview"
        )
    )

    etiqueta_business_overview.config(
        text=t(
            "business_overview"
        )
    )

    boton_dashboard_inicio.config(
        text=t(
            "open_dashboard"
        )
    )

    if obtener_idioma() == "es":
        etiqueta_management.config(
            text="Gestión Ejecutiva"
        )

        etiqueta_dashboard_inicio.config(
            text="Dashboard Financiero"
        )

        etiqueta_descripcion_dashboard.config(
            text=(
                "Abrí el Dashboard ejecutivo para ver "
                "ventas, ganancias, cuentas por cobrar, "
                "inventario, flujo de caja y alertas."
            )
        )

    else:
        etiqueta_management.config(
            text="Executive Management"
        )

        etiqueta_dashboard_inicio.config(
            text="Financial Dashboard"
        )

        etiqueta_descripcion_dashboard.config(
            text=(
                "Open the executive dashboard to review "
                "sales, profit, accounts receivable, "
                "inventory, cash flow and alerts."
            )
        )


def seleccionar_idioma(event=None):
    seleccion = selector_idioma.get()

    if seleccion == "English":
        cambiar_idioma(
            "en"
        )
    else:
        cambiar_idioma(
            "es"
        )

    actualizar_textos_principales()


selector_idioma.bind(
    "<<ComboboxSelected>>",
    seleccionar_idioma
)

actualizar_textos_principales()

ventana.mainloop()
