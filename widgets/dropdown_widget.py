import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, code_list, py

FRUITS = ["Manzana", "Banana", "Cereza", "Durazno", "Fresa", "Kiwi", "Mango", "Naranja"]


class DropdownConfig(WidgetConfig):
    PARAMS = [
        Param("label", "Label", "text", "Fruta favorita", group="Contenido"),
        Param("count", "Cantidad de opciones", "slider", 5.0, 2, 8, divisions=6, group="Contenido"),
        Param("width", "Ancho", "slider", 260.0, 160, 460, unit="px", group="Estilo"),
        Param("filled", "Relleno (filled)", "switch", False, group="Estilo"),
        Param("leading_icon", "Icono inicial", "switch", True, group="Estilo"),
        Param("editable", "Editable (escribir)", "switch", False, group="Búsqueda"),
        Param("enable_filter", "Filtrar al escribir", "switch", False, group="Búsqueda"),
    ]

    def __init__(self):
        super().__init__(
            name="Dropdown", icon=ft.Icons.ARROW_DROP_DOWN_CIRCLE, category="Entrada",
            description="Menú desplegable Material 3. En Flet 1.0 se usa ft.DropdownOption (no "
                        "ft.dropdown.Option) y el evento on_select (no on_change).",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        editable = p("editable")
        return ft.Dropdown(
            label=p("label"), width=p("width"), filled=p("filled"),
            leading_icon=ft.Icons.RESTAURANT if p("leading_icon") else None,
            editable=editable, enable_filter=p("enable_filter") and editable,
            options=[ft.DropdownOption(key=f, text=f) for f in FRUITS[: int(p("count"))]],
            on_select=lambda e: print("Elegiste:", e.control.value),
        )

    def generate_code(self) -> str:
        p = self.p
        editable = p("editable")
        opts = [f'ft.DropdownOption(key={py(f)}, text={py(f)})' for f in FRUITS[: int(p("count"))]]
        return call(
            "ft.Dropdown",
            ("label", py(p("label"))),
            ("width", py(p("width"))),
            ("filled", "True") if p("filled") else None,
            ("leading_icon", "ft.Icons.RESTAURANT") if p("leading_icon") else None,
            ("editable", "True") if editable else None,
            ("enable_filter", "True") if p("enable_filter") and editable else None,
            ("options", code_list(opts)),
            ("on_select", 'lambda e: print("Elegiste:", e.control.value)'),
        )
