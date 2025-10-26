import flet as ft
from core.base_widget import WidgetConfig


class ColumnConfig(WidgetConfig):
    """Configuración para el widget Column"""
    
    def __init__(self):
        super().__init__(
            name="Column",
            icon=ft.Icons.VIEW_AGENDA,
            description="Column organiza widgets verticalmente en una columna. Es el complemento de Row "
                       "y permite crear layouts verticales con control de espaciado y alineación."
        )
        self.params = {
            'spacing': 10.0,
            'horizontal_alignment': 'center',
            'scroll': False,
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        return ft.Column([
            self._create_slider("Spacing", 'spacing', 0, 50, on_change_callback),
            
            ft.Text("Horizontal Alignment:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.Dropdown(
                value=self.params['horizontal_alignment'],
                options=[
                    ft.dropdown.Option("start", "Start"),
                    ft.dropdown.Option("center", "Center"),
                    ft.dropdown.Option("end", "End"),
                ],
                on_change=lambda e: self._update_param('horizontal_alignment', e.control.value, on_change_callback)
            ),
            
            ft.Divider(height=10),
            ft.Switch(
                label="Scroll",
                value=self.params['scroll'],
                on_change=lambda e: self._update_param('scroll', e.control.value, on_change_callback)
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        horizontal_map = {
            'start': ft.CrossAxisAlignment.START,
            'center': ft.CrossAxisAlignment.CENTER,
            'end': ft.CrossAxisAlignment.END,
        }
        
        scroll_mode = ft.ScrollMode.AUTO if self.params['scroll'] else None
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Item 1", color="#ffffff", size=14),
                        bgcolor="#667eea",
                        padding=15,
                        border_radius=10,
                        width=200,
                    ),
                    ft.Container(
                        content=ft.Text("Item 2", color="#ffffff", size=14),
                        bgcolor="#48bb78",
                        padding=15,
                        border_radius=10,
                        width=200,
                    ),
                    ft.Container(
                        content=ft.Text("Item 3", color="#ffffff", size=14),
                        bgcolor="#f56565",
                        padding=15,
                        border_radius=10,
                        width=200,
                    ),
                ],
                spacing=self.params['spacing'],
                horizontal_alignment=horizontal_map[self.params['horizontal_alignment']],
                scroll=scroll_mode,
            ),
            width=250,
            height=250,
            padding=20,
            bgcolor="#f7fafc",
            border_radius=10,
        )
    
    def generate_code(self) -> str:
        horizontal_code = {
            'start': 'ft.CrossAxisAlignment.START',
            'center': 'ft.CrossAxisAlignment.CENTER',
            'end': 'ft.CrossAxisAlignment.END',
        }
        
        code_lines = ["ft.Column("]
        code_lines.append("    [")
        code_lines.append("        ft.Text('Item 1'),")
        code_lines.append("        ft.Text('Item 2'),")
        code_lines.append("        ft.Text('Item 3'),")
        code_lines.append("    ],")
        code_lines.append(f"    spacing={self.params['spacing']:.0f},")
        code_lines.append(f"    horizontal_alignment={horizontal_code[self.params['horizontal_alignment']]},")
        
        if self.params['scroll']:
            code_lines.append("    scroll=ft.ScrollMode.AUTO,")
        
        code_lines.append(")")
        return "\n".join(code_lines)