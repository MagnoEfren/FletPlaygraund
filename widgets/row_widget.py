import flet as ft
from core.base_widget import WidgetConfig


class RowConfig(WidgetConfig):
    """Configuración para el widget Row"""
    
    def __init__(self):
        super().__init__(
            name="Row",
            icon=ft.Icons.VIEW_WEEK,
            description="Row organiza widgets horizontalmente en una fila. Permite alinear elementos, "
                       "controlar espaciado y hacer que los elementos se envuelvan automáticamente."
        )
        self.params = {
            'spacing': 10.0,
            'alignment': 'start',
            'vertical_alignment': 'center',
            'wrap': False,
        }
    
    def create_controls(self, on_change_callback) -> ft.Column:
        return ft.Column([
            self._create_slider("Spacing", 'spacing', 0, 50, on_change_callback),
            
            ft.Text("Horizontal Alignment:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.Dropdown(
                value=self.params['alignment'],
                options=[
                    ft.dropdown.Option("start", "Start"),
                    ft.dropdown.Option("center", "Center"),
                    ft.dropdown.Option("end", "End"),
                    ft.dropdown.Option("space_between", "Space Between"),
                    ft.dropdown.Option("space_around", "Space Around"),
                ],
                on_change=lambda e: self._update_param('alignment', e.control.value, on_change_callback)
            ),
            
            ft.Text("Vertical Alignment:", size=14, weight=ft.FontWeight.BOLD, color="#2d3748"),
            ft.Dropdown(
                value=self.params['vertical_alignment'],
                options=[
                    ft.dropdown.Option("start", "Start"),
                    ft.dropdown.Option("center", "Center"),
                    ft.dropdown.Option("end", "End"),
                ],
                on_change=lambda e: self._update_param('vertical_alignment', e.control.value, on_change_callback)
            ),
            
            ft.Divider(height=10),
            ft.Switch(
                label="Wrap (Auto ajuste)",
                value=self.params['wrap'],
                on_change=lambda e: self._update_param('wrap', e.control.value, on_change_callback)
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_preview(self) -> ft.Control:
        alignment_map = {
            'start': ft.MainAxisAlignment.START,
            'center': ft.MainAxisAlignment.CENTER,
            'end': ft.MainAxisAlignment.END,
            'space_between': ft.MainAxisAlignment.SPACE_BETWEEN,
            'space_around': ft.MainAxisAlignment.SPACE_AROUND,
        }
        
        vertical_map = {
            'start': ft.CrossAxisAlignment.START,
            'center': ft.CrossAxisAlignment.CENTER,
            'end': ft.CrossAxisAlignment.END,
        }
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Text("Item 1", color="#ffffff", size=14),
                        bgcolor="#667eea",
                        padding=15,
                        border_radius=10,
                    ),
                    ft.Container(
                        content=ft.Text("Item 2", color="#ffffff", size=14),
                        bgcolor="#48bb78",
                        padding=15,
                        border_radius=10,
                    ),
                    ft.Container(
                        content=ft.Text("Item 3", color="#ffffff", size=14),
                        bgcolor="#f56565",
                        padding=15,
                        border_radius=10,
                    ),
                ],
                spacing=self.params['spacing'],
                alignment=alignment_map[self.params['alignment']],
                vertical_alignment=vertical_map[self.params['vertical_alignment']],
                wrap=self.params['wrap'],
            ),
            width=450,
            padding=20,
            bgcolor="#f7fafc",
            border_radius=10,
        )
    
    def generate_code(self) -> str:
        alignment_code = {
            'start': 'ft.MainAxisAlignment.START',
            'center': 'ft.MainAxisAlignment.CENTER',
            'end': 'ft.MainAxisAlignment.END',
            'space_between': 'ft.MainAxisAlignment.SPACE_BETWEEN',
            'space_around': 'ft.MainAxisAlignment.SPACE_AROUND',
        }
        
        vertical_code = {
            'start': 'ft.CrossAxisAlignment.START',
            'center': 'ft.CrossAxisAlignment.CENTER',
            'end': 'ft.CrossAxisAlignment.END',
        }
        
        code_lines = ["ft.Row("]
        code_lines.append("    [")
        code_lines.append("        ft.Text('Item 1'),")
        code_lines.append("        ft.Text('Item 2'),")
        code_lines.append("        ft.Text('Item 3'),")
        code_lines.append("    ],")
        code_lines.append(f"    spacing={self.params['spacing']:.0f},")
        code_lines.append(f"    alignment={alignment_code[self.params['alignment']]},")
        code_lines.append(f"    vertical_alignment={vertical_code[self.params['vertical_alignment']]},")
        
        if self.params['wrap']:
            code_lines.append("    wrap=True,")
        
        code_lines.append(")")
        return "\n".join(code_lines)