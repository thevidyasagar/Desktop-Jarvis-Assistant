import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SARA State View")
        self.resize(600, 400)
        self.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.status_label = QLabel("SYSTEM IDLE")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        layout.addWidget(self.status_label)
        
        self.info_label = QLabel("Minimal Mode Active")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px; color: gray;")
        layout.addWidget(self.info_label)

    def paintEvent(self, event):
        # Traditional simple UI doesn't need custom painting
        pass

def start_ui():
    app = QApplication(sys.argv)
    ui = JarvisUI()
    ui.show()
    sys.exit(app.exec())
