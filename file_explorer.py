import os
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QSplitter, QTreeWidget, QTreeWidgetItem, QTextEdit, QComboBox,
    QFileDialog, QInputDialog, QListWidget, QSizePolicy, QListWidgetItem, QStyle,
    QMenu, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

from client import XboxSFTPClient
from theme import DARK_QSS
from hydra_panel import HydraPanel
from security_tools_panel import SecurityToolsPanel

TARGET_RUN_PATH = r"U:\\Users\\UserMgr0\\AppData\\Local\\Packages\\27878ConstantineTarasenko.458004FD2C47C_c8b3w9r5va522\\LocalState\\run.exe"

class FileExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xbox SFTP Tool")
        self.setGeometry(300, 200, 1100, 650)
        self.setStyleSheet(DARK_QSS)

        self.client = None
        self.current_path = "U:\\"
        self.path_history = []

        style = self.style() or QApplication.style()
        self.drive_icon = style.standardIcon(QStyle.SP_DriveHDIcon)
        self.folder_icon = style.standardIcon(QStyle.SP_DirIcon)
        self.file_icon = style.standardIcon(QStyle.SP_FileIcon)
        self.upload_icon = style.standardIcon(QStyle.SP_ArrowUp)
        self.download_icon = style.standardIcon(QStyle.SP_ArrowDown)

        self.host_input = QLineEdit("192.168.0.8")
        self.host_input.setMinimumWidth(150)
        self.host_input.setMaximumWidth(200)
        self.username_input = QLineEdit("xbox")
        self.username_input.setMinimumWidth(80)
        self.username_input.setMaximumWidth(120)
        self.password_input = QLineEdit()
        self.password_input.setMinimumWidth(110)
        self.password_input.setMaximumWidth(140)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setIcon(style.standardIcon(QStyle.SP_DialogOkButton))
        self.connect_btn.clicked.connect(self.connect_to_xbox)

        self.refresh_drives_btn = QPushButton("Refresh Drives")
        self.refresh_drives_btn.clicked.connect(self.scan_drives)

        self.payload_dropdown = QComboBox()
        self.refresh_payloads()
        self.auto_payload_btn = QPushButton("Auto Inject & Execute")
        self.auto_payload_btn.setIcon(style.standardIcon(QStyle.SP_MediaPlay))
        self.auto_payload_btn.clicked.connect(self.auto_inject_execute)
        self.payload_btn = QPushButton("Inject and Execute Payload")
        self.payload_btn.setIcon(style.standardIcon(QStyle.SP_CommandLink))
        self.payload_btn.clicked.connect(self.inject_and_execute_payload)

        control_panel = QHBoxLayout()
        control_panel.addWidget(QLabel("IP:"))
        control_panel.addWidget(self.host_input)
        control_panel.addWidget(QLabel("User:"))
        control_panel.addWidget(self.username_input)
        control_panel.addWidget(QLabel("Pass:"))
        control_panel.addWidget(self.password_input)
        control_panel.addWidget(self.connect_btn)
        control_panel.addSpacing(16)
        control_panel.addWidget(self.refresh_drives_btn)
        control_panel.addWidget(QLabel("Payload:"))
        control_panel.addWidget(self.payload_dropdown)
        control_panel.addWidget(self.auto_payload_btn)
        control_panel.addWidget(self.payload_btn)

        self.sidebar = QListWidget()
        self.sidebar.setMinimumWidth(170)
        self.sidebar.setMaximumWidth(210)
        self.sidebar.itemClicked.connect(self.change_drive)

        self.file_tree = QTreeWidget()
        self.file_tree.setColumnCount(4)
        self.file_tree.setHeaderLabels(["Name", "Size", "Type", "Modified"])
        self.file_tree.itemDoubleClicked.connect(self.tree_item_double_clicked)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.open_tree_context_menu)

        self.upload_btn = QPushButton("Upload")
        self.upload_btn.setIcon(self.upload_icon)
        self.upload_btn.clicked.connect(self.upload_file)
        self.memory_btn = QPushButton("Dump Game Memory")
        self.memory_btn.setIcon(style.standardIcon(QStyle.SP_ComputerIcon))
        self.memory_btn.clicked.connect(self.dump_memory)
        self.scan_game_btn = QPushButton("Scan Game Info")
        self.scan_game_btn.setIcon(style.standardIcon(QStyle.SP_MessageBoxInformation))
        self.scan_game_btn.clicked.connect(self.scan_game_info)
        self.list_apps_btn = QPushButton("List Installed Apps")
        self.list_apps_btn.setIcon(style.standardIcon(QStyle.SP_DirHomeIcon))
        self.list_apps_btn.clicked.connect(self.list_installed_apps)
        self.toast_test_btn = QPushButton("Test Toast")
        self.toast_test_btn.clicked.connect(self.test_xbox_toast)

        extra_btns = QHBoxLayout()
        extra_btns.addWidget(self.upload_btn)
        extra_btns.addWidget(self.memory_btn)
        extra_btns.addWidget(self.scan_game_btn)
        extra_btns.addWidget(self.list_apps_btn)
        extra_btns.addWidget(self.toast_test_btn)

        self.hydra_btn = QPushButton("Hydra")
        self.hydra_btn.clicked.connect(self.open_hydra_panel)
        extra_btns.addWidget(self.hydra_btn)

        self.security_tools_btn = QPushButton("Security Tools")
        self.security_tools_btn.clicked.connect(self.open_security_tools_panel)
        extra_btns.addWidget(self.security_tools_btn)

        extra_btns.addStretch()

        self.back_btn = QPushButton("Back")
        self.back_btn.setIcon(style.standardIcon(QStyle.SP_ArrowBack))
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(140)

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.back_btn)
        right_panel.addWidget(QLabel("Current Path:"))
        self.path_label = QLabel(self.current_path)
        right_panel.addWidget(self.path_label)
        right_panel.addWidget(self.file_tree)
        right_panel.addLayout(extra_btns)
        right_panel.addWidget(QLabel("Log Output:"))
        right_panel.addWidget(self.log)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        splitter = QSplitter(Qt.Horizontal)
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QLabel("Drives"))
        sidebar_layout.addWidget(self.sidebar)
        sidebar_layout.addStretch()
        sidebar_widget.setLayout(sidebar_layout)
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 18, 24, 18)
        main_layout.setSpacing(18)
        main_layout.addLayout(control_panel)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def open_security_tools_panel(self):
        panel = SecurityToolsPanel(self, default_ip=self.host_input.text().strip())
        panel.exec_()

    def go_back(self):
        if self.path_history:
            prev_path = self.path_history.pop()
            self.current_path = prev_path
            self.path_label.setText(self.current_path)
            self.refresh_file_tree()
            if not self.path_history:
                self.back_btn.setEnabled(False)

    def append_log(self, message):
        self.log.moveCursor(QTextCursor.End)
        self.log.insertPlainText(message + '\n')
        self.log.moveCursor(QTextCursor.End)

    def open_hydra_panel(self):
        panel = HydraPanel(self, default_ip=self.host_input.text().strip())
        panel.exec_()

    def test_xbox_toast(self):
        message, ok = QInputDialog.getText(self, "Test Toast", "Toast message:", text="Hello from SFTP Tool!")
        if ok and message:
            self.send_xbox_toast(message)

    def send_xbox_toast(self, message):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        try:
            self.append_log(f"[TOAST] {message}")
        except Exception as e:
            self.append_log(f"[ERROR] Could not send toast: {e}")

    def refresh_payloads(self):
        self.payload_dropdown.clear()
        if os.path.exists("payloads"):
            for fname in os.listdir("payloads"):
                if fname.lower().endswith(('.exe', '.bin', '.sh')):
                    self.payload_dropdown.addItem(fname)

    def connect_to_xbox(self):
        try:
            self.client = XboxSFTPClient(
                host=self.host_input.text().strip(),
                username=self.username_input.text().strip(),
                password=self.password_input.text().strip()
            )
            self.client.connect()
            self.append_log("[INFO] Connected successfully.")
            self.scan_drives()
        except Exception as e:
            self.append_log(f"[ERROR] Connection failed: {e}")

    def scan_drives(self):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        self.sidebar.clear()
        try:
            drives = []
            entries = self.client.list_dir("/")
            for entry in entries:
                name = entry.filename
                if (name.endswith(':') or name.endswith(':\\')) and (entry.st_mode & 0o040000):
                    drives.append(name if name.endswith('\\') else name + '\\')
                elif len(name) == 1 and (entry.st_mode & 0o040000):
                    drives.append(f"{name}:\\")
            if not drives:
                self.append_log("[WARN] Could not auto-detect drives, using fallback drive list.")
                drives = ["U:\\", "D:\\", "X:\\", "Y:\\", "Z:\\"]
            for drive in drives:
                item = QListWidgetItem(self.drive_icon, drive)
                self.sidebar.addItem(item)
            if drives:
                self.current_path = drives[0]
                self.path_label.setText(self.current_path)
                self.refresh_file_tree()
        except Exception as e:
            self.append_log(f"[ERROR] Drive scan failed: {e}")

    def change_drive(self, item):
        if self.current_path != item.text():
            self.path_history.append(self.current_path)
            self.back_btn.setEnabled(True)
        self.current_path = item.text()
        self.path_label.setText(self.current_path)
        self.refresh_file_tree()

    def refresh_file_tree(self):
        if not self.client:
            return
        try:
            self.file_tree.clear()
            entries = self.client.list_dir(self.current_path)
            for entry in entries:
                is_folder = entry.st_mode & 0o040000
                size = entry.st_size if not is_folder else ""
                ftype = "Folder" if is_folder else "File"
                modified = datetime.fromtimestamp(entry.st_mtime).strftime("%Y-%m-%d %H:%M")
                item = QTreeWidgetItem([
                    entry.filename, str(size), ftype, modified
                ])
                if is_folder:
                    item.setIcon(0, self.folder_icon)
                else:
                    item.setIcon(0, self.file_icon)
                if is_folder:
                    item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                self.file_tree.addTopLevelItem(item)
            self.path_label.setText(self.current_path)
        except Exception as e:
            self.append_log(f"[ERROR] Failed to list directory: {e}")

    def tree_item_double_clicked(self, item, col):
        name = item.text(0)
        ftype = item.text(2)
        new_path = str(Path(self.current_path) / name)
        if ftype == "Folder":
            self.path_history.append(self.current_path)
            self.back_btn.setEnabled(True)
            self.current_path = new_path
            self.path_label.setText(self.current_path)
            self.refresh_file_tree()
        else:
            self.download_file(new_path)

    def download_file(self, remote_path):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File As", os.path.basename(remote_path))
        if save_path:
            try:
                self.client.download_file(remote_path, save_path)
                self.append_log(f"[INFO] Downloaded {remote_path} to {save_path}")
            except Exception as e:
                self.append_log(f"[ERROR] Download failed: {e}")

    def upload_file(self):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if file_path:
            try:
                remote_path = str(Path(self.current_path) / Path(file_path).name)
                self.client.upload_file(file_path, remote_path)
                self.append_log(f"[INFO] Uploaded {remote_path}")
                self.refresh_file_tree()
            except Exception as e:
                self.append_log(f"[ERROR] Upload failed: {e}")

    def auto_inject_execute(self):
        fname = self.payload_dropdown.currentText()
        if not fname:
            self.append_log("[ERROR] No payload selected.")
            return
        full_path = str(Path("payloads") / fname)
        if not os.path.exists(full_path):
            self.append_log("[ERROR] Payload file not found.")
            return
        try:
            remote_path = str(Path(self.current_path) / Path(full_path).name)
            self.client.upload_file(full_path, remote_path)
            self.append_log(f"[INFO] Uploaded {remote_path}, executing...")
            stdout, stderr = self.client.execute_command(remote_path)
            if stdout:
                self.append_log(f"[OUTPUT] {stdout}")
            if stderr:
                self.append_log(f"[ERROR] {stderr}")
        except Exception as e:
            self.append_log(f"[ERROR] Auto inject/exec failed: {e}")

    def inject_and_execute_payload(self):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Payload to Upload and Execute")
        if file_path:
            try:
                remote_path = str(Path(self.current_path) / Path(file_path).name)
                self.client.upload_file(file_path, remote_path)
                self.append_log(f"[INFO] Uploaded {remote_path}, executing...")
                stdout, stderr = self.client.execute_command(remote_path)
                if stdout:
                    self.append_log(f"[OUTPUT] {stdout}")
                if stderr:
                    self.append_log(f"[ERROR] {stderr}")
            except Exception as e:
                self.append_log(f"[ERROR] Upload or Execution failed: {e}")

    def dump_memory(self):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        try:
            addr, ok1 = QInputDialog.getText(self, "Memory Address", "Enter memory address (hex):", text="0x100000")
            size, ok2 = QInputDialog.getInt(self, "Size", "Enter number of bytes to read:", value=64)
            if ok1 and ok2:
                stdout, stderr = self.client.read_memory(addr, size)
                if stdout:
                    self.append_log(f"[MEMORY DUMP] {stdout}")
                if stderr:
                    self.append_log(f"[ERROR] {stderr}")
        except Exception as e:
            self.append_log(f"[ERROR] Memory dump failed: {e}")

    def scan_game_info(self):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        try:
            out, err = self.client.get_game_info()
            if out:
                self.append_log(f"[GAME INFO] {out}")
            if err:
                self.append_log(f"[ERROR] {err}")
        except Exception as e:
            self.append_log(f"[ERROR] Game scan failed: {e}")

    def list_installed_apps(self):
        if not self.client:
            self.append_log("[ERROR] Not connected.")
            return
        try:
            apps_dir = "U:\\Program Files\\WindowsApps"
            entries = self.client.list_dir(apps_dir)
            app_names = [entry.filename for entry in entries if entry.st_mode & 0o040000]
            if not app_names:
                self.append_log("[INFO] No installed apps found in WindowsApps.")
                QMessageBox.information(self, "Installed Apps", "No installed apps found.")
                return
            app_list_str = "\n".join(app_names)
            QMessageBox.information(self, "Installed Apps/Games", app_list_str)
            self.append_log(f"[INFO] Listed {len(app_names)} installed apps/games.")
        except Exception as e:
            self.append_log(f"[ERROR] Could not list installed apps: {e}")
            QMessageBox.warning(self, "Error", f"Could not list apps: {e}")

    def open_tree_context_menu(self, pos):
        item = self.file_tree.itemAt(pos)
        menu = QMenu()
        actions = {}
        if item:
            actions['copy'] = menu.addAction("Copy")
            actions['rename'] = menu.addAction("Rename")
            actions['delete'] = menu.addAction("Delete")
            if item.text(2) == "File":
                actions['send_run'] = menu.addAction("Send & Execute as run.exe")
        actions['new_folder'] = menu.addAction("New Folder")
        action = menu.exec_(self.file_tree.viewport().mapToGlobal(pos))

        if item and action == actions.get('copy'):
            name = item.text(0)
            src_path = str(Path(self.current_path) / name)
            dest_path, ok = QInputDialog.getText(self, "Copy", f"Copy '{name}' to (destination path):", text=str(Path(self.current_path) / (name + '_copy')))
            if ok and dest_path:
                try:
                    if item.text(2) == "Folder":
                        self.copy_folder(src_path, dest_path)
                    else:
                        self.client.sftp.get(src_path, "__tmp_copy_file__")
                        self.client.sftp.put("__tmp_copy_file__", dest_path)
                        os.remove("__tmp_copy_file__")
                    self.append_log(f"[INFO] Copied {src_path} to {dest_path}")
                    self.refresh_file_tree()
                except Exception as e:
                    self.append_log(f"[ERROR] Copy failed: {e}")

        if item and action == actions.get('rename'):
            name = item.text(0)
            old_path = str(Path(self.current_path) / name)
            new_name, ok = QInputDialog.getText(self, "Rename", f"Rename '{name}' to:")
            if ok and new_name:
                new_path = str(Path(self.current_path) / new_name)
                try:
                    self.client.sftp.rename(old_path, new_path)
                    self.append_log(f"[INFO] Renamed {old_path} to {new_path}")
                    self.refresh_file_tree()
                except Exception as e:
                    self.append_log(f"[ERROR] Rename failed: {e}")

        if item and action == actions.get('delete'):
            name = item.text(0)
            path = str(Path(self.current_path) / name)
            reply = QMessageBox.question(self, "Delete", f"Delete '{name}'?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    if item.text(2) == "Folder":
                        self.client.sftp.rmdir(path)
                    else:
                        self.client.sftp.remove(path)
                    self.append_log(f"[INFO] Deleted {path}")
                    self.refresh_file_tree()
                except Exception as e:
                    self.append_log(f"[ERROR] Delete failed: {e}")

        if action == actions.get('new_folder'):
            folder_name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
            if ok and folder_name:
                path = str(Path(self.current_path) / folder_name)
                try:
                    self.client.sftp.mkdir(path)
                    self.append_log(f"[INFO] Created folder {path}")
                    self.refresh_file_tree()
                except Exception as e:
                    self.append_log(f"[ERROR] Create folder failed: {e}")

        if item and action == actions.get('send_run'):
            name = item.text(0)
            src_path = str(Path(self.current_path) / name)
            try:
                self.append_log(f"[INFO] Sending {src_path} as run.exe ...")
                self.client.sftp.get(src_path, "__tmp_run_file__")
                self.client.sftp.put("__tmp_run_file__", TARGET_RUN_PATH)
                os.remove("__tmp_run_file__")
                self.append_log(f"[INFO] Executing run.exe ...")
                exec_cmd = f'"{TARGET_RUN_PATH}"'
                stdout, stderr = self.client.execute_command(exec_cmd)
                if stdout:
                    self.append_log(f"[OUTPUT] {stdout}")
                if stderr:
                    self.append_log(f"[ERROR] {stderr}")
            except Exception as e:
                self.append_log(f"[ERROR] Send & Execute failed: {e}")

    def copy_folder(self, src, dst):
        try:
            self.client.sftp.mkdir(dst)
        except Exception:
            pass
        for entry in self.client.sftp.listdir_attr(src):
            src_item = str(Path(src) / entry.filename)
            dst_item = str(Path(dst) / entry.filename)
            if entry.st_mode & 0o040000:
                self.copy_folder(src_item, dst_item)
            else:
                self.client.sftp.get(src_item, "__tmp_copy_file__")
                self.client.sftp.put("__tmp_copy_file__", dst_item)
                os.remove("__tmp_copy_file__")
