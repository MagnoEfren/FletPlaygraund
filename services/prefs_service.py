"""
Persistencia de preferencias con ft.SharedPreferences (Flet 1.0).

- En web se guarda en el localStorage del navegador; en desktop/móvil en el
  almacenamiento nativo. Sobrevive a cerrar la app.
- Se guarda EN EL MOMENTO del cambio (nunca "al cerrar"): en Flet 1.0 un
  proceso empaquetado termina sin correr atexit/__del__.
- SharedPreferences es un Service: se crea una instancia NUEVA dentro de
  cada función async (no se guarda en self ni se agrega a page.overlay).
"""
import flet as ft

from models.app_state import AppState

_PREFIX = "flet_playground."
KEY_THEME = _PREFIX + "theme_mode"
KEY_FAVS = _PREFIX + "favorites"
KEY_LAST = _PREFIX + "last_widget"
KEY_CODE_MODE = _PREFIX + "code_mode"
KEY_PREVIEW_MODE = _PREFIX + "preview_mode"


async def load_into(state: AppState, valid_widgets: set[str]) -> None:
    """Lee las preferencias guardadas y las vuelca en el estado."""
    try:
        prefs = ft.SharedPreferences()
        theme = await prefs.get(KEY_THEME)
        favs = await prefs.get(KEY_FAVS)
        last = await prefs.get(KEY_LAST)
        code_mode = await prefs.get(KEY_CODE_MODE)
        preview_mode = await prefs.get(KEY_PREVIEW_MODE)
    except Exception as ex:  # primera ejecución, o plataforma sin soporte
        print("Preferencias no disponibles:", ex)
        return

    if theme in ("light", "dark", "system"):
        state.theme_mode = theme
    if isinstance(favs, list):
        state.favorites = {f for f in favs if f in valid_widgets}
    if isinstance(last, str) and last in valid_widgets:
        state.current_widget = last
    if code_mode in ("snippet", "app"):
        state.code_mode = code_mode
    if preview_mode in ("auto", "light", "dark"):
        state.preview_mode = preview_mode


async def save(key: str, value) -> None:
    try:
        await ft.SharedPreferences().set(key, value)
    except Exception as ex:
        print(f"No se pudo guardar {key}:", ex)
