# Autor: Soriano Josue Lautaro

import flet as ft

precios_procesadores = {
    "Intel Core i3-12100": 120000,
    "AMD Ryzen 5 5600G": 180000,
    "Intel Core i7-13700K": 350000,
    "AMD Ryzen 7 7800X3D": 450000
}
consumo_cpu = {
    "Intel Core i3-12100": 60,
    "AMD Ryzen 5 5600G": 65,
    "Intel Core i7-13700K": 125,
    "AMD Ryzen 7 7800X3D": 120
}

def main(page: ft.Page):
    page.title = "Tienda de informática"
    page.scroll = "auto"

    campo_nombre = ft.TextField(label="Ingrese su Nombre")
    campo_presupuesto = ft.TextField(
        label="Ingrese el tope del presupuesto (En pesos)"
    )

    dropdown_procesador = ft.Dropdown(
        label="Seleccione un procesador",
        options=[
            ft.dropdown.Option("Intel Core i3-12100"),
            ft.dropdown.Option("AMD Ryzen 5 5600G"),
            ft.dropdown.Option("Intel Core i7-13700K"),
            ft.dropdown.Option("AMD Ryzen 7 7800X3D")
        ]
    )

    texto_ram = ft.Text(
        value="Cantidad de RAM elegida: 8 GB",
        size=20
    )

    def cambiar_slider(e):
        valor_real = 2 ** int(e.control.value)
        texto_ram.value = f"Cantidad de RAM elegida: {valor_real} GB"
        page.update()

    ram = ft.Slider(
        label="{value}",
        min=3,
        max=6,
        value=3,
        divisions=3,
        on_change=cambiar_slider
    )

    gpu = ft.Checkbox(label="Placa de video dedicada")
    ssd = ft.Checkbox(label="Unidad SSD extra")
    armado = ft.Checkbox(label="Servicio de armado")

    optativos = ft.Column(
        controls=[gpu, ssd, armado]
    )

    modalidad = ft.Text("Seleccionado: Retiro en tienda")

    def modalidad_entrega(e):
        if switch_entrega.value:
            switch_entrega.label = "Envío a domicilio"
            modalidad.value = "Seleccionado: Envío a domicilio"
        else:
            switch_entrega.label = "Retiro en tienda"
            modalidad.value = "Seleccionado: Retiro en tienda"
        page.update()

    switch_entrega = ft.Switch(
        label="Retiro en tienda",
        value=False,
        on_change=modalidad_entrega
    )

    medios_pago = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="opcion1", label="Efectivo o Transferencia bancaria (-10%)"),
            ft.Radio(value="opcion2", label="Tarjeta de Débito"),
            ft.Radio(value="opcion3", label="Tarjeta de Crédito 3 cuotas (+15%)")
        ])
    )

    resultado = ft.Text(size=18)

    def calcular(e):
        try:
            if dropdown_procesador.value is None:
                resultado.value = "Debe seleccionar un procesador"
                page.update()
                return

            if medios_pago.value is None:
                resultado.value = "Debe seleccionar un medio de pago"
                page.update()
                return

            presupuesto = int(campo_presupuesto.value)
            procesador = dropdown_procesador.value

            total = precios_procesadores[procesador]

            ram_gb = 2 ** int(ram.value)
            precios_ram = {
                8: 40000,
                16: 70000,
                32: 120000,
                64: 220000
            }
            total += precios_ram[ram_gb]

            if gpu.value:
                total += 250000
            if ssd.value:
                total += 90000
            if armado.value:
                total += 30000

            if switch_entrega.value:
                total += 15000

            cuota = None
            if medios_pago.value == "opcion1":
                total *= 0.90
            elif medios_pago.value == "opcion3":
                total *= 1.15
                cuota = total / 3

            consumo = consumo_cpu[procesador]
            if gpu.value:
                consumo += 200
            consumo += 50
            consumo *= 1.25

            if consumo > 450:
                fuente = "Recomendación: Fuente 650W o superior"
            else:
                fuente = "Recomendación: Fuente convencional 500W"

            diferencia = presupuesto - total

            if diferencia >= 0:
                estado = f"Presupuesto aprobado. Saldo restante: ${diferencia:.0f}"
            else:
                estado = f"Presupuesto insuficiente. Faltan ${abs(diferencia):.0f}"

            detalle_cuota = (
                f"\n3 cuotas de ${cuota:.0f} c/u"
                if cuota is not None
                else ""
            )

            resultado.value = (
                f"Cliente: {campo_nombre.value}\n\n"
                f"Procesador: {procesador}\n"
                f"RAM: {ram_gb} GB\n"
                f"Total final: ${total:.0f}{detalle_cuota}\n\n"
                f"Consumo estimado: {consumo:.0f}W\n"
                f"{fuente}\n\n"
                f"{estado}"
            )
        except ValueError:
            resultado.value = "Error: ingrese un presupuesto válido"
        page.update()

    boton = ft.ElevatedButton(
        "Calcular cotización",
        on_click=calcular
    )

    page.add(
        ft.Row([
            ft.Column([
                campo_nombre,
                campo_presupuesto,
                dropdown_procesador,
                texto_ram,
                ram,
                optativos,
                switch_entrega,
                modalidad,
                medios_pago,
                boton
            ]),
            ft.Column([
                ft.Text("RESULTADO", size=25),
                resultado
            ])
        ])
    )

ft.run(main)
