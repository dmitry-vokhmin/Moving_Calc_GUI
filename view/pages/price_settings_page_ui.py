from PyQt5.QtWidgets import QVBoxLayout, QFrame, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QSize, Qt
from model.price import Price


class PriceSettingsPage:
    def __init__(self, main_window):
        self.main_window = main_window
        self.price = Price()

    def set_movers_prices(self, price_tag_id, is_update_price=False):
        if is_update_price:
            self.main_window.get_data(self.price.get)
        self.main_window.delete_layout(self.main_window.ui.config_clear_frame.layout())
        config_clear_layout = QVBoxLayout(self.main_window.ui.config_clear_frame)
        config_clear_layout.setContentsMargins(0, 0, 0, 0)
        config_clear_layout.setSpacing(0)
        background_gray = True
        for mover in self.main_window.mover_amount.movers:
            main_frame = QFrame(self.main_window.ui.config_clear_frame)
            main_frame.setMinimumSize(QSize(0, 54))
            if background_gray:
                main_frame.setStyleSheet("QFrame {\n"
                                         "    background: #F2F3F6;\n"
                                         "    border-radius: 4px;\n"
                                         "}")
            background_gray = not background_gray
            main_frame.setFrameShape(QFrame.NoFrame)
            main_layout = QHBoxLayout(main_frame)
            main_layout.setContentsMargins(0, 0, 80, 0)
            main_layout.setSpacing(7)
            movers_frame = QFrame(main_frame)
            movers_frame.setFrameShape(QFrame.NoFrame)
            movers_layout = QHBoxLayout(movers_frame)
            movers_layout.setContentsMargins(17, 0, 0, 0)
            movers_layout.setSpacing(7)
            icon = QLabel(movers_frame)
            icon.setMinimumSize(QSize(22, 22))
            icon.setMaximumSize(QSize(20, 20))
            icon.setStyleSheet(" image: url(:/image/config_users_icon.svg);")
            icon.setText("")
            icon.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
            movers_layout.addWidget(icon)
            movers_amount = QLabel(movers_frame)
            movers_amount.setText(f"{mover['amount']} movers")
            movers_layout.addWidget(movers_amount)
            main_layout.addWidget(movers_frame, 0, Qt.AlignLeft)
            currency_icon = QLabel(main_frame)
            currency_icon.setMinimumSize(QSize(20, 8))
            currency_icon.setStyleSheet(" image: url(:/image/currency_icon.svg);")
            currency_icon.setText("")
            main_layout.addWidget(currency_icon, 0, Qt.AlignRight)
            price = QLineEdit(main_frame)
            price.setMinimumSize(QSize(96, 38))
            price.setMaximumSize(QSize(96, 38))
            price_db = self.price_id(mover, price_tag_id)
            if not price_db or price_db["price"] == 0.0:
                price.setText("0.00")
                price.__setattr__("mover_amount_id", mover["id"])
                price.setStyleSheet("color: #B5B8C7;")
                currency_icon.setStyleSheet(" image: url(:/image/currency_icon_disabled.svg);")
            elif price_db:
                price.setText(f'{price_db["price"]:.2f}')
                price.__setattr__("mover_amount_id", price_db["mover_amount_id"])
            price.setEnabled(False)
            main_layout.addWidget(price, 0, Qt.AlignRight)
            main_layout.setStretch(0, 1)
            config_clear_layout.addWidget(main_frame)

    def price_id(self, mover, price_tag_id):
        for price in self.price.prices:
            if price["mover_amount_id"] == mover["id"] and price["price_tag_id"] == price_tag_id:
                return price
