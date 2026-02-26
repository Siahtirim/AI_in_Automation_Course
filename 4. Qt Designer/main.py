import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("mainwindow.ui")

        if not ui_file.open(QFile.ReadOnly):
            print("Cannot open UI file")
            return

        self.ui = loader.load(ui_file)
        ui_file.close()

        if not self.ui:
            print("UI failed to load")
            return

        self.setCentralWidget(self.ui)

        # اتصال دکمه
        self.ui.UI_Cal.clicked.connect(self.check_age)

    def check_age(self):
        try:
            age = int(self.ui.UI_Age.text())

            if age > 18:
                self.ui.UI_Out.setText("You are old enough!")
                self.ui.UI_Out.setStyleSheet("color: green;")
            elif age == 18:
                self.ui.UI_Out.setText("You are exactly 18!")
                self.ui.UI_Out.setStyleSheet("color: orange;")
            else:
                self.ui.UI_Out.setText("You are too young!")
                self.ui.UI_Out.setStyleSheet("color: red;")

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())