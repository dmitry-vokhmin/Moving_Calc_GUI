from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QDoubleValidator
from controller.validator import validation
from model.inventory.inventory_collection import InventoryCollection
from model.inventory.inventory_inventory_collection import InventoryInventoryCollection


class InventoryItemPresetPage(QDialog):
    def __init__(self, main_modal_window):
        super().__init__()
        self.main_modal_window = main_modal_window
        self.first_time = True
        self.inventory = None
        self.fields = {
            "quantity": {
                "fields": (self.main_modal_window.ui.inventory_preset_qty_input,
                           self.main_modal_window.ui.error_inventory_preset_qty)
            },
        }
        self.main_modal_window.ui.cancel_inventory_preset_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.add_inventory_preset_butt.clicked.connect(self.add_item_to_db)
        self.validator = validation.Validation()
        self.main_modal_window.ui.inventory_preset_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        float_validator = QDoubleValidator()
        float_validator.setNotation(QDoubleValidator.Notation(0))
        self.main_modal_window.ui.inventory_preset_qty_input.setValidator(float_validator)

    def add_item_to_calc_preset(self):
        data = {
            "inventory_id": self.inventory["id"],
            "count": self.main_modal_window.ui.inventory_preset_qty_input.text(),
            "inventories": {
                "name": self.inventory["name"]
            }
        }
        selected_move_size = self.main_modal_window.ui.inventory_preset_combobox.currentData()
        self.main_modal_window.main_window.calculator_page.inventory_check_page.update_preset_inventory(
            data, selected_move_size
        )

    def add_item_to_db(self):
        if self.validator.check_validation(self.fields):
            data = self.get_data()
            inventory_collection = InventoryInventoryCollection(**data)
            response_code, response_data = inventory_collection.post()
            if response_code > 399:
                self.main_modal_window.show_notification_page(
                    description=response_data,
                    is_error=True,
                    previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                        self.main_modal_window.ui.inventory_preset_page
                    )
                )
            else:
                self.main_modal_window.show_notification_page(
                    title="New item added",
                    description=f"New item was added to "
                                f"{self.main_modal_window.ui.inventory_preset_combobox.currentText()}",
                    is_error=False)

    def get_data(self):
        return {
            "count": self.main_modal_window.ui.inventory_preset_qty_input.text(),
            "inventory_id": self.inventory["id"],
            "inventory_collection_id": self.main_modal_window.ui.inventory_preset_combobox.currentData()
        }

    def calculator_setup(self, preset_inventory):
        self.main_modal_window.inventory_add_item_ui.set_calculator_move_size_list(preset_inventory)
        self.main_modal_window.ui.add_inventory_preset_butt.disconnect()
        self.main_modal_window.ui.add_inventory_preset_butt.clicked.connect(self.add_item_to_calc_preset)

    def set_page(self):
        inventory_collection_data = self.main_modal_window.main_window.get_data(InventoryCollection)
        self.main_modal_window.inventory_add_item_ui.set_move_size_list(inventory_collection_data)
        self.main_modal_window.ui.add_inventory_preset_butt.disconnect()
        self.main_modal_window.ui.add_inventory_preset_butt.clicked.connect(self.add_item_to_db)

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.inventory_preset_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                return True
        return False
