"""
Módulo widgets: una clase de configuración por control de Flet.

Para agregar un widget nuevo basta con crear su archivo y añadir la clase a
ALL_WIDGETS (el WidgetManager los registra automáticamente desde aquí).
"""
from .avatar_widget import CircleAvatarConfig
from .badge_widget import BadgeConfig
from .button_widget import ButtonConfig
from .card_widget import CardConfig
from .checkbox_widget import CheckboxConfig
from .chip_widget import ChipConfig
from .column_widget import ColumnConfig
from .container_widget import ContainerConfig
from .datatable_widget import DataTableConfig
from .dialog_widget import AlertDialogConfig
from .divider_widget import DividerConfig
from .dropdown_widget import DropdownConfig
from .expansiontile_widget import ExpansionTileConfig
from .fab_widget import FloatingActionButtonConfig
from .gridview_widget import GridViewConfig
from .icon_widget import IconConfig
from .iconbutton_widget import IconButtonConfig
from .image_widget import ImageConfig
from .listtile_widget import ListTileConfig
from .progress_widget import ProgressBarConfig, ProgressRingConfig
from .radio_widget import RadioGroupConfig
from .row_widget import RowConfig
from .segmented_widget import SegmentedButtonConfig
from .slider_widget import SliderConfig
from .stack_widget import StackConfig
from .switch_widget import SwitchConfig
from .text_widget import TextConfig
from .textfield_widget import TextFieldConfig

# El orden de esta lista es el orden en el panel izquierdo.
ALL_WIDGETS = [
    # Layout
    ContainerConfig, RowConfig, ColumnConfig, StackConfig, GridViewConfig, CardConfig, DividerConfig,
    # Texto y media
    TextConfig, IconConfig, ImageConfig, CircleAvatarConfig, BadgeConfig,
    # Botones
    ButtonConfig, IconButtonConfig, FloatingActionButtonConfig, SegmentedButtonConfig,
    # Entrada
    TextFieldConfig, DropdownConfig, CheckboxConfig, SwitchConfig, SliderConfig, RadioGroupConfig,
    # Listas y datos
    ListTileConfig, ExpansionTileConfig, DataTableConfig, ChipConfig,
    # Feedback
    ProgressBarConfig, ProgressRingConfig, AlertDialogConfig,
]

__all__ = ["ALL_WIDGETS"] + [cls.__name__ for cls in ALL_WIDGETS]
