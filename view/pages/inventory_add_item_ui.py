from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate


class InventoryAddItemUi:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.inventory_preset_combobox.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.main_modal_window.ui.inventory_preset_combobox.setItemDelegate(QStyledItemDelegate())

    def set_move_size_list(self, inventory_collection_data):
        for inventory_collection in inventory_collection_data:
            self.main_modal_window.ui.inventory_preset_combobox.addItem(
                inventory_collection["move_size"]["name"].title().replace("_", " "),
                inventory_collection["id"]
            )

    def set_calculator_move_size_list(self, preset_inventory):
        for key, value in preset_inventory.items():
            self.main_modal_window.ui.inventory_preset_combobox.addItem(value["move_size_name"], key)
