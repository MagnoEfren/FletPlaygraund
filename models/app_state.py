"""
Estado compartido de la app (singleton).

Los paneles se vuelven a crear cuando el layout cruza un punto de quiebre
(escritorio <-> tablet <-> móvil). Por eso el estado NO vive en los paneles:
vive aquí, y cada panel lo lee al construirse.
"""


class AppState:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            obj = super().__new__(cls)
            obj._init()
            cls._instancia = obj
        return cls._instancia

    def _init(self):
        self.theme_mode: str = "system"      # light | dark | system
        self.current_widget: str = "Container"
        self.query: str = ""
        self.category: str = "Todos"
        self.favorites: set[str] = set()
        self.preview_mode: str = "auto"      # auto | light | dark  (tema SOLO de la vista previa)
        self.code_mode: str = "snippet"      # snippet | app
        self.layout_mode: str = ""           # mobile | tablet | desktop
        self.mobile_tab: int = 1             # 0 widgets, 1 editor, 2 código

    @classmethod
    def reset_singleton(cls):
        """Solo para pruebas."""
        cls._instancia = None
