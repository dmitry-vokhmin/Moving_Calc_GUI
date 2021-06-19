
class AssetTypePageUi:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.add_asset_type_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.asset_type_delete.clicked.connect(self.main_modal_window.reject)

    def set_add_asset(self, add_asset_funk):
        self.main_modal_window.ui.asset_type_header.setText("Add asset type")
        self.main_modal_window.ui.asset_type_text.setText("Add a new asset type to your equipment by filling out a form below.")
        self.main_modal_window.ui.asset_type_name_input.setText("")
        self.main_modal_window.ui.length_input.setText("")
        self.main_modal_window.ui.width_input.setText("")
        self.main_modal_window.ui.height_input.setText("")
        self.main_modal_window.ui.sq_feet_input.setText("")
        self.main_modal_window.ui.asset_type_delete.setVisible(False)
        self.main_modal_window.ui.add_asset_type_butt.setText("Add Asset Type")
        self.main_modal_window.ui.add_asset_type_butt.setMinimumSize(156, 47)
        self.main_modal_window.ui.add_asset_type_butt.disconnect()
        self.main_modal_window.ui.add_asset_type_butt.clicked.connect(add_asset_funk)

    def set_update_asset(self, asset_data, update_funk, delete_funk):
        self.main_modal_window.ui.asset_type_header.setText("Edit asset type")
        self.main_modal_window.ui.asset_type_text.setText("Apply any changes to your asset type information.")
        self.main_modal_window.ui.asset_type_name_input.setText(asset_data["name"].capitalize())
        self.main_modal_window.ui.length_input.setText(f'{asset_data["length"] or ""}')
        self.main_modal_window.ui.width_input.setText(f'{asset_data["width"] or ""}')
        self.main_modal_window.ui.height_input.setText(f'{asset_data["height"] or ""}')
        self.main_modal_window.ui.sq_feet_input.setText(str(asset_data["dimension"]))
        self.main_modal_window.ui.asset_type_delete.setVisible(True)
        self.main_modal_window.ui.add_asset_type_butt.setText("Save")
        self.main_modal_window.ui.add_asset_type_butt.setMinimumSize(116, 47)
        self.main_modal_window.ui.add_asset_type_butt.disconnect()
        self.main_modal_window.ui.asset_type_delete.disconnect()
        self.main_modal_window.ui.add_asset_type_butt.clicked.connect(lambda: update_funk(asset_data))
        self.main_modal_window.ui.asset_type_delete.clicked.connect(lambda: delete_funk(asset_data))
