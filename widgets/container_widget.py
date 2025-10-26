import flet as ft
from core.base_widget import WidgetConfig


class ContainerConfig(WidgetConfig):
    """Configuración para el widget Container"""
    
    def __init__(self):
        super().__init__(
            name="Container",
            icon=ft.Icons.CROP_SQUARE,
            description="Un Container es como una caja contenedora. Permite controlar tamaño, espaciado, "
                       "color de fondo, bordes, sombras y gradientes. Es uno de los widgets más versátiles."
        )
        self.params = {
            'width': 250.0,
            'height': 200.0,
            'padding': 20.0,
            'margin': 10.0,
            'border_radius': 15.0,
            'bgcolor': '#667eea',
            'shadow': True,
            'gradient': False,
            'border': False,
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        return ft.Column([
            self._create_slider("Width", 'width', 50, 500, on_change_callback),
            self._create_slider("Height", 'height', 50, 400, on_change_callback),
            self._create_slider("Padding", 'padding', 0, 50, on_change_callback),
            self._create_slider("Margin", 'margin', 0, 50, on_change_callback),
            self._create_slider("Border Radius", 'border_radius', 0, 50, on_change_callback),
            
            ft.Divider(height=10),
            ft.Text("Opciones:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            
            ft.Row([
                ft.Switch(
                    label="Shadow",
                    value=self.params['shadow'],
                    on_change=lambda e: self._update_param('shadow', e.control.value, on_change_callback)
                ),
                ft.Switch(
                    label="Gradient",
                    value=self.params['gradient'],
                    on_change=lambda e: self._update_param('gradient', e.control.value, on_change_callback)
                ),
                ft.Switch(
                    label="Border",
                    value=self.params['border'],
                    on_change=lambda e: self._update_param('border', e.control.value, on_change_callback)
                ),
            ], wrap=True),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        border_obj = ft.border.all(3, "#2d3748") if self.params['border'] else None
        
        shadow_obj = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, "#000000"),
            offset=ft.Offset(0, 4),
        ) if self.params['shadow'] else None
        
        gradient_obj = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#667eea", "#764ba2"],
        ) if self.params['gradient'] else None
        
        return ft.Container(
            content=ft.Text("¡Hola Flet!", color="#ffffff", size=16, weight=ft.FontWeight.BOLD),
            width=self.params['width'],
            height=self.params['height'],
            padding=self.params['padding'],
            margin=self.params['margin'],
            border_radius=self.params['border_radius'],
            bgcolor=None if self.params['gradient'] else self.params['bgcolor'],
            alignment=ft.alignment.center,
            shadow=shadow_obj,
            gradient=gradient_obj,
            border=border_obj,
        )
    
    def generate_code(self) -> str:
        code_lines = ["ft.Container("]
        code_lines.append(f"    content=ft.Text('¡Hola Flet!', color='#ffffff'),")
        code_lines.append(f"    width={self.params['width']:.0f},")
        code_lines.append(f"    height={self.params['height']:.0f},")
        code_lines.append(f"    padding={self.params['padding']:.0f},")
        code_lines.append(f"    margin={self.params['margin']:.0f},")
        code_lines.append(f"    border_radius={self.params['border_radius']:.0f},")
        
        if self.params['gradient']:
            code_lines.append("    gradient=ft.LinearGradient(")
            code_lines.append("        begin=ft.alignment.top_left,")
            code_lines.append("        end=ft.alignment.bottom_right,")
            code_lines.append("        colors=['#667eea', '#764ba2'],")
            code_lines.append("    ),")
        else:
            code_lines.append(f"    bgcolor='{self.params['bgcolor']}',")
        
        if self.params['shadow']:
            code_lines.append("    shadow=ft.BoxShadow(")
            code_lines.append("        spread_radius=1,")
            code_lines.append("        blur_radius=15,")
            code_lines.append("        color=ft.Colors.with_opacity(0.3, '#000000'),")
            code_lines.append("        offset=ft.Offset(0, 4),")
            code_lines.append("    ),")
        
        if self.params['border']:
            code_lines.append("    border=ft.border.all(3, '#2d3748'),")
        
        code_lines.append("    alignment=ft.alignment.center,")
        code_lines.append(")")
        
        return "\n".join(code_lines)