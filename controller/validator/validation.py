import re
from PyQt5.QtGui import QValidator


class Validation(QValidator):
    def __init__(self, input_field=None, error_field=None):
        QValidator.__init__(self)
        self.input_field = input_field
        self.error_field = error_field

    @staticmethod
    def change_field_style(input_field, error_field, status: bool):
        error_field.setVisible(status)
        input_field.setProperty("error", status)
        input_field.setStyle(input_field.style())

    def reset_error_fields(self, fields):
        for field in fields.values():
            self.change_field_style(field["fields"][0], field["fields"][1], False)

    def check_validation(self, fields):
        is_valid = True
        for field in fields.values():
            if not field["fields"][0].hasAcceptableInput():
                self.change_field_style(field["fields"][0], field["fields"][1], True)
                is_valid = False
            else:
                self.change_field_style(field["fields"][0], field["fields"][1], False)
        return is_valid

    def fixup(self, text: str) -> str:
        self.change_field_style(self.input_field, self.error_field, True)
        return text


class PasswordValidation(Validation):
    def validate(self, text: str, pos: int):
        reg_exp = re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"), text)
        if reg_exp:
            self.change_field_style(self.input_field, self.error_field, False)
            return QValidator.Acceptable, text, pos
        else:
            return QValidator.Intermediate, text, pos


class Password2Validation(Validation):
    def __init__(self, input_field, error_field, pass1_field):
        Validation.__init__(self, input_field, error_field)
        self.pass1_field = pass1_field

    def validate(self, text: str, pos: int):
        if self.pass1_field.text() == self.input_field.text():
            self.change_field_style(self.input_field, self.error_field, False)
            return QValidator.Acceptable, text, pos
        else:
            return QValidator.Intermediate, text, pos


class EmptyStrValidation(Validation):
    def validate(self, text: str, pos: int):
        if self.input_field.text():
            self.change_field_style(self.input_field, self.error_field, False)
            return QValidator.Acceptable, text, pos
        else:
            return QValidator.Intermediate, text, pos


class EmailValidation(Validation):
    def validate(self, text: str, pos: int):
        reg_exp = re.search(re.compile('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'), text)
        if reg_exp:
            self.change_field_style(self.input_field, self.error_field, False)
            return QValidator.Acceptable, text, pos
        else:
            return QValidator.Intermediate, text, pos