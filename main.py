import sys
import json
from pathlib import Path
from datetime import datetime
import requests
from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,  # 추가됨
    QLabel,
    QPushButton   # 추가됨
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class ConfigManager:
    def __init__(self):
        self.config_file = Path("config.json")
        self.default_config = {
            "update_interval": 300000,  # 5 minutes in milliseconds
            "last_position": {"x": 100, "y": 100}
        }
        self.config = self.load_config()

    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_config.copy()
        return self.default_config.copy()

    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

class WeatherAPI:
    def __init__(self, city="Seoul"):
        self.api_key = os.getenv('WEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        self.city = city
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self):
        try:
            params = {
                "q": self.city,
                "APPID": self.api_key,
                "units": "metric",
                "lang": "kr"
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"날씨 정보 가져오기 실패: {e}")
            return None

class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        
        try:
            self.weather_api = WeatherAPI("Seoul")
        except ValueError as e:
            print(e)
            sys.exit(1)
            
        self.init_ui()
        self.setup_timer()
        self.restore_position()
        
    def init_ui(self):
        # Window settings
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title bar with close button
        title_bar = QWidget()
        title_bar.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.7);
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 5, 5, 0)
        
        # Spacer to push close button to right
        title_layout.addStretch()
        
        # Close button
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(self.close)
        close_button.setFont(QFont("Arial", 12))
        title_layout.addWidget(close_button)
        
        # Add title bar to main layout
        main_layout.addWidget(title_bar)
        
        # Content layout
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 0.9);
                border-radius: 15px;
                min-width: 200px;
            }
            QLabel {
                color: white;
                padding: 5px;
                font-family: 'Segoe UI', sans-serif;
                background-color: transparent;
            }
        """)
        
        # Labels
        self.time_label = self.create_label("시간")
        self.temp_label = self.create_label("온도")
        self.weather_label = self.create_label("날씨")
        self.humidity_label = self.create_label("습도")
        
        # Add labels to content layout
        for label in [self.time_label, self.temp_label, 
                     self.weather_label, self.humidity_label]:
            content_layout.addWidget(label)
        
        # Add content widget to main layout
        main_layout.addWidget(content_widget)
        main_layout.setContentsMargins(0, 0, 0, 10)
        
        self.resize(200, 160)
        
    def create_label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(10)
        label.setFont(font)
        return label
        
    def setup_timer(self):
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_weather)
        self.update_timer.start(self.config_manager.config["update_interval"])
        self.update_weather()
        
    def update_weather(self):
        weather_data = self.weather_api.get_weather()
        if weather_data:
            try:
                temp = weather_data['main']['temp']
                weather = weather_data['weather'][0]['description']
                humidity = weather_data['main']['humidity']
                current_time = datetime.now().strftime("%H:%M")
                
                self.time_label.setText(f"현재 시각: {current_time}")
                self.temp_label.setText(f"온도: {temp:.1f}°C")
                self.weather_label.setText(f"날씨: {weather}")
                self.humidity_label.setText(f"습도: {humidity}%")
            except Exception as e:
                print(f"날씨 데이터 처리 실패: {e}")
                self.show_error()
        else:
            self.show_error()
            
    def show_error(self):
        self.temp_label.setText("날씨 정보 로딩 실패")
        self.weather_label.setText("인터넷 연결을 확인해주세요")
        
    def restore_position(self):
        pos = self.config_manager.config["last_position"]
        self.move(pos["x"], pos["y"])
        
    def save_position(self):
        pos = self.pos()
        self.config_manager.config["last_position"] = {
            "x": pos.x(),
            "y": pos.y()
        }
        self.config_manager.save_config()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.save_position()
            
    def closeEvent(self, event):
        self.save_position()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    widget = WeatherWidget()
    widget.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()