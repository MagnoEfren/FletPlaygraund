import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hola Magno 👋, Flet está funcionando!"))

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)

