import sys

from PIL import Image

# You need to import ImageQt explicitly for the conversion function
from PIL.ImageQt import ImageQt
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from resizable_widget import ResizableImageWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Image Editor by Eyad Senosy, Supervisor Phd.Prof.MarianWagdy")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.pil_image = None

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open an existing file.")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        central_widget = QWidget()
        central_widget_layout = QHBoxLayout()
        central_widget.setLayout(central_widget_layout)
        self.setCentralWidget(central_widget)

        operations_widget = QWidget()
        operations_widget_layout = QVBoxLayout()
        operations_widget.setLayout(operations_widget_layout)
        central_widget_layout.addWidget(operations_widget)

        self.image_viewer = ResizableImageWidget()
        central_widget_layout.addWidget(self.image_viewer)

        self.rotate_pushbutton = QPushButton("Rotate 45")
        operations_widget_layout.addWidget(self.rotate_pushbutton)
        self.rotate_pushbutton.clicked.connect(self.rotate_45)

        self.rotate_pushbutton = QPushButton("Rotate 90")
        operations_widget_layout.addWidget(self.rotate_pushbutton)
        self.rotate_pushbutton.clicked.connect(self.rotate_90)

        operations_widget_layout.addStretch()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an image file", "", "Image Files (*.png *.jpg *.jpeg)")
        try:
            self.pil_image = Image.open(file_path)
            self.image_viewer.set_from_pillow_image(self.pil_image)
        except FileNotFoundError:
            print(f"Error: Image file not found at {file_path}")
        except Exception as e:
            print(f"Error loading or converting image: {e}")

    def rotate_45(self):
        if self.pil_image is None:
            return
        self.pil_image = self.pil_image.rotate(45)
        self.image_viewer.set_from_pillow_image(self.pil_image)

    def rotate_90(self):
        if self.pil_image is None:
            return
        self.pil_image = self.pil_image.rotate(90)
        self.image_viewer.set_from_pillow_image(self.pil_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
