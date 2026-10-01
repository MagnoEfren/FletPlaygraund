import flet as ft

from core.base_widget import ICON_OPTIONS, Param, WidgetConfig
from services.code_service import call, indent, py


class AlertDialogConfig(WidgetConfig):
    PARAMS = [
        Param("title", "Título", "text", "¿Eliminar archivo?", group="Contenido"),
        Param("content", "Mensaje", "text", "Esta acción no se puede deshacer.", group="Contenido"),
        Param("show_icon", "Icono superior", "switch", True, group="Contenido"),
        Param("icon", "Icono", "icon", "DELETE", options=ICON_OPTIONS, group="Contenido"),
        Param("modal", "Modal (no se cierra al tocar fuera)", "switch", True, group="Comportamiento"),
        Param("confirm", "Texto del botón principal", "text", "Eliminar", group="Comportamiento"),
    ]

    def __init__(self):
        super().__init__(
            name="AlertDialog", icon=ft.Icons.CHAT_BUBBLE_OUTLINE, category="Feedback",
            description="Diálogo de confirmación. En Flet 1.0 se abre con page.show_dialog(dlg) y "
                        "se cierra con page.pop_dialog(). Pulsa el botón de la vista previa.",
        )

    def _dialog(self, page: ft.Page) -> ft.AlertDialog:
        p = self.p
        return ft.AlertDialog(
            modal=p("modal"),
            icon=ft.Icon(self.icon_of(p("icon"))) if p("show_icon") else None,
            title=ft.Text(p("title")),
            content=ft.Text(p("content")),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                ft.FilledButton(p("confirm"), on_click=lambda e: page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def create_preview(self) -> ft.Control:
        def open_dialog(e: ft.Event):
            e.page.show_dialog(self._dialog(e.page))

        return ft.Button("Abrir diálogo", icon=ft.Icons.OPEN_IN_NEW, on_click=open_dialog)

    def generate_code(self) -> str:
        p = self.p
        dlg = call(
            "ft.AlertDialog",
            ("modal", py(p("modal"))),
            ("icon", f"ft.Icon({self.icon_code(p('icon'))})") if p("show_icon") else None,
            ("title", f"ft.Text({py(p('title'))})"),
            ("content", f"ft.Text({py(p('content'))})"),
            ("actions", "[\n"
                        '    ft.TextButton("Cancelar", on_click=lambda e: e.page.pop_dialog()),\n'
                        f"    ft.FilledButton({py(p('confirm'))}, on_click=lambda e: e.page.pop_dialog()),\n"
                        "]"),
            ("actions_alignment", "ft.MainAxisAlignment.END"),
        )
        return call("ft.Button", '"Abrir diálogo"',
                    ("on_click", f"lambda e: e.page.show_dialog(\n{indent(dlg)}\n)"))
