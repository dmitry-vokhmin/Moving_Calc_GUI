from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget
from model.company import Company
from controller.validator import validation


class RegistrationCompanyPage(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self, main_window)
        self.main_window = main_window
        self.validation = validation.Validation()
        self.company_id = None
        self.fields = {
            "name": {
                "fields": (self.main_window.ui.reg_comp_name_input, self.main_window.ui.reg_comp_error_name),
                "validator": validation.EmptyStrValidation
            },
            "address1": {
                "fields": (self.main_window.ui.reg_comp_address1_input, self.main_window.ui.reg_comp_address1_error),
                "validator": validation.EmptyStrValidation
            },
            "city": {
                "fields": (self.main_window.ui.reg_comp_city_input, self.main_window.ui.reg_comp_city_error),
                "validator": validation.EmptyStrValidation
            },
            "state": {
                "fields": (self.main_window.ui.reg_comp_state_input,self.main_window.ui.reg_comp_state_error),
                "validator": validation.EmptyStrValidation
            },
            "zip_code": {
                "fields": (self.main_window.ui.reg_comp_zipcode_input, self.main_window.ui.reg_comp_zipcode_error),
                "validator": validation.ZipValidation
            },
        }
        self.main_window.ui.reg_comp_sign_but.clicked.connect(
            lambda: self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.login_page)
        )
        self.main_window.ui.reg_comp_next_butt.clicked.connect(self.registration_company)
        self.main_window.ui.registration_company_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        for field in self.fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))

    def registration_company(self):
        if self.validation.check_validation(self.fields):
            company_data = self.get_company_data()
            company = Company(**company_data)
            response_code, response_data = company.post()
            if response_code > 399:
                self.main_window.registration_error(response_data)
                self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.acc_created_error_page)
            else:
                self.company_id = response_data["id"]
                self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.registration_page)

    def get_company_data(self):
        return {
            "name": self.main_window.ui.reg_comp_name_input.text(),
            "street": self.main_window.ui.reg_comp_address1_input.text(),
            "apartment": self.main_window.ui.reg_comp_address2_input.text(),
            "zip_code": self.main_window.ui.reg_comp_zipcode_input.text(),
            "city": self.main_window.ui.reg_comp_city_input.text(),
            "state": self.main_window.ui.reg_comp_state_input.text()
        }

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.registration_company_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.validation.reset_error_fields(self.fields)
                return True
        return False
