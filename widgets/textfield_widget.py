import flet as ft
from core.base_widget import WidgetConfig


class TextFieldConfig(WidgetConfig):
    """Configuración para el widget TextField"""
    
    def __init__(self):
        super().__init__(
            name="TextField",
            icon=ft.Icons.INPUT,
            description="TextField es un campo de entrada de texto que permite al usuario escribir información. "
                       "Puede tener etiquetas, hints, validación y estilos personalizados."
        )
        self.params = {
            'width': 300.0,
            'label': 'Nombre de usuario',
            'border_radius': 10.0,
            'filled': True,
            'password': False,
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        return ft.Column([
            ft.Text(f"Width: {self.params['width']:.0f}px", 
                   size=13, weight=ft.FontWeight.W_500, color="#2d3748"),
            ft.Slider(
                min=150,
                max=500,
                value=self.params['width'],
                on_change=lambda e: self._update_param('width', e.control.value, on_change_callback)
            ),
            
            ft.Text(f"Border Radius: {self.params['border_radius']:.0f}px", 
                   size=13, weight=ft.FontWeight.W_500, color="#2d3748"),
            ft.Slider(
                min=0,
                max=30,
                value=self.params['border_radius'],
                on_change=lambda e: self._update_param('border_radius', e.control.value, on_change_callback)
            ),
            
            ft.Text("Label:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.TextField(
                value=self.params['label'],
                on_change=lambda e: self._update_param('label', e.control.value, on_change_callback)
            ),
            
            ft.Divider(height=10),
            ft.Row([
                ft.Switch(
                    label="Filled",
                    value=self.params['filled'],
                    on_change=lambda e: self._update_param('filled', e.control.value, on_change_callback)
                ),
                ft.Switch(
                    label="Password",
                    value=self.params['password'],
                    on_change=lambda e: self._update_param('password', e.control.value, on_change_callback)
                ),
            ], wrap=True),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        return ft.TextField(
            label=self.params['label'],
            width=self.params['width'],
            border_radius=self.params['border_radius'],
            filled=self.params['filled'],
            password=self.params['password'],
            can_reveal_password=self.params['password'],
        )
    
    def generate_code(self) -> str:
        code_lines = ["ft.TextField("]
        code_lines.append(f"    label='{self.params['label']}',")
        code_lines.append(f"    width={self.params['width']:.0f},")
        code_lines.append(f"    border_radius={self.params['border_radius']:.0f},")
        
        if self.params['filled']:
            code_lines.append("    filled=True,")
        if self.params['password']:
            code_lines.append("    password=True,")
            code_lines.append("    can_reveal_password=True,")
        
        code_lines.append(")")
        return "\n".join(code_lines)