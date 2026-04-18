import sys
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

from core.assistant import AssistantCore
from voice.speak import speak
from voice.listen import listen

class TaskWorker(QThread):
    finished = pyqtSignal(str, str) # user_text, bot_response
    status = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, assistant, task_type, text=None):
        super().__init__()
        self.assistant = assistant
        self.task_type = task_type
        self.text = text

    def run(self):
        try:
            if self.task_type == "text":
                self.status.emit("Thinking...")
                response = self.assistant.process_text(self.text)
                self.finished.emit(self.text, response)
            elif self.task_type == "voice":
                self.status.emit("Listening...")
                command, lang = listen()
                if command:
                    self.status.emit("Thinking...")
                    response = self.assistant.process_text(command, lang)
                    self.finished.emit(command, response)
                else:
                    self.finished.emit("", "")
            elif self.task_type == "speak":
                self.status.emit("Speaking...")
                speak(self.text)
                self.status.emit("Idle")
        except Exception as e:
            err_msg = traceback.format_exc()
            print(f"❌ Worker Error: {err_msg}")
            self.error.emit(str(e))

class MessageBubble(QFrame):
    def __init__(self, text, is_user=True):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.label)
        
        # Simple, clean styling
        if is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #E3F2FD;
                    border: 1px solid #BBDEFB;
                    border-radius: 10px;
                }
                QLabel { color: #0D47A1; font-size: 13px; }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #F5F5F5;
                    border: 1px solid #E0E0E0;
                    border-radius: 10px;
                }
                QLabel { color: #212121; font-size: 13px; }
            """)

class JarvisUI(QMainWindow):
    def __init__(self, assistant_core):
        super().__init__()
        self.assistant = assistant_core
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SARA Assistant")
        self.resize(500, 700)
        
        # Set system default/white background
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.white)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Header Label
        self.title_label = QLabel("SARA Assistant")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-bottom: 10px;")
        self.main_layout.addWidget(self.title_label)

        # Status Label
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("color: #666; font-size: 11px;")
        self.main_layout.addWidget(self.status_label)

        # Chat Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.StyledPanel)
        
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: white;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.addStretch()
        self.scroll.setWidget(self.chat_container)
        
        self.main_layout.addWidget(self.scroll)

        # Input Area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;")
        self.input_field.returnPressed.connect(self.handle_send)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("padding: 8px 15px; background-color: #2196F3; color: white; border: none; border-radius: 4px; font-weight: bold;")
        self.send_btn.clicked.connect(self.handle_send)
        
        self.mic_btn = QPushButton("🎤")
        self.mic_btn.setFixedSize(40, 40)
        self.mic_btn.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 20px; font-size: 18px;")
        self.mic_btn.clicked.connect(self.handle_mic)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        input_layout.addWidget(self.mic_btn)
        
        self.main_layout.addLayout(input_layout)

    def add_message(self, text, is_user=True):
        if not text: return
        bubble = MessageBubble(text, is_user)
        bubble_layout = QHBoxLayout()
        if is_user:
            bubble_layout.addStretch()
            bubble_layout.addWidget(bubble)
        else:
            bubble_layout.addWidget(bubble)
            bubble_layout.addStretch()
        
        # Insert before the stretch
        count = self.chat_layout.count()
        self.chat_layout.insertLayout(count - 1, bubble_layout)
        
        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def update_status(self, msg):
        self.status_label.setText(f"Status: {msg}")

    def handle_send(self):
        text = self.input_field.text().strip()
        if not text: return
        self.input_field.clear()
        self.add_message(text, is_user=True)
        self.run_task("text", text)

    def handle_mic(self):
        self.run_task("voice")

    def run_task(self, task_type, text=None):
        self.worker = TaskWorker(self.assistant, task_type, text)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.handle_finished)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

    def handle_error(self, err):
        self.add_message(f"Error: {err}", is_user=False)
        self.update_status("Error")

    def handle_finished(self, user_text, bot_response):
        if user_text and self.sender().task_type == "voice":
            self.add_message(user_text, is_user=True)
        
        if bot_response == "EXIT_SIGNAL":
            self.add_message("Goodbye! System offline.", is_user=False)
            speak("Goodbye Sir. System offline.")
            QTimer.singleShot(2000, self.close)
            return

        if bot_response:
            self.add_message(bot_response, is_user=False)
            self.run_task("speak", bot_response)
        
        self.update_status("Idle")
