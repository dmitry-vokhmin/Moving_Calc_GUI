class InventoryPageUi:
    def __init__(self, main_window):
        self.main_window = main_window

    def change_page_selector_style(self, is_all_inventory, button):
        self.main_window.ui.inventory_reset_btn.setVisible(not is_all_inventory)
        self.main_window.ui.inventory_all_menu_butt.setProperty("selected", is_all_inventory)
        self.main_window.ui.inventory_all_menu_butt.setStyle(self.main_window.ui.inventory_all_menu_butt.style())
        self.main_window.ui.inventory_preset_choose_butt.setProperty("selected", not is_all_inventory)
        self.main_window.ui.inventory_preset_choose_butt.setStyle(
            self.main_window.ui.inventory_preset_choose_butt.style()
        )
        self.main_window.ui.inventory_preset_choose_line.setVisible(not is_all_inventory)
        self.main_window.ui.inventory_all_menu_line.setVisible(is_all_inventory)
        self.main_window.ui.inventory_add_butt.setVisible(is_all_inventory)
        self.main_window.ui.inventory_save_butt.setVisible(not is_all_inventory)
        self.main_window.ui.inventory_categor_frame.setVisible(is_all_inventory)
        button.click()
