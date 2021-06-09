from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QDoubleValidator
from controller.validator import validation
from model.inventory_collections.inventory_collection import InventoryCollection


class InventoryItemPresetPage(QDialog):
    def __init__(self, main_modal_window):
        super().__init__()
        self.main_modal_window = main_modal_window
        self.first_time = True
        self.inventory_id = None
        self.fields = {
            "quantity": {
                "fields": (self.main_modal_window.ui.inventory_preset_qty_input,
                           self.main_modal_window.ui.error_inventory_preset_qty)
            },
        }
        self.main_modal_window.ui.cancel_inventory_preset_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.add_inventory_preset_butt.clicked.connect(self.add_item)
        self.validator = validation.Validation()
        self.main_modal_window.ui.inventory_preset_page.installEventFilter(self)
        self.set_input_fields()

    def set_input_fields(self):
        float_validator = QDoubleValidator()
        float_validator.setNotation(QDoubleValidator.Notation(0))
        self.main_modal_window.ui.inventory_preset_qty_input.setValidator(float_validator)

    def add_item(self):
        if self.validator.check_validation(self.fields):
            data = self.get_data()
            inventory_collection = InventoryCollection(**data)
            response_code, response_data = inventory_collection.post()
            if response_code > 399:
                self.main_modal_window.show_notification_page(
                    response_data,
                    is_error=True,
                    previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                        self.main_modal_window.ui.inventory_preset_page
                    )
                )
            else:
                self.main_modal_window.show_notification_page(response_data, is_error=False)

    def get_data(self):
        return {
            "count": self.main_modal_window.ui.inventory_preset_qty_input.text(),
            "inventory_id": self.inventory_id,
            "move_size_id": self.main_modal_window.ui.inventory_preset_combobox.currentData()
        }

    def set_page(self):
        move_size_data = self.main_modal_window.main_window.move_size.move_sizes
        self.main_modal_window.inventory_add_item_ui.set_move_size_list(move_size_data)

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.inventory_preset_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                if self.first_time:
                    self.set_page()
                    self.first_time = False
                return True
        return False
