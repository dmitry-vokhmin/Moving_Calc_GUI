from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QDoubleValidator
from controller.validator import validation


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

    def check_dimension_fields(self):
        all_fields_filled = True
        error_fields = []
        for line_input in self.main_modal_window.ui.inventor_item_dimension_frame.findChildren(QLineEdit):
            if line_input.text():
                all_fields_filled = False
                line_input.setProperty("error", False)
                line_input.setStyle(line_input.style())
            else:
                error_fields.append(line_input)
        if not all_fields_filled:
            for line_input in error_fields:
                self.validator.change_field_style(
                    line_input, self.main_modal_window.ui.error_inventory_item_dimension, True
                )
        return all_fields_filled

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.invetory_item_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                self.main_modal_window.ui.error_inventory_item_dimension.setVisible(False)
                return True
        return False
