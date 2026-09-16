from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import Qt


class HorizontalScrollArea(QScrollArea):
    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            delta = event.angleDelta().y()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta
            )
            event.accept()
            return

        super().wheelEvent(event)