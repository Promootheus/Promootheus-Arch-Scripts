import sys
import os
import tempfile
import subprocess
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
from collections import deque
from PyQt5.QtCore import QTimer
from QTermWidget import QTermWidget


class SudoPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Enter sudo password")
        self.layout = QVBoxLayout()

        self.password_label = QLabel("Enter sudo password:", self)
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_password(self):
        return self.password_input.text()


class BashScriptRunner(QWidget):
    def __init__(self, sudo_password):
        super().__init__()

        self.sudo_password = sudo_password
        self.commands = []
        self.command_queue = deque()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        script_folder = Path(os.path.expanduser("~/Documents/shell2gui"))
        script_files = script_folder.glob('*.sh')

        tab_widget = QTabWidget()

        for script_file in script_files:
            script_name = script_file.stem

            script_widget = QWidget()
            script_layout = QVBoxLayout()

            with open(script_file, 'r') as file:
                lines = file.readlines()

            for i in range(len(lines)):
                line = lines[i].strip()
                if line.startswith("#title-"):
                    title = line.replace("#title-", "")
                    button = QPushButton(title)
                    command = lines[i + 1].strip()
                    button.clicked.connect(self.create_button_handler(button, command))
                    script_layout.addWidget(button)
                    self.commands.append(command)

            run_all_button = QPushButton("Run All")
            run_all_button.clicked.connect(self.run_all_commands)
            script_layout.addWidget(run_all_button)

            self.output_term = QTermWidget()
            self.output_term.setColorScheme("Linux")  # Set the color scheme
            script_layout.addWidget(self.output_term)

            script_widget.setLayout(script_layout)
            tab_widget.addTab(script_widget, script_name)

        layout.addWidget(tab_widget)
        self.setLayout(layout)
        self.setWindowTitle("Bash Script Runner")

    def create_button_handler(self, button, command):
        def handle_button_click():
            sudo_command = f'echo "{self.sudo_password}" | sudo -S {command}'
            self.run_bash_command(sudo_command)

        return handle_button_click

    def run_all_commands(self):
        self.run_all_mode = True
        for command in self.commands:
            self.command_queue.append(command)
        self.run_next_command()

    def run_next_command(self):
        if self.command_queue:
            command = self.command_queue.popleft()
            self.run_bash_command(command)

    def run_bash_command(self, command):
        self.output_term.sendText(f'echo "Running: {command}"\n')
        self.output_term.sendText(f'{command}\n')
        self.output_term.sendText('clear\n')

def main():
    app = QApplication(sys.argv)
    sudo_password_dialog = SudoPasswordDialog()
    result = sudo_password_dialog.exec_()

    if result == QDialog.Accepted:
        sudo_password = sudo_password_dialog.get_password()
        window = BashScriptRunner(sudo_password)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == '__main__':
    main()

