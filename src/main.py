from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("VCDL Version 0.0.1")
		button = QPushButton("Press Me!")

		self.setCentralWidget(button)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()