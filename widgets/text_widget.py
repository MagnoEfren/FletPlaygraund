import flet as ft
from core.base_widget import WidgetConfig


class TextConfig(WidgetConfig):
    """Configuración para el widget Text"""
    
    def __init__(self):
        super().__init__(
            name="Text",
            icon=ft.Icons.TEXT_FIELDS,
            description="El widget Text muestra texto en pantalla. Permite personalizar tamaño, peso, "
                       "color, estilo, alineación y más. Es fundamental para mostrar información al usuario."
        )
        self.params = {
            'size': 24.0,
            'weight': 'normal',
            'color': '#2d3748',
            'italic': False,
            'selectable': False,
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        return ft.Column([
            ft.Text(f"Size: {self.params['size']:.0f}px", 
                   size=13, weight=ft.FontWeight.W_500, color="#2d3748"),
            ft.Slider(
                min=10,
                max=60,
                value=self.params['size'],
                on_change=lambda e: self._update_param('size', e.control.value, on_change_callback)
            ),
            
            ft.Text("Weight:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.Dropdown(
                value=self.params['weight'],
                options=[
                    ft.dropdown.Option("normal", "Normal"),
                    ft.dropdown.Option("bold", "Bold"),
                    ft.dropdown.Option("w_300", "Light (300)"),
                    ft.dropdown.Option("w_500", "Medium (500)"),
                    ft.dropdown.Option("w_700", "Bold (700)"),
                ],
                on_change=lambda e: self._update_param('weight', e.control.value, on_change_callback)
            ),
            
            ft.Text("Color:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.Dropdown(
                value=self.params['color'],
                options=[
                    ft.dropdown.Option("#2d3748", "Gris Oscuro"),
                    ft.dropdown.Option("#667eea", "Azul"),
                    ft.dropdown.Option("#48bb78", "Verde"),
                    ft.dropdown.Option("#f56565", "Rojo"),
                    ft.dropdown.Option("#ed8936", "Naranja"),
                ],
                on_change=lambda e: self._update_param('color', e.control.value, on_change_callback)
            ),
            
            ft.Divider(height=10),
            ft.Row([
                ft.Switch(
                    label="Italic",
                    value=self.params['italic'],
                    on_change=lambda e: self._update_param('italic', e.control.value, on_change_callback)
                ),
                ft.Switch(
                    label="Selectable",
                    value=self.params['selectable'],
                    on_change=lambda e: self._update_param('selectable', e.control.value, on_change_callback)
                ),
            ], wrap=True),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        weight_map = {
            'normal': ft.FontWeight.NORMAL,
            'bold': ft.FontWeight.BOLD,
            'w_300': ft.FontWeight.W_300,
            'w_500': ft.FontWeight.W_500,
            'w_700': ft.FontWeight.W_700,
        }
        
        return ft.Text(
            "Este es un texto de ejemplo",
            size=self.params['size'],
            weight=weight_map[self.params['weight']],
            color=self.params['color'],
            italic=self.params['italic'],
            selectable=self.params['selectable'],
        )
    
    def generate_code(self) -> str:
        weight_str = f"ft.FontWeight.{self.params['weight'].upper()}"
        
        code_lines = ["ft.Text("]
        code_lines.append("    'Este es un texto de ejemplo',")
        code_lines.append(f"    size={self.params['size']:.0f},")
        code_lines.append(f"    weight={weight_str},")
        code_lines.append(f"    color='{self.params['color']}',")
        
        if self.params['italic']:
            code_lines.append("    italic=True,")
        if self.params['selectable']:
            code_lines.append("    selectable=True,")
        
        code_lines.append(")")
        return "\n".join(code_lines)