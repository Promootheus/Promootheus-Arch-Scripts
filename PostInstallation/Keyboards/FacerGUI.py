#QT Python code for a GUI interface to Facer

import os
import json
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QComboBox, QSlider, QPushButton, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class FacerRGBGUI(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize default settings
        self.mode = 3  # Wave
        self.zone = 1
        self.speed = 5  # Half of maximum
        self.brightness = 100  # Maximum brightness
        self.direction = 1
        self.color = QColor(0, 0, 255)  # Blue color
        self.color_rgb = self.color.red(), self.color.green(), self.color.blue()

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        mode_label = QLabel('Mode:')
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Static', 'Breath', 'Neon', 'Wave', 'Shifting', 'Zoom'])
        self.mode_combo.setCurrentIndex(self.mode)

        zone_label = QLabel('Zone:')
        self.zone_combo = QComboBox()
        self.zone_combo.addItems(['1', '2', '3', '4'])
        self.zone_combo.setCurrentIndex(self.zone - 1)

        speed_label = QLabel('Speed:')
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(0, 9)
        self.speed_slider.setValue(self.speed)
        self.speed_value = QLabel(f"Animation Speed: {self.speed}")
        self.speed_slider.valueChanged.connect(lambda: self.speed_value.setText(f"Animation Speed: {self.speed_slider.value()}"))

        brightness_label = QLabel('Brightness:')
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(self.brightness)
        self.brightness_value = QLabel(f"Backlight Brightness: {self.brightness}")
        self.brightness_slider.valueChanged.connect(lambda: self.brightness_value.setText(f"Backlight Brightness: {self.brightness_slider.value()}"))

        direction_label = QLabel('Direction:')
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(['Right to Left', 'Left to Right'])
        self.direction_combo.setCurrentIndex(self.direction - 1)

        color_label = QLabel('Color:')
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(50, 25)
        self.color_preview.setStyleSheet(f'background-color: {self.color.name()}')
        color_button = QPushButton('Select Color')
        color_button.clicked.connect(self.select_color)

        apply_button = QPushButton('Apply')
        apply_button.clicked.connect(self.apply_settings)

        save_button = QPushButton('Save Profile')
        save_button.clicked.connect(self.save_profile)

        load_button = QPushButton('Load Profile')
        load_button.clicked.connect(self.load_profile)

        layout.addWidget(mode_label, 0, 0)
        layout.addWidget(self.mode_combo, 0, 1)
        layout.addWidget(zone_label, 1, 0)
        layout.addWidget(self.zone_combo, 1, 1)
        layout.addWidget(speed_label, 2, 0)
        layout.addWidget(self.speed_slider, 2, 1)
        layout.addWidget(self.speed_value, 4, 1)
        layout.addWidget(brightness_label, 3, 0)
        layout.addWidget(self.brightness_slider, 3, 1)
        layout.addWidget(self.brightness_value, 5, 1)
        layout.addWidget(direction_label, 6, 0)
        layout.addWidget(direction_label, 6, 0)
        layout.addWidget(self.direction_combo, 6, 1)
        layout.addWidget(color_label, 7, 0)
        layout.addWidget(self.color_preview, 7, 1)
        layout.addWidget(color_button, 7, 2)
        layout.addWidget(apply_button, 8, 0)
        layout.addWidget(save_button, 8, 1)
        layout.addWidget(load_button, 8, 2)

        self.setLayout(layout)

    def select_color(self):
        self.color = QColorDialog.getColor(self.color)
        if self.color.isValid():
            self.color_rgb = self.color.red(), self.color.green(), self.color.blue()
            self.color_preview.setStyleSheet(f'background-color: {self.color.name()}')

    def apply_settings(self):
        facer_rgb_script = os.path.join(os.environ['HOME'], 'acer-predator-turbo-and-rgb-keyboard-linux-module', 'facer_rgb.py')
        command = f'python {facer_rgb_script} -m {self.mode_combo.currentIndex()} -z {self.zone_combo.currentIndex() + 1} -s {self.speed_slider.value()} -b {self.brightness_slider.value()} -d {self.direction_combo.currentIndex() + 1} -cR {self.color_rgb[0]} -cG {self.color_rgb[1]} -cB {self.color_rgb[2]}'
        subprocess.run(command, shell=True)

    def save_profile(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Profile', os.path.join(os.environ['HOME'], '.config', 'predator', 'saved profiles'), 'Profile files (*.json)')
        if save_path:
            profile_data = {
                'mode': self.mode_combo.currentIndex(),
                'zone': self.zone_combo.currentIndex() + 1,
                'speed': self.speed_slider.value(),
                'brightness': self.brightness_slider.value(),
                'direction': self.direction_combo.currentIndex() + 1,
                'color': self.color_rgb
            }

            with open(save_path, 'w') as file:
                json.dump(profile_data, file)

    def load_profile(self):
        load_path, _ = QFileDialog.getOpenFileName(self, 'Load Profile', os.path.join(os.environ['HOME'], '.config', 'predator', 'saved profiles'), 'Profile files (*.json)')
        if load_path:
            profile_name = os.path.splitext(os.path.basename(load_path))[0]
            facer_rgb_script = os.path.join(os.environ['HOME'], 'acer-predator-turbo-and-rgb-keyboard-linux-module', 'facer_rgb.py')
            command = f'python {facer_rgb_script} -load "{profile_name}"'
            subprocess.run(command, shell=True)

            # Read the JSON file and update the UI
            with open(load_path, 'r') as file:
                profile_data = json.load(file)

            self.mode_combo.setCurrentIndex(profile_data['mode'])
            self.zone_combo.setCurrentIndex(profile_data['zone'] - 1)
            self.speed_slider.setValue(profile_data['speed'])
            self.brightness_slider.setValue(profile_data['brightness'])
            self.direction_combo.setCurrentIndex(profile_data['direction'] - 1)

            red, green, blue = profile_data['color']
            self.color = QColor(red, green, blue)
            self.color_rgb = red, green, blue
            self.color_preview.setStyleSheet(f'background-color: {self.color.name()}')

if __name__ == '__main__':
    app = QApplication([])
    window = FacerRGBGUI()
    window.setWindowTitle('Facer RGB')
    window.show()
    app.exec_()
