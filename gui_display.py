import sys
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QRectF

class BatteryMonitorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAV Battery Monitoring Station")
        self.setGeometry(100, 100, 900, 500)
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Get current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Date and Ambient Temperature Label
        self.date_temp_label = QLabel(f"{current_date} | Temp: 30°F", self)
        self.date_temp_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.date_temp_label.setGeometry(600, 20, 280, 40)
        self.date_temp_label.setStyleSheet("color: white;")  # Set text color to white
        
        # Set Central Widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set background to black
        painter.fillRect(self.rect(), QColor(Qt.GlobalColor.black))
        
        battery_x = 50  # Initial X position
        battery_y = 150 # Y position for all batteries
        battery_width = 60
        battery_height = 100
        spacing = 80  # Space between batteries

        battery_data = [
            {"charge": 73, "connected": True, "Done": False, "amperage": 2.83},
            {"charge": 0, "connected": False, "Done": False, "amperage": 0},
            {"charge": 100, "connected": True, "Done": False, "amperage": 0},
            {"charge": 0, "connected": False, "Done": False, "amperage": 0},
            {"charge": 0, "connected": False, "Done": False, "amperage": 0},
            {"charge": 20, "connected": True, "Done": False, "amperage": 3.21},
            {"charge": 0, "connected": False, "Done": False, "amperage": 0},
            {"charge": 0, "connected": False, "Done": False, "amperage": 0},
        ]
        
        for i, battery in enumerate(battery_data):
            x = battery_x + (i * spacing)
            self.drawBattery(painter, x, battery_y, battery_width, battery_height, battery, i)
            
            # Draw separator line between batteries
            if i < len(battery_data) - 1:
                painter.setPen(QPen(Qt.GlobalColor.white, 1))
                painter.drawLine(x + battery_width + 10, battery_y, x + battery_width + 10, battery_y + battery_height + 50)

    def drawBattery(self, painter, x, y, width, height, battery, index):
        # Draw Battery Outline
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.drawRect(x, y, width, height)
        
        # Draw Battery Fill Based on Charge or Leave Blank
        charge_level = battery["charge"]
        if battery["connected"] and charge_level > 0:
            fill_height = (charge_level / 100) * height
            color = QColor("green") if charge_level > 50 else QColor("red")
            painter.setBrush(QBrush(color))
            painter.drawRect(QRectF(x, y + (height - fill_height), width, fill_height))
        
        else:
            painter.setBrush(QBrush(QColor(Qt.GlobalColor.black)))
            painter.drawRect(x, y, width, height)
        
        # Draw Battery Label
        label_text = f"B{index+1}"
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(x + 25, y - 10, label_text)
        charge_level = battery["charge"]
        amp_level = battery["amperage"]
        if battery["connected"] and charge_level < 100:
            painter.drawText(x, y + height + 15, "Connected")
            painter.drawText(x + 20, y + height + 30, f"{charge_level}%")
            painter.drawText(x+13, y + height + 45, f"{amp_level} (A)")



        if battery["connected"] and charge_level == 100:
            battery["Done"] = True
            painter.drawText(x + 15, y + height + 15, "Done!")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BatteryMonitorUI()
    window.show()
    sys.exit(app.exec())
