import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

POSITIONS = [("RIGHT", "Derecha"), ("LEFT", "Izquierda")]


class SwitchConfig(WidgetConfig):
    PARAMS = [
        Param("label", "Label", "text", "Notificaciones", group="Contenido"),
        Param("value", "Encendido", "switch", True, group="Estado"),
        Param("adaptive", "Adaptativo (estilo iOS en Apple)", "switch", False, group="Estado"),
        Param("label_position", "Posición del label", "select", "RIGHT", options=POSITIONS, group="Estilo"),
        Param("active_color", "Color activo (pulgar)", "color", None, allow_none=True, group="Estilo"),
        Param("active_track_color", "Color de la pista", "color", None, allow_none=True, group="Estilo"),
        Param("thumb_icon", "Icono en el pulgar", "switch", False, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="Switch", icon=ft.Icons.TOGGLE_ON, category="Entrada",
            description="Interruptor encendido/apagado. Con adaptive=True usa el estilo nativo "
                        "Cupertino en iOS y macOS.",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Switch(
            label=p("label"), value=p("value"), adaptive=p("adaptive") or None,
            label_position=getattr(ft.LabelPosition, p("label_position")),
            active_color=p("active_color"), active_track_color=p("active_track_color"),
            thumb_icon={ft.ControlState.SELECTED: ft.Icons.CHECK,
                        ft.ControlState.DEFAULT: ft.Icons.CLOSE} if p("thumb_icon") else None,
        )

    def generate_code(self) -> str:
        p = self.p
        return call(
            "ft.Switch",
            ("label", py(p("label"))),
            ("value", py(p("value"))),
            ("adaptive", "True") if p("adaptive") else None,
            ("label_position", "ft.LabelPosition.LEFT") if p("label_position") == "LEFT" else None,
            ("active_color", py(p("active_color"))) if p("active_color") else None,
            ("active_track_color", py(p("active_track_color"))) if p("active_track_color") else None,
            ("thumb_icon", "{\n    ft.ControlState.SELECTED: ft.Icons.CHECK,\n"
                           "    ft.ControlState.DEFAULT: ft.Icons.CLOSE,\n}") if p("thumb_icon") else None,
            ("on_change", "lambda e: print(e.control.value)"),
        )
