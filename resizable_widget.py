import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, QSize
from PIL import Image
from PIL.ImageQt import ImageQt


class ResizableImageWidget(QWidget):
    """
    A QWidget that displays an image and automatically scales it to fit
    the widget's size while preserving the aspect ratio.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap()
        self.setMinimumSize(50, 50)  # Set a minimum size

    def set_from_pillow_image(self, pil_image):
        # 2. Convert PIL Image to QPixmap
        qt_image = ImageQt(pil_image)
        self.pixmap = QPixmap.fromImage(qt_image)
        # Request a repaint to draw the new image
        self.update()

    def paintEvent(self, event):
        """Overrides the standard paint event to handle image scaling and drawing."""
        if self.pixmap.isNull():
            return

        painter = QPainter(self)

        # Get the size of the current widget
        widget_size = self.size()

        # 1. Scale the QPixmap to fit the widget size while preserving the aspect ratio.
        #    Qt.KeepAspectRatio: maintains the original ratio.
        #    Qt.SmoothTransformation: uses a high-quality scaling algorithm.
        scaled_pixmap = self.pixmap.scaled(
            widget_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )

        # 2. Calculate the top-left position to center the scaled image.
        #    If the widget is wider than the image, center horizontally.
        #    If the widget is taller than the image, center vertically.
        x = (widget_size.width() - scaled_pixmap.width()) // 2
        y = (widget_size.height() - scaled_pixmap.height()) // 2

        # 3. Draw the centered, scaled image
        painter.drawPixmap(x, y, scaled_pixmap)
