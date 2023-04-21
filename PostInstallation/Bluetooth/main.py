import os
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from subprocess import Popen, PIPE

class TrayApp:
    def __init__(self):
        app = QApplication(sys.argv)

        self.tray_icon = QSystemTrayIcon()
        icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "on.png")
        tooltip = "Disable Bluetooth"
        if not self.is_bluetooth_active():
            icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "off.png")
            tooltip = "Enable Bluetooth"
        icon = QIcon(icon_file)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip(tooltip)
        self.tray_icon.activated.connect(self.toggle_bluetooth)

        menu = QMenu()
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(app.quit)
        menu.addAction(quit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

        sys.exit(app.exec_())

    def is_bluetooth_active(self):
        # Check if Bluetooth is currently enabled or disabled
        p = Popen(["systemctl", "is-active", "bluetooth"], stdout=PIPE)
        output, _ = p.communicate()
        return output.decode().strip() == "active"

    def toggle_bluetooth(self, reason):
        # Toggle Bluetooth
        if reason == QSystemTrayIcon.Trigger:
            is_active = self.is_bluetooth_active()
            sudo_password, ok = QInputDialog.getText(None, "Enter sudo password", "Password:", QLineEdit.Password)
            if ok:
                if is_active:
                    Popen(["sudo", "-S", "systemctl", "stop", "bluetooth"], stdin=PIPE).communicate(sudo_password.encode())
                else:
                    Popen(["sudo", "-S", "systemctl", "start", "bluetooth"], stdin=PIPE).communicate(sudo_password.encode())
            icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "on.png")
            tooltip = "Disable Bluetooth"
            if not self.is_bluetooth_active():
                icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "off.png")
                tooltip = "Enable Bluetooth"
            self.tray_icon.setIcon(QIcon(icon_file))
            self.tray_icon.setToolTip(tooltip)

TrayApp()
