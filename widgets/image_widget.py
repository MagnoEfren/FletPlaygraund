import flet as ft

from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

SOURCES = [
    ("https://picsum.photos/id/1015/600/400", "Río y montañas"),
    ("https://picsum.photos/id/1025/600/400", "Perro"),
    ("https://picsum.photos/id/1043/600/400", "Ciudad"),
    ("https://picsum.photos/id/1069/600/400", "Medusas"),
    ("https://flet.dev/img/logo.svg", "Logo de Flet (SVG)"),
]
FITS = [("COVER", "Cover"), ("CONTAIN", "Contain"), ("FILL", "Fill"), ("FIT_WIDTH", "Fit width"),
        ("FIT_HEIGHT", "Fit height"), ("NONE", "None"), ("SCALE_DOWN", "Scale down")]


class ImageConfig(WidgetConfig):
    PARAMS = [
        Param("src", "Imagen", "select", SOURCES[0][0], options=SOURCES, group="Fuente"),
        Param("width", "Ancho", "slider", 320.0, 80, 520, unit="px", group="Tamaño"),
        Param("height", "Alto", "slider", 220.0, 80, 420, unit="px", group="Tamaño"),
        Param("fit", "fit (ft.BoxFit)", "select", "COVER", options=FITS, group="Tamaño"),
        Param("border_radius", "Radio de borde", "slider", 16.0, 0, 200, unit="px", group="Estilo"),
        Param("opacity", "Opacidad", "slider", 1.0, 0.1, 1.0, decimals=2, group="Estilo"),
    ]

    def __init__(self):
        super().__init__(
            name="Image", icon=ft.Icons.IMAGE, category="Texto y media",
            description="Muestra imágenes desde URL, assets locales o bytes (PNG, JPG, GIF, SVG...). "
                        "fit usa ft.BoxFit en Flet 1.0 (antes ImageFit).",
        )

    def create_preview(self) -> ft.Control:
        p = self.p
        return ft.Image(
            src=p("src"), width=p("width"), height=p("height"),
            fit=getattr(ft.BoxFit, p("fit")), border_radius=p("border_radius"),
            opacity=p("opacity"),
            error_content=ft.Column(
                [ft.Icon(ft.Icons.BROKEN_IMAGE, size=40), ft.Text("Sin conexión a la imagen")],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def generate_code(self) -> str:
        p = self.p
        return call(
            "ft.Image",
            ("src", py(p("src"))),
            ("width", py(p("width"))),
            ("height", py(p("height"))),
            ("fit", f"ft.BoxFit.{p('fit')}"),
            ("border_radius", py(p("border_radius"))),
            ("opacity", py(p("opacity"))) if p("opacity") < 1 else None,
        )
