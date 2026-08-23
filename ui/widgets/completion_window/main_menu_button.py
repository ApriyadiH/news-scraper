# ui\widgets\completion_window\main_menu_button.py

from PySide6.QtWidgets import QPushButton

class MainMenuButton(QPushButton):
    def __init__(self, main_window=None, completion_window=None, parent=None):
        super().__init__("Back to Main Menu", parent)

        self.main_window = main_window
        self.completion_window = completion_window
        
        self.clicked.connect(self.go_to_main_menu)

    def go_to_main_menu(self):
        if self.completion_window:
            self.completion_window.close()

        if self.main_window:
            self.main_window.showNormal()
            self.main_window.raise_()
            self.main_window.activateWindow()