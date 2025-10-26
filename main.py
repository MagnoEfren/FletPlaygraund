import flet as ft
from ui  import MainLayout
from core  import WidgetManager


def main(page: ft.Page):
    """Punto de entrada principal de la aplicación"""
    page.title = "Flet Widgets Playground"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#f7fafc"
    
    # Inicializar el gestor de widgets
    widget_manager = WidgetManager()
    
    # Crear y agregar el layout principal
    main_layout = MainLayout(page, widget_manager)
    page.add(main_layout.build())


if __name__ == "__main__":

    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
