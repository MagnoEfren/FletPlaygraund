"""Avisos breves (SnackBar) — en Flet 1.0 se muestran con page.show_dialog()."""
import flet as ft


def show_snack(page: ft.Page, text: str, icon=ft.Icons.CHECK_CIRCLE) -> None:
    try:
        page.show_dialog(
            ft.SnackBar(
                content=ft.Row(
                    [ft.Icon(icon, color=ft.Colors.ON_INVERSE_SURFACE, size=18),
                     ft.Text(text, color=ft.Colors.ON_INVERSE_SURFACE)],
                    spacing=10,
                ),
                behavior=ft.SnackBarBehavior.FLOATING,
                width=360,
                duration=2200,
            )
        )
    except Exception:
        pass  # la página puede no estar lista todavía
