import flet as ft
from core.base_widget import WidgetConfig


class CardConfig(WidgetConfig):
    """Configuración para el widget Card"""
    
    def __init__(self):
        super().__init__(
            name="Card",
            icon=ft.Icons.CREDIT_CARD,
            description="Card es un contenedor con elevación que crea una superficie Material Design. "
                       "Es ideal para agrupar información relacionada con un efecto de profundidad."
        )
        self.params = {
            'elevation': 4.0,
            'color': '#ffffff',
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        return ft.Column([
            self._create_slider("Elevation", 'elevation', 0, 20, on_change_callback),
            
            ft.Text("Color:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.Dropdown(
                value=self.params['color'],
                options=[
                    ft.dropdown.Option("#ffffff", "Blanco"),
                    ft.dropdown.Option("#f7fafc", "Gris Claro"),
                    ft.dropdown.Option("#e3f2fd", "Azul Claro"),
                    ft.dropdown.Option("#f0fff4", "Verde Claro"),
                ],
                on_change=lambda e: self._update_param('color', e.control.value, on_change_callback)
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        return ft.Card(
            elevation=self.params['elevation'],
            color=self.params['color'],
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Card Title", size=18, weight=ft.FontWeight.BOLD, color="#2d3748"),
                    ft.Text(
                        "Este es un ejemplo de Card con contenido.\n"
                        "Puedes agregar cualquier widget dentro.",
                        size=13,
                        color="#718096",
                    ),
                    ft.ElevatedButton("Acción", bgcolor="#667eea", color="#ffffff"),
                ], spacing=10),
                padding=20,
                width=300,
            ),
        )
    
    def generate_code(self) -> str:
        code_lines = ["ft.Card("]
        code_lines.append(f"    elevation={self.params['elevation']:.0f},")
        code_lines.append(f"    color='{self.params['color']}',")
        code_lines.append("    content=ft.Container(")
        code_lines.append("        content=ft.Column([")
        code_lines.append("            ft.Text('Card Title', size=18, weight=ft.FontWeight.BOLD),")
        code_lines.append("            ft.Text('Contenido de la card'),")
        code_lines.append("        ]),")
        code_lines.append("        padding=20,")
        code_lines.append("    ),")
        code_lines.append(")")
        return "\n".join(code_lines)