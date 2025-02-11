import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.button = QPushButton("Click Me", self)
        self.button.clicked.connect(self.showMessage)

        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setWindowTitle("Basic PyQt App")
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showMessage(self):
        QMessageBox.information(self, "Message", "Hello, PyQt!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
