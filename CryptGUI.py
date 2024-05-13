import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QHBoxLayout, QRadioButton
from CryptImg import process_image

class ToggleButton(QRadioButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QRadioButton {
                color: #CECECE;
            }
        """)
        self.toggled.connect(self.update_text_color)

    def update_text_color(self):
        if self.isChecked():
            self.setStyleSheet("color: #CECECE;")
        else:
            self.setStyleSheet("color: #5E5E5E;")

class CryptGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Cryptography Tool")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet("background-color: #303036;")

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        # Mode Selector
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("color: #CECECE;")
        layout.addWidget(mode_label)

        mode_layout = QHBoxLayout()

        self.encrypt_radio = ToggleButton("Encryption")
        self.encrypt_radio.setChecked(True)
        self.encrypt_radio.toggled.connect(self.update_mode)
        mode_layout.addWidget(self.encrypt_radio)

        self.decrypt_radio = ToggleButton("Decryption")
        self.decrypt_radio.toggled.connect(self.update_mode)
        mode_layout.addWidget(self.decrypt_radio)

        layout.addLayout(mode_layout)

        # Key Entry
        key_label = QLabel("Key:")
        key_label.setStyleSheet("color: #CECECE;")
        layout.addWidget(key_label)
        self.key_entry = QLineEdit()
        self.key_entry.setStyleSheet("background-color: #FFFAFF; color: #050401;")
        layout.addWidget(self.key_entry)

        # Image Path Entry
        image_path_label = QLabel("Image Path:")
        image_path_label.setStyleSheet("color: #CECECE;")
        layout.addWidget(image_path_label)
        self.image_path_entry = QLineEdit()
        self.image_path_entry.setReadOnly(True)
        self.image_path_entry.setStyleSheet("background-color: #FFFAFF; color: #050401;")
        layout.addWidget(self.image_path_entry)
        self.image_path_button = QPushButton("Paste")
        self.image_path_button.clicked.connect(self.paste_file_path)
        self.image_path_button.setStyleSheet("background-color: #006666; color: #CECECE;")
        layout.addWidget(self.image_path_button)

        # Output Folder Entry
        output_label = QLabel("Output Folder:")
        output_label.setStyleSheet("color: #CECECE;")
        layout.addWidget(output_label)
        self.output_entry = QLineEdit()
        self.output_entry.setStyleSheet("background-color: #FFFAFF; color: #050401;")
        layout.addWidget(self.output_entry)
        self.output_button = QPushButton("Choose Folder")
        self.output_button.clicked.connect(self.choose_output_path)
        self.output_button.setStyleSheet("background-color: #006666; color: #CECECE;")
        layout.addWidget(self.output_button)

        # Run Button
        run_button = QPushButton("Run Program")
        run_button.clicked.connect(self.run_cryptimg)
        run_button.setStyleSheet("background-color: #006666; color: #CECECE;")
        layout.addWidget(run_button)

        self.setLayout(layout)

    def paste_file_path(self):
        clipboard = QApplication.clipboard()
        file_path = clipboard.text()
        if file_path:
            self.image_path_entry.setText(file_path)

    def choose_output_path(self):
        output_path = QFileDialog.getExistingDirectory(self, "Choose Output Folder")
        if output_path:
            self.output_entry.setText(output_path)

    def update_mode(self):
        sender = self.sender()
        if sender == self.encrypt_radio:
            self.decrypt_radio.setChecked(False)
        elif sender == self.decrypt_radio:
            self.encrypt_radio.setChecked(False)


    def run_cryptimg(self):
        method = "E" if self.encrypt_radio.isChecked() else "D"
        key = self.key_entry.text()
        image_path = self.image_path_entry.text()
        output_path = self.output_entry.text()

        # Validate inputs
        if method not in ['E', 'D']:
            QMessageBox.critical(self, "Error", "Invalid method. Use 'E' for encryption or 'D' for decryption.")
            return

        if not key:
            QMessageBox.critical(self, "Error", "Please enter a key.")
            return

        if not image_path:
            QMessageBox.critical(self, "Error", "Please choose an image.")
            return

        if not output_path:
            QMessageBox.critical(self, "Error", "Please choose an output directory.")
            return

        # Call process_image function
        process_image(method, key, image_path, output_path)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CryptGUI()
    gui.show()
    sys.exit(app.exec())
