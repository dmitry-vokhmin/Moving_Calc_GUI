from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate


class AssetPageUi:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.asset_type_combobox.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.main_modal_window.ui.asset_type_combobox.setItemDelegate(QStyledItemDelegate())

    def set_add_asset(self, add_asset_funk):
        self.main_modal_window.ui.asset_header.setText("Add new asset")
        self.main_modal_window.ui.asset_text.setText("Add a new asset to your equipment by filling out a form below.")
        self.main_modal_window.ui.asset_name_input.setText("")
        for asset_type in self.main_modal_window.main_window.truck_type.truck_types:
            self.main_modal_window.ui.asset_type_combobox.addItem(asset_type["name"].capitalize(), asset_type["id"])
        self.main_modal_window.ui.asset_delete.setVisible(False)
        self.main_modal_window.ui.add_asset_butt.setText("Add Asset")
        self.main_modal_window.ui.add_asset_butt.setMinimumSize(156, 47)
        self.main_modal_window.ui.add_asset_butt.clicked.connect(add_asset_funk)

    def set_update_asset(self, asset_data, update_funk, delete_funk):
        self.main_modal_window.ui.asset_header.setText("Edit asset")
        self.main_modal_window.ui.asset_text.setText("Apply any changes to your asset information.")
        self.main_modal_window.ui.asset_name_input.setText(asset_data["name"].capitalize())
        self.main_modal_window.ui.asset_type_combobox.addItem(
            asset_data["truck_type"]["name"].capitalize(),
            asset_data["truck_type"]["id"]
        )
        for asset_type in self.main_modal_window.main_window.truck_type.truck_types:
            self.main_modal_window.ui.asset_type_combobox.addItem(asset_type["name"].capitalize(), asset_type["id"])
        self.main_modal_window.ui.asset_delete.setVisible(True)
        self.main_modal_window.ui.add_asset_butt.setText("Save")
        self.main_modal_window.ui.add_asset_butt.setMinimumSize(116, 47)
        self.main_modal_window.ui.add_asset_butt.clicked.connect(lambda: update_funk(asset_data))
        self.main_modal_window.ui.asset_delete.clicked.connect(lambda: delete_funk(asset_data))
