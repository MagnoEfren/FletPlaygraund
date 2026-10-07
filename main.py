"""
Flet Widgets Playground — punto de entrada (Flet 1.0.0).

    flet run --web main.py     # en el navegador
    flet run main.py           # app de escritorio
    python main.py             # abre el navegador (igual que la versión original)
"""
from pathlib import Path

import flet as ft

import theme
from core import WidgetManager
from models import AppState
from services import prefs_service
from ui import MainLayout

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


async def main(page: ft.Page):
    page.title = theme.APP_NAME
    page.padding = 0
    page.spacing = 0
    # Errores de dibujo de Flutter (pantallas grises, etc.) llegan aquí con el mensaje exacto
    page.on_error = lambda e: print("ERROR CLIENTE:", e.data)

    manager = WidgetManager()
    state = AppState()

    # Preferencias guardadas: tema, favoritos, último widget, modos de código/vista previa
    await prefs_service.load_into(state, manager.names())
    manager.set_current_widget(state.current_widget)
    theme.apply_theme(page, state.theme_mode)

    layout = MainLayout(page, manager)
    page.add(layout.build())




# Sin "if __name__ == '__main__'": al publicarse como web estática (flet publish,
# Cloudflare Pages) el archivo se ejecuta dentro de Pyodide y ft.run debe correr siempre.
ft.run(main, assets_dir=str(ASSETS_DIR), view=ft.AppView.WEB_BROWSER)
