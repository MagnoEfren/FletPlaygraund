"""
theme.py — Un solo lugar para colores, medidas y temas.

Los colores de la interfaz usan los roles semánticos de Material 3
(ft.Colors.SURFACE, ON_SURFACE, OUTLINE_VARIANT...). Así el modo claro y
el oscuro funcionan solos: Flutter resuelve cada rol según el tema activo
y no hay que reconstruir nada al cambiar de modo.
"""
import flet as ft

APP_NAME = "Flet Widgets Playground"
APP_VERSION = "2.0.0"
REPO_URL = "https://github.com/MagnoEfren/FletPlaygraund"
DOCS_URL = "https://docs.flet.dev/controls/{slug}/"

# ---------- Marca ----------
SEED = "#4F46E5"                                   # índigo: semilla del esquema M3
BRAND_GRADIENT = ["#7EDF26", "#0148E2", "#00FBE8"]  # el degradado del logo original

# ---------- Roles semánticos (se adaptan a claro/oscuro) ----------
BG = ft.Colors.SURFACE_CONTAINER_LOW          # fondo de la página
PANEL_BG = ft.Colors.SURFACE                  # fondo de cada panel
CARD_BG = ft.Colors.SURFACE_CONTAINER         # tarjetas internas
STAGE_BG = ft.Colors.SURFACE_CONTAINER_LOWEST  # "escenario" de la vista previa
BORDER = ft.Colors.OUTLINE_VARIANT
TEXT = ft.Colors.ON_SURFACE
TEXT_MUTED = ft.Colors.ON_SURFACE_VARIANT
PRIMARY = ft.Colors.PRIMARY
SELECTED_BG = ft.Colors.PRIMARY_CONTAINER
SELECTED_TEXT = ft.Colors.ON_PRIMARY_CONTAINER

# ---------- Medidas ----------
BP_MOBILE = 700        # < 700 px: móvil (navegación inferior, una columna)
BP_DESKTOP = 1100      # >= 1100 px: escritorio (tres paneles)
SIDEBAR_W = 270
PARAMS_W = 340
MOBILE_PREVIEW_H = 260

RADIUS = 14
RADIUS_SM = 10
GAP = 12
PAD = 16
ANIM_MS = 180

# ---------- Paleta para los selectores de color ----------
PALETTE = [
    ("#667EEA", "Índigo"),
    ("#4F46E5", "Violeta"),
    ("#0EA5E9", "Cielo"),
    ("#14B8A6", "Turquesa"),
    ("#48BB78", "Verde"),
    ("#EAB308", "Ámbar"),
    ("#ED8936", "Naranja"),
    ("#F56565", "Rojo"),
    ("#EC4899", "Rosa"),
    ("#2D3748", "Grafito"),
    ("#FFFFFF", "Blanco"),
    ("#000000", "Negro"),
]


def build_theme() -> ft.Theme:
    """Tema base; el mismo objeto sirve para claro y oscuro (la semilla manda)."""
    return ft.Theme(color_scheme_seed=SEED)


def apply_theme(page: ft.Page, mode: str) -> None:
    """Aplica 'light' | 'dark' | 'system' a la página."""
    page.theme = build_theme()
    page.dark_theme = build_theme()
    page.theme_mode = {
        "light": ft.ThemeMode.LIGHT,
        "dark": ft.ThemeMode.DARK,
    }.get(mode, ft.ThemeMode.SYSTEM)
    page.bgcolor = BG


def panel(content: ft.Control, *, expand=None, width=None, padding=PAD) -> ft.Container:
    """Caja estándar de panel (borde suave + esquinas redondeadas)."""
    return ft.Container(
        content=content,
        expand=expand,
        width=width,
        padding=padding,
        bgcolor=PANEL_BG,
        border_radius=RADIUS,
        border=ft.Border.all(1, BORDER),
    )
