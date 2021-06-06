from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate


class InventoryAddItemUi:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.inventory_preset_combobox.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.main_modal_window.ui.inventory_preset_combobox.setItemDelegate(QStyledItemDelegate())

    def set_move_size_list(self, move_sizes):
        for move_size in move_sizes:
            self.main_modal_window.ui.inventory_preset_combobox.addItem(move_size["name"].title(), move_size["id"])
