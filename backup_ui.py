import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

from backup import (
    crear_respaldo,
    listar_respaldos,
    restaurar_respaldo,
)


def abrir_backup(ventana_padre=None):
    FONDO = "#0B1220"
    PANEL = "#111C2E"
    PANEL_SECUNDARIO = "#162238"
    BORDE = "#24344D"
    TEXTO = "#F4F7FB"
    TEXTO_SECUNDARIO = "#8FA3BF"
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    ROJO = "#EF4444"

    if ventana_padre is None:
        v = tk.Tk()
    else:
        v = tk.Toplevel(ventana_padre)

    v.title(
        "AI Business Assistant - Backup"
    )

    v.geometry("850x650")
    v.minsize(720, 560)
    v.configure(bg=FONDO)

    # ==============================================
    # ENCABEZADO
    # ==============================================

    encabezado = tk.Frame(
        v,
        bg=FONDO
    )

    encabezado.pack(
        fill="x",
        padx=35,
        pady=(30, 18)
    )

    tk.Label(
        encabezado,
        text="RESPALDO DE DATOS",
        font=("Segoe UI", 23, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(
        anchor="w"
    )

    tk.Label(
        encabezado,
        text=(
            "Protegé la información de tu negocio "
            "creando copias de seguridad."
        ),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    # ==============================================
    # PANEL CREAR RESPALDO
    # ==============================================

    panel_crear = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_crear.pack(
        fill="x",
        padx=35,
        pady=(0, 18)
    )

    tk.Label(
        panel_crear,
        text="CREAR NUEVO RESPALDO",
        font=("Segoe UI", 13, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        anchor="w",
        padx=22,
        pady=(18, 5)
    )

    tk.Label(
        panel_crear,
        text=(
            "Guarda clientes, ventas, inventario, "
            "gastos, cuentas por cobrar, reposiciones "
            "y configuración del negocio."
        ),
        font=("Segoe UI", 10),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO,
        wraplength=720,
        justify="left"
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 15)
    )

    # ==============================================
    # PANEL RESPALDOS
    # ==============================================

    panel_respaldos = tk.Frame(
        v,
        bg=PANEL,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    panel_respaldos.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=(0, 20)
    )

    cabecera_lista = tk.Frame(
        panel_respaldos,
        bg=PANEL
    )

    cabecera_lista.pack(
        fill="x",
        padx=22,
        pady=(18, 10)
    )

    tk.Label(
        cabecera_lista,
        text="RESPALDOS DISPONIBLES",
        font=("Segoe UI", 13, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(
        side="left"
    )

    etiqueta_total = tk.Label(
        cabecera_lista,
        text="0 respaldos",
        font=("Segoe UI", 9),
        bg=PANEL,
        fg=TEXTO_SECUNDARIO
    )

    etiqueta_total.pack(
        side="right"
    )

    marco_lista = tk.Frame(
        panel_respaldos,
        bg=PANEL
    )

    marco_lista.pack(
        fill="both",
        expand=True,
        padx=22,
        pady=(0, 12)
    )

    scrollbar = tk.Scrollbar(
        marco_lista,
        orient="vertical"
    )

    lista_respaldos = tk.Listbox(
        marco_lista,
        font=("Segoe UI", 10),
        bg=PANEL_SECUNDARIO,
        fg=TEXTO,
        selectbackground=AZUL,
        selectforeground="white",
        highlightbackground=BORDE,
        highlightthickness=1,
        relief="flat",
        bd=0,
        activestyle="none",
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(
        command=lista_respaldos.yview
    )

    lista_respaldos.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    respaldos_actuales = []

    def actualizar_lista():
        nonlocal respaldos_actuales

        respaldos_actuales = (
            listar_respaldos()
        )

        lista_respaldos.delete(
            0,
            tk.END
        )

        for respaldo in respaldos_actuales:
            nombre = respaldo.name

            texto = nombre.replace(
                "backup_",
                ""
            )

            texto = texto.replace(
                "_",
                " "
            )

            lista_respaldos.insert(
                tk.END,
                texto
            )

        cantidad = len(
            respaldos_actuales
        )

        etiqueta_total.config(
            text=(
                f"{cantidad} respaldo"
                if cantidad == 1
                else f"{cantidad} respaldos"
            )
        )

    def crear_nuevo_respaldo():
        try:
            resultado = crear_respaldo()

            actualizar_lista()

            messagebox.showinfo(
                "Respaldo completado",
                (
                    "El respaldo fue creado "
                    "correctamente.\n\n"
                    f"Archivos guardados: "
                    f"{len(resultado['archivos_copiados'])}\n\n"
                    f"Ubicación:\n"
                    f"{resultado['carpeta']}"
                ),
                parent=v
            )

        except Exception as error:
            messagebox.showerror(
                "Error de respaldo",
                (
                    "No fue posible crear "
                    "el respaldo.\n\n"
                    f"{error}"
                ),
                parent=v
            )

    def restaurar_seleccionado():
        seleccion = (
            lista_respaldos.curselection()
        )

        if not seleccion:
            messagebox.showwarning(
                "Seleccioná un respaldo",
                (
                    "Primero seleccioná el respaldo "
                    "que querés restaurar."
                ),
                parent=v
            )
            return

        indice = seleccion[0]

        respaldo = (
            respaldos_actuales[indice]
        )

        confirmar = messagebox.askyesno(
            "Confirmar restauración",
            (
                "¿Estás seguro de que querés "
                "restaurar este respaldo?\n\n"
                f"{respaldo.name}\n\n"
                "Los datos actuales serán "
                "reemplazados por los datos "
                "guardados en este respaldo."
            ),
            parent=v
        )

        if not confirmar:
            return

        try:
            resultado = restaurar_respaldo(
                respaldo
            )

            messagebox.showinfo(
                "Restauración completada",
                (
                    "Los datos fueron restaurados "
                    "correctamente.\n\n"
                    f"Archivos restaurados: "
                    f"{len(resultado['archivos_restaurados'])}\n\n"
                    "Cerrá y volvé a abrir la "
                    "aplicación para cargar "
                    "los datos restaurados."
                ),
                parent=v
            )

        except Exception as error:
            messagebox.showerror(
                "Error de restauración",
                (
                    "No fue posible restaurar "
                    "el respaldo.\n\n"
                    f"{error}"
                ),
                parent=v
            )

    # ==============================================
    # BOTONES
    # ==============================================

    tk.Button(
        panel_crear,
        text="Crear respaldo ahora",
        command=crear_nuevo_respaldo,
        font=("Segoe UI", 10, "bold"),
        bg=AZUL,
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=10
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 20)
    )

    marco_botones = tk.Frame(
        panel_respaldos,
        bg=PANEL
    )

    marco_botones.pack(
        fill="x",
        padx=22,
        pady=(0, 18)
    )

    tk.Button(
        marco_botones,
        text="Restaurar respaldo seleccionado",
        command=restaurar_seleccionado,
        font=("Segoe UI", 10, "bold"),
        bg=VERDE,
        fg="white",
        activebackground="#16A34A",
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
        marco_botones,
        text="Cerrar",
        command=v.destroy,
        font=("Segoe UI", 10),
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
        side="right"
    )

    actualizar_lista()

    if ventana_padre is None:
        v.mainloop()


if __name__ == "__main__":
    abrir_backup()