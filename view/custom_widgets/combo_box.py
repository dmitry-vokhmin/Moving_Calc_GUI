from PyQt5.QtWidgets import QComboBox
from typing import Any


class ComboBox(QComboBox):
    def addItem(self, str, userData: Any = None):
        if str not in self.get_set_items():
            super(ComboBox, self).addItem(str, userData)

    def get_set_items(self):
        return set([self.itemText(i) for i in range(self.count())])
