# import sys
# import math
# from PySide6.QtWidgets import QApplication, QWidget
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QPainter, QColor, QPainterPath, QPen


# class JarvisBlob(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("JARVIS USER INTERFACE")
#         self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
#         self.showMaximized()
#         self.setAttribute(Qt.WA_TranslucentBackground)

#         self.t = 0.0

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(16)  # ~60 FPS

#     def keyPressEvent(self, event):
#         if event.key() in (Qt.Key_Escape, Qt.Key_Q):
#             self.close()

#     def update_frame(self):
#         self.t += 0.02   # 🔥 rings move faster
#         self.update()

#     def paintEvent(self, event):
#         p = QPainter(self)
#         p.setRenderHint(QPainter.Antialiasing)
#         p.fillRect(self.rect(), QColor(0, 0, 0))

#         cx, cy = self.width() // 2, self.height() // 2

#         # 🔵 PERFECT CENTER CIRCLE (unchanged)
#         base_radius = min(self.width(), self.height()) * 0.26

#         total_rings = 60  # ✅ reduced rings

#         for layer in range(total_rings):
#             path = QPainterPath()

#             phase = self.t * (1 + layer * 0.015)

#             # 🔥 STRONGER RING MOTION
#             amp1 = 22
#             amp2 = 14
#             amp3 = 8

#             points = []
#             for i in range(0, 360, 5):
#                 a = math.radians(i)

#                 r = base_radius
#                 r += math.sin(a * 2 + phase) * amp1
#                 r += math.cos(a * 3 - phase * 1.4) * amp2
#                 r += math.sin(phase * 1.8 + layer * 0.3) * amp3

#                 x = cx + math.cos(a) * r
#                 y = cy + math.sin(a) * r
#                 points.append((x, y))

#             path.moveTo(points[0][0], points[0][1])
#             for x, y in points[1:]:
#                 path.lineTo(x, y)
#             path.closeSubpath()

#             alpha = 30 + (layer % 20) * 3
#             color = QColor(0, 185, 255, alpha)

#             p.setPen(QPen(color, 0.9))
#             p.drawPath(path)

#         # 🌌 CORE GLOW (unchanged, perfect)
#         for i in range(6):
#             glow_radius = base_radius * (0.55 + i * 0.07)
#             glow = QPainterPath()
#             glow.addEllipse(
#                 cx - glow_radius,
#                 cy - glow_radius,
#                 glow_radius * 2,
#                 glow_radius * 2
#             )

#             p.setPen(Qt.NoPen)
#             p.setBrush(QColor(0, 185, 255, 35 - i * 4))
#             p.drawPath(glow)


# def start_ui():
#     app = QApplication(sys.argv)
#     ui = JarvisBlob()
#     ui.show()
#     sys.exit(app.exec())



from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QTimer
from ui.ui_state import get_ui_data

class JarvisUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VEDA")
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        state, user_text, ai_text = get_ui_data()

        # STATUS
        painter.setPen(QColor(0, 255, 255))
        painter.setFont(QFont("Consolas", 22))
        painter.drawText(40, 50, f"STATUS : {state.value}")

        # USER SAID
        painter.setFont(QFont("Consolas", 16))
        painter.drawText(40, 100, f"YOU : {user_text}")

        # AI RESPONSE
        painter.setPen(QColor(0, 200, 255))
        painter.drawText(40, 140, f"VEDA : {ai_text}")

        painter.end()
