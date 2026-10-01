# Flet Widgets Playground 2.0 — Flet 1.0.0

Explora los widgets de Flet en tiempo real: ajusta parámetros, mira la vista previa y copia el código.

## ▶️ Ejecutar
```bash
pip install -r requirements.txt      # flet==1.0.0
python main.py                       # abre en el navegador
flet run --web main.py               # modo web
flet run main.py                     # app de escritorio
```

## ✨ Novedades v2
- **Migrado a Flet 1.0.0**: `ft.run`, `ft.Button`, `ft.DropdownOption` + `on_select`, `ft.Border.all`, `ft.Alignment.*`, `ft.BoxFit`, Client Actions (`action=ft.CopyToClipboard` / `ft.OpenUrl`).
- **Modo claro / oscuro** con botón en la cabecera (se recuerda). Colores Material 3 semánticos.
- **Responsive**: escritorio (3 paneles), tablet y móvil (barra inferior Widgets · Editor · Código).
- **29 widgets** organizados en 6 categorías.
- **Búsqueda + filtros por categoría + favoritos** (persistentes).
- **Vista previa con tema propio**: Auto / Claro / Oscuro sin cambiar la app.
- **Código**: Snippet o App completa ejecutable, resaltado, copiar y descargar `.py`.
- **Restablecer** parámetros, enlace a la **documentación** oficial y atajo **Ctrl+K**.

## 📁 Estructura
```
main.py                  # punto de entrada (ft.run)
theme.py                 # colores, medidas, temas
pyproject.toml / requirements.txt
core/base_widget.py      # WidgetConfig + Param (parámetros declarativos)
core/widget_manager.py   # registro, búsqueda, filtros
models/app_state.py      # estado compartido (singleton)
services/code_service.py # generación de código (lógica pura)
services/prefs_service.py# preferencias (SharedPreferences)
ui/layout.py             # layout responsivo y acciones
ui/panels/               # left, center, right (preview + código)
ui/components/           # generador de controles de parámetros, avisos
widgets/                 # un archivo por widget
```

## 🔧 Agregar un widget
1. Crea `widgets/mi_widget.py`:
```python
import flet as ft
from core.base_widget import Param, WidgetConfig
from services.code_service import call, py

class MiWidgetConfig(WidgetConfig):
    PARAMS = [
        Param("size", "Tamaño", "slider", 40.0, 10, 100, unit="px"),
        Param("color", "Color", "color", "#667EEA"),
        Param("visible_icon", "Mostrar icono", "switch", True),
    ]

    def __init__(self):
        super().__init__(name="MiWidget", icon=ft.Icons.STAR,
                         category="Texto y media", description="Descripción...")

    def create_preview(self):
        return ft.Icon(ft.Icons.STAR, size=self.p("size"), color=self.p("color"))

    def generate_code(self):
        return call("ft.Icon", "ft.Icons.STAR", ("size", py(self.p("size"))),
                    ("color", py(self.p("color"))))
```
2. Añade la clase a `ALL_WIDGETS` en `widgets/__init__.py`. ¡Listo! Los controles se generan solos.

Tipos de `Param`: `slider`, `select`, `switch`, `color`, `text`, `icon`.

## ☁️ Desplegar en Cloudflare Pages
En **Settings → Builds & deployments** del proyecto:

| Campo | Valor |
|---|---|
| Framework preset | None |
| Build command | `bash build.sh` |
| Build output directory | `dist` |
| Variable de entorno | `PYTHON_VERSION` = `3.12` |

`build.sh` usa `flet publish` (web estática con Pyodide), que **no necesita Flutter**.
No uses `flet build web` en Cloudflare: intenta instalar Flutter y pide confirmación
(`[y/n]`), y como el build no es interactivo falla con `EOFError`.

Probar el build localmente:
```bash
bash build.sh
python -m http.server 8000 --directory dist   # abre http://localhost:8000
```
