# ui/widgets/completion_window/exit_button.py

from PySide6.QtWidgets import QApplication, QPushButton


class ExitButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Exit App", parent)

        self.clicked.connect(self.exit_app)

    def exit_app(self):
        QApplication.quit()
