from PyQt5.QtWidgets import QWidget
from controller.validator import validation
from PyQt5.QtCore import QEvent
from model.user.user_client import UserClient
from model.zip_code import ZipCode
from model.address import Address
from model.order import Order
from model.inventory.inventory_order import InventoryOrder


class CalcPersonalInfoPage(QWidget):
    def __init__(self, main_window, calc_main_page):
        super().__init__()
        self.main_window = main_window
        self.calc_main_page = calc_main_page
        self.validation = validation.Validation()
        self.personal_info_fields = {
            "first_name": {
                "fields": (self.main_window.ui.calc_result_cus_info_f_name_input,
                           self.main_window.ui.calc_result_cus_info_error_f_name),
                "validator": validation.EmptyStrValidation
            },
            "last_name": {
                "fields": (self.main_window.ui.calc_result_cus_info_l_name_input,
                           self.main_window.ui.calc_result_cus_info_error_l_name),
                "validator": validation.EmptyStrValidation
            },
            "email": {
                "fields": (self.main_window.ui.calc_result_cus_info_email_input,
                           self.main_window.ui.calc_result_cus_info_error_email),
                "validator": validation.EmailValidation
            },
            "phone": {
                "fields": (self.main_window.ui.calc_result_cus_info_phone_input,
                           self.main_window.ui.calc_result_cus_info_error_phone),
                "validator": validation.PhoneValidation
            },
        }
        self.main_window.ui.calc_result_customer_info_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        for field in self.personal_info_fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))

    def submit_form(self, move_details, inventory_preset, calc_result):
        if self.validation.check_validation(self.personal_info_fields):
            personal_data = self.get_personal_info()
            customer = self.get_or_post_data(UserClient, personal_data, is_get=False)
            zip_code_to = self.get_or_post_data(ZipCode, {"zip_code": move_details["zip_code_to"]}, is_get=True)
            zip_code_from = self.get_or_post_data(ZipCode, {"zip_code": move_details["zip_code_from"]},
                                                  is_get=True)
            address_from_data = self.get_address_info(self.main_window.ui.calc_result_cus_info_adr_from_1_input,
                                                      self.main_window.ui.calc_result_cus_info_adr_from_2_input,
                                                      zip_code_from["id"])
            address_to_data = self.get_address_info(self.main_window.ui.calc_result_cus_info_adr_to_1_input,
                                                    self.main_window.ui.calc_result_cus_info_adr_to_2_input,
                                                    zip_code_to["id"])
            address_from = self.get_or_post_data(Address, address_from_data, is_get=False)
            address_to = self.get_or_post_data(Address, address_to_data, is_get=False)
            order_data = self.get_order_data(customer["id"], address_from["id"],
                                             address_to["id"], move_details, calc_result)
            order = self.get_or_post_data(Order, order_data, is_get=False)
            inventory_order_data = self.get_inventory_for_order(order["id"], inventory_preset)
            inventory_order = InventoryOrder(**inventory_order_data)
            response_code, response_data = inventory_order.post()
            if response_code > 399:
                self.main_window.modal_window.show_notification_page(response_data, is_error=True)
            else:
                self.calc_main_page.reset_pages()
                self.main_window.modal_window.show_notification_page(response_data, is_error=False)

    def get_inventory_for_order(self, order_id, preset_inventory):
        return {
            "inventory": {
                move_size: [
                    {"inventory_id": inv["inventory_id"], "count": inv["count"]} for inv in value["inventory"]
                ] for move_size, value in preset_inventory.items()
            },
            "order_id": order_id
        }

    def get_order_data(self, user_id, address_from_id, address_to_id, move_details, calc_result):
        return {
            "move_date": move_details["move_date"].isoformat(),
            "hourly_rate": calc_result["hourly_rate"],
            "estimated_cost": "-".join([str(elem) for elem in calc_result["estimated_quote"]]),
            "estimated_hours": "-".join([str(elem) for elem in calc_result["estimated_job_time"]]),
            "crew_size": calc_result["crew_size"],
            "truck_size": calc_result["truck_size"],
            "travel_time": calc_result["travel_time"],
            "user_id": user_id,
            "address_from_id": address_from_id,
            "address_to_id": address_to_id,
            "move_size_id_list": [move_size[1] for move_size in move_details["move_size"]],
            "service_id": 1,
            "floor_collection_from_id": move_details["floor_collection_from"][1],
            "floor_collection_to_id": move_details["floor_collection_to"][1]
        }

    def get_or_post_data(self, endpoint, data, is_get):
        api_endpoint = endpoint(**data)
        if is_get:
            response_code, response_data = api_endpoint.get()
        else:
            response_code, response_data = api_endpoint.post()
        if response_code > 399:
            print(response_data)
        else:
            return response_data

    def get_personal_info(self):
        return {
            "firstname": self.main_window.ui.calc_result_cus_info_f_name_input.text().lower(),
            "lastname": self.main_window.ui.calc_result_cus_info_l_name_input.text().lower(),
            "email": self.main_window.ui.calc_result_cus_info_email_input.text().lower(),
            "phone_number": self.main_window.ui.calc_result_cus_info_phone_input.text().lower(),
        }

    def get_address_info(self, address_1, address_2, zip_code_id):
        return {
            "street": address_1.text().lower(),
            "apartment": address_2.text().lower(),
            "zip_code_id": zip_code_id
        }

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.calc_result_customer_info_page:
            if event.type() == QEvent.Show:
                self.validation.reset_error_fields(self.personal_info_fields)
                return True
        return False
