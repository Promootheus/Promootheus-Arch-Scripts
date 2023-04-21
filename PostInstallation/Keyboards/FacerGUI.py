#QT Python code for a GUI interface to Facer

import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QSlider, QPushButton, QColorDialog

class FacerRGBGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.mode_label = QLabel('Select mode:')
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Static', 'Breath', 'Neon', 'Wave', 'Shifting', 'Zoom'])
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_combo)

        self.zone_label = QLabel('Select zone (Static mode only):')
        self.zone_combo = QComboBox()
        self.zone_combo.addItems(['1', '2', '3', '4'])
        layout.addWidget(self.zone_label)
        layout.addWidget(self.zone_combo)

        self.speed_label = QLabel('Animation speed:')
        self.speed_slider = QSlider()
        self.speed_slider.setRange(0, 9)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.speed_slider)

        self.brightness_label = QLabel('Backlight brightness:')
        self.brightness_slider = QSlider()
        self.brightness_slider.setRange(0, 100)
        layout.addWidget(self.brightness_label)
        layout.addWidget(self.brightness_slider)

        self.direction_label = QLabel('Animation direction:')
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(['Right to Left', 'Left to Right'])
        layout.addWidget(self.direction_label)
        layout.addWidget(self.direction_combo)

        self.color_button = QPushButton('Choose color')
        self.color_button.clicked.connect(self.color_dialog)
        layout.addWidget(self.color_button)

        self.apply_button = QPushButton('Apply')
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def color_dialog(self):
        self.color = QColorDialog.getColor()
        if self.color.isValid():
            self.color_rgb = self.color.red(), self.color.green(), self.color.blue()

    def apply_settings(self):
        # Use the current user's home directory
        user_home = os.environ['HOME']
        facer_rgb_script = os.path.join(user_home, 'acer-predator-turbo-and-rgb-keyboard-linux-module', 'facer_rgb.py')
        command = f'python {facer_rgb_script} -m {self.mode_combo.currentIndex()} -z {self.zone_combo.currentText()} -s {self.speed_slider.value()} -b {self.brightness_slider.value()} -d {self.direction_combo.currentIndex() + 1} -cR {self.color_rgb[0]} -cG {self.color_rgb[1]} -cB {self.color_rgb[2]}'
        subprocess.run(command, shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FacerRGBGUI()
    ex.show()
    sys.exit(app.exec_())

