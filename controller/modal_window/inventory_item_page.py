from PyQt5.QtWidgets import QDialog, QLineEdit
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
        self.set_input_fields()

    def set_input_fields(self):
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
                        response_data,
                        is_error=True,
                        previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                            self.main_modal_window.ui.invetory_item_page
                        )
                    )
                else:
                    self.main_modal_window.show_notification_page(response_data, is_error=False)

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

    # def set_categories(self):
    #     api_category = InventoryCategory()
    #     response_code, response_data = api_category.get()
    #     if response_code > 399:
    #         print(response_data)
    #     self.main_modal_window.inventory_new_item_ui.set_categories(response_data)

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.invetory_item_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                self.main_modal_window.ui.error_inventory_item_dimension.setVisible(False)
                return True
        return False
