from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QDoubleValidator
from model.truck.truck_type import TruckType
from controller.validator import validation


class AssetTypePage(QDialog):
    def __init__(self, main_modal_window):
        QDialog.__init__(self, main_modal_window)
        self.main_modal_window = main_modal_window
        self.fields = {
            "name": {
                "fields": (self.main_modal_window.ui.asset_type_name_input,
                           self.main_modal_window.ui.error_asset_type_name)
            },
            "sq_feet": {
                "fields": (self.main_modal_window.ui.sq_feet_input, self.main_modal_window.ui.error_dimension)
            }
        }
        self.main_modal_window.ui.cancel_asset_type_butt.clicked.connect(self.main_modal_window.reject)
        self.validator = validation.Validation()
        self.main_modal_window.ui.asset_type_page.installEventFilter(self)
        self.set_input_fields()

    def set_input_fields(self):
        float_validator = QDoubleValidator()
        float_validator.setNotation(QDoubleValidator.Notation(0))
        for input_field in self.main_modal_window.ui.asset_type_dimension_frame.findChildren(QLineEdit):
            input_field.setValidator(float_validator)
            input_field.textChanged.connect(self.sq_feet_calculator)
        self.main_modal_window.ui.sq_feet_input.setValidator(float_validator)
        self.main_modal_window.ui.asset_type_name_input.setValidator(
            validation.EmptyStrValidation(*self.fields["name"]["fields"])
        )

    def set_asset_page(self, asset_data):
        if asset_data:
            self.main_modal_window.asset_type_page_ui.set_update_asset(asset_data, self.update_asset, self.delete_asset)
        else:
            self.main_modal_window.asset_type_page_ui.set_add_asset(self.add_new_asset)
        self.main_modal_window.open()

    def add_new_asset(self):
        if self.validator.check_validation(self.fields):
            if self.check_dimension_fields():
                data = self.get_data()
                truck_type_api = TruckType(**data)
                response_code, response_data = truck_type_api.post()
                self.show_notification(response_code, response_data)

    def update_asset(self, asset_data):
        if self.validator.check_validation(self.fields):
            if self.check_dimension_fields():
                data = {"id": asset_data["id"]}
                data.update(self.get_data())
                truck_type_api = TruckType(**data)
                response_code, response_data = truck_type_api.put()
                self.show_notification(response_code, response_data)

    def delete_asset(self, asset_data):
        truck_type_api = TruckType(**asset_data)
        response_code, response_data = truck_type_api.delete()
        self.show_notification(response_code, response_data)

    def get_data(self):
        data = {
            "name": self.main_modal_window.ui.asset_name_input.text()
        }
        if self.main_modal_window.ui.sq_feet_input.text():
            data["dimension"] = self.main_modal_window.ui.sq_feet_input.text()
        else:
            data["length"] = self.main_modal_window.ui.length_input.text()
            data["weight"] = self.main_modal_window.ui.weight_input.text()
            data["height"] = self.main_modal_window.ui.height_input.text()
        return data

    def show_notification(self, response_code, response_data):
        if response_code > 399:
            self.main_modal_window.show_notification_page(
                response_data,
                is_error=True,
                previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                    self.main_modal_window.ui.asset_type_page
                )
            )
        else:
            self.main_modal_window.main_window.equipment_page.truck_type_update = True
            self.main_modal_window.main_window.ui.equipment_page.setVisible(False)
            self.main_modal_window.main_window.ui.equipment_page.setVisible(True)
            self.main_modal_window.show_notification_page(response_data, is_error=False)

    def sq_feet_calculator(self):
        total_sq_feet = 1
        for line_input in self.main_modal_window.ui.asset_type_dimension_frame.findChildren(QLineEdit):
            try:
                total_sq_feet *= float(line_input.text())
            except ValueError:
                total_sq_feet *= 1
        self.main_modal_window.ui.sq_feet_input.setText(str(total_sq_feet))

    def check_dimension_fields(self):
        all_fields_filled = True
        one_field_filled = True
        dimension_sum = 0
        error_fields = []
        self.main_modal_window.ui.error_dimension.setText("Enter asset dimensions or sq. feet size")
        for line_input in self.main_modal_window.ui.asset_type_dimension_frame.findChildren(QLineEdit):
            if line_input.text():
                dimension_sum *= float(line_input.text())
                all_fields_filled = False
                line_input.setProperty("error", False)
                line_input.setStyle(line_input.style())
            else:
                error_fields.append(line_input)
                if one_field_filled:
                    one_field_filled = False
        if not all_fields_filled:
            for line_input in error_fields:
                self.validator.change_field_style(line_input, self.main_modal_window.ui.error_dimension, True)
        if one_field_filled:
            return self.check_sq_with_dimension(dimension_sum)
        return any((all_fields_filled, one_field_filled))

    def check_sq_with_dimension(self, dimension_sum):
        if dimension_sum == float(self.main_modal_window.ui.sq_feet_input.text()):
            return True
        else:
            self.main_modal_window.ui.error_dimension.setText("Length * Width * Height not equal Sq feet")
            self.main_modal_window.ui.error_dimension.setVisible(True)
            return False

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.asset_type_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                return True
        return False
