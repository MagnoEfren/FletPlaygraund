import flet as ft
from core.base_widget import WidgetConfig


class ElevatedButtonConfig(WidgetConfig):
    """Configuración para el widget ElevatedButton"""
    
    def __init__(self):
        super().__init__(
            name="ElevatedButton",
            icon=ft.Icons.SMART_BUTTON,
            description="Los botones elevados permiten interacciones del usuario. Tienen una elevación "
                       "que crea una sombra, lo que los hace destacar. Ideales para acciones principales."
        )
        self.params = {
            'width': 200.0,
            'height': 50.0,
            'bgcolor': '#48bb78',
            'color': '#ffffff',
            'elevation': 4.0,
            'icon': True,
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        return ft.Column([
            self._create_slider("Width", 'width', 100, 400, on_change_callback),
            self._create_slider("Height", 'height', 30, 100, on_change_callback),
            self._create_slider("Elevation", 'elevation', 0, 20, on_change_callback),
            
            ft.Text("Background Color:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.Dropdown(
                value=self.params['bgcolor'],
                options=[
                    ft.dropdown.Option("#48bb78", "Verde"),
                    ft.dropdown.Option("#667eea", "Azul"),
                    ft.dropdown.Option("#f56565", "Rojo"),
                    ft.dropdown.Option("#ed8936", "Naranja"),
                ],
                on_change=lambda e: self._update_param('bgcolor', e.control.value, on_change_callback)
            ),
            
            ft.Divider(height=10),
            ft.Switch(
                label="Mostrar Icono",
                value=self.params['icon'],
                on_change=lambda e: self._update_param('icon', e.control.value, on_change_callback)
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        icon_obj = ft.Icons.STAR if self.params['icon'] else None
        
        return ft.ElevatedButton(
            text="Click Me!",
            width=self.params['width'],
            height=self.params['height'],
            icon=icon_obj,
            style=ft.ButtonStyle(
                bgcolor=self.params['bgcolor'],
                color=self.params['color'],
                elevation=self.params['elevation'],
            ),
        )
    
    def generate_code(self) -> str:
        code_lines = ["ft.ElevatedButton("]
        code_lines.append("    text='Click Me!',")
        code_lines.append(f"    width={self.params['width']:.0f},")
        code_lines.append(f"    height={self.params['height']:.0f},")
        
        if self.params['icon']:
            code_lines.append("    icon=ft.Icons.STAR,")
        
        code_lines.append("    style=ft.ButtonStyle(")
        code_lines.append(f"        bgcolor='{self.params['bgcolor']}',")
        code_lines.append(f"        color='{self.params['color']}',")
        code_lines.append(f"        elevation={self.params['elevation']:.0f},")
        code_lines.append("    ),")
        code_lines.append(")")
        
        return "\n".join(code_lines)