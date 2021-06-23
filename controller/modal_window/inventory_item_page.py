import re
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QDoubleValidator
from controller.validator import validation
from model.inventory.inventory import Inventory


class InventoryItemPage(QDialog):
    def __init__(self, main_modal_window):
        super().__init__()
        self.main_modal_window = main_modal_window
        self.fields = {
            "name": {
                "fields": (self.main_modal_window.ui.inventory_item_name_input,
                           self.main_modal_window.ui.error_inventory_item_name)
            },
        }
        self.main_modal_window.ui.cancel_inventor_item_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.add_inventor_item_butt.clicked.connect(self.add_item)
        self.validator = validation.Validation()
        self.main_modal_window.ui.invetory_item_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        float_validator = QDoubleValidator()
        float_validator.setNotation(QDoubleValidator.Notation(0))
        for input_field in self.main_modal_window.ui.inventor_item_dimension_frame.findChildren(QLineEdit):
            input_field.setValidator(float_validator)
        self.main_modal_window.ui.inventory_item_name_input.setValidator(
            validation.EmptyStrValidation(*self.fields["name"]["fields"])
        )

    def add_item(self):
        if self.validator.check_validation(self.fields):
            if self.check_dimension_fields():
                data = self.get_data()
                api_inventory = Inventory(**data)
                response_code, response_data = api_inventory.post()
                if response_code > 399:
                    self.main_modal_window.show_notification_page(
                        description=response_data,
                        is_error=True,
                        previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                            self.main_modal_window.ui.invetory_item_page
                        )
                    )
                else:
                    self.main_modal_window.show_notification_page(
                        title="New item added",
                        description="New inventory item was added successfully to the Custom Room bucket.",
                        next_page=self.go_to_custom_room,
                        btn_text="Go to Custom Room",
                        is_error=False)

    def go_to_custom_room(self):
        for btn in self.main_modal_window.main_window.ui.inventory_room_menu_frame.findChildren(QPushButton):
            if re.search("Custom", btn.text()):
                btn.click()
        self.main_modal_window.close()

    def get_data(self):
        return {
            "name": self.fields["name"]["fields"][0].text(),
            "length": self.main_modal_window.ui.inventory_length_input.text(),
            "width": self.main_modal_window.ui.inventory_width_input.text(),
            "height": self.main_modal_window.ui.inventory_height_input.text(),
        }

    def check_dimension_fields(self):
        all_fields_filled = True
        error_fields = []
        for line_input in self.main_modal_window.ui.inventor_item_dimension_frame.findChildren(QLineEdit):
            if line_input.text():
                line_input.setProperty("error", False)
                line_input.setStyle(line_input.style())
            else:
                all_fields_filled = False
                error_fields.append(line_input)
        if not all_fields_filled:
            for line_input in error_fields:
                self.validator.change_field_style(
                    line_input, self.main_modal_window.ui.error_inventory_item_dimension, True
                )
        return all_fields_filled

    def reset_fields(self):
        for input_field in self.main_modal_window.ui.inventor_item_main_frame.findChildren(QLineEdit):
            input_field.setText("")

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.invetory_item_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                self.reset_fields()
                self.main_modal_window.ui.error_inventory_item_dimension.setVisible(False)
                return True
        return False
