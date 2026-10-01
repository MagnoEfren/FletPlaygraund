import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, code_list, py

OPTIONS = ["Rojo", "Verde", "Azul", "Amarillo", "Morado"]


class RadioGroupConfig(WidgetConfig):
    PARAMS = [
        Param("count", "Cantidad de opciones", "slider", 3.0, 2, 5, divisions=3, group="Opciones"),
        Param("horizontal", "En fila (Row)", "switch", False, group="Opciones"),
        Param("selected", "Seleccionada", "select", "Rojo",
              options=[(o, o) for o in OPTIONS], group="Estado"),
        Param("active_color", "Color activo", "color", None, allow_none=True, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="RadioGroup", icon=ft.Icons.RADIO_BUTTON_CHECKED, category="Entrada",
            doc_slug="radiogroup",
            description="Grupo de opciones excluyentes: un RadioGroup envuelve varios Radio "
                        "(en Column o Row) y guarda el valor elegido.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        radios = [ft.Radio(value=o, label=o, active_color=p("active_color"))
                  for o in OPTIONS[: int(p("count"))]]
        box = ft.Row(radios) if p("horizontal") else ft.Column(radios, spacing=0)
        return ft.RadioGroup(content=box, value=p("selected"))

    def generate_code(self) -> str:
        p = self.p
        radios = [call("ft.Radio", ("value", py(o)), ("label", py(o)),
                       ("active_color", py(p("active_color"))) if p("active_color") else None)
                  for o in OPTIONS[: int(p("count"))]]
        box = call("ft.Row" if p("horizontal") else "ft.Column", code_list(radios))
        return call("ft.RadioGroup", ("content", box), ("value", py(p("selected"))),
                    ("on_change", "lambda e: print(e.control.value)"))
