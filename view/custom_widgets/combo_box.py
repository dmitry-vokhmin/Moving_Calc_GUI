from PyQt5.QtWidgets import QComboBox as qcombobox
from typing import Any


class QComboBox(qcombobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def addItem(self, str, userData: Any = None):
        if str not in self.get_set_items():
            super(QComboBox, self).addItem(str, userData)

    def get_set_items(self):
        return set([self.itemText(i) for i in range(self.count())])
