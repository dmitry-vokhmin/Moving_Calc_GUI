from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from model.truck.truck import Truck
from controller.validator import validation


class AssetPage(QDialog):
    def __init__(self, main_modal_window):
        QDialog.__init__(self, main_modal_window)
        self.main_modal_window = main_modal_window
        self.validator = validation.Validation()
        self.fields = {
            "name": {
                "fields": (self.main_modal_window.ui.asset_type_name_input,
                           self.main_modal_window.ui.error_asset_name)
            },
        }
        self.main_modal_window.ui.cancel_asset_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.asset_add_asset_type.clicked.connect(
            lambda: self.main_modal_window.ui.pages.setCurrentWidget(self.main_modal_window.ui.asset_type_page)
        )
        self.main_modal_window.ui.asset_name_input.setValidator(
            validation.EmptyStrValidation(*self.fields["name"]["fields"])
        )
        self.main_modal_window.ui.asset_add_asset_type.installEventFilter(self)
        self.main_modal_window.ui.asset_page.installEventFilter(self)

    def set_asset_page(self, asset_data):
        if asset_data:
            self.main_modal_window.asset_page_ui.set_update_asset(asset_data, self.update_asset, self.delete_asset)
        else:
            self.main_modal_window.asset_page_ui.set_add_asset(self.add_new_asset)
        self.main_modal_window.open()

    def add_new_asset(self):
        if self.validator.check_validation(self.fields):
            data = self.get_data()
            truck_api = Truck(**data)
            response_code, response_data = truck_api.post()
            self.show_notification(response_code, response_data)

    def update_asset(self, asset_data):
        if self.validator.check_validation(self.fields):
            data = {"id": asset_data["id"]}
            data.update(self.get_data())
            truck_api = Truck(**data)
            response_code, response_data = truck_api.put()
            self.show_notification(response_code, response_data)

    def delete_asset(self, asset_data):
        truck_api = Truck(**asset_data)
        response_code, response_data = truck_api.delete()
        self.show_notification(response_code, response_data)

    def get_data(self):
        return {
            "name": self.main_modal_window.ui.asset_name_input.text(),
            "truck_type_id": self.main_modal_window.ui.asset_type_combobox.currentData()
        }

    def show_notification(self, response_code, response_data):
        if response_code > 399:
            self.main_modal_window.show_notification_page(
                response_data,
                is_error=True,
                previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                    self.main_modal_window.ui.asset_page
                )
            )
        else:
            self.main_modal_window.main_window.equipment_page.truck_update = True
            self.main_modal_window.main_window.ui.equipment_page.setVisible(False)
            self.main_modal_window.main_window.ui.equipment_page.setVisible(True)
            self.main_modal_window.show_notification_page(response_data, is_error=False)

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.asset_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                return True
        if obj is self.main_modal_window.ui.asset_add_asset_type:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/round_plus_icon_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/round_plus_icon_default.svg"))
                return True
        return False
