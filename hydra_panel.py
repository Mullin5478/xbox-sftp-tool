from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QInputDialog, QMessageBox, QDialog, QGroupBox
)
from PyQt5.QtCore import Qt
from hydra_client import LittleHydraClient
import json

class HydraPanel(QDialog):
    def __init__(self, parent=None, default_ip='127.0.0.1', default_port=9000):
        super().__init__(parent)
        self.setWindowTitle("LittleHydra Control Panel")
        self.setGeometry(400, 250, 580, 500)
        self.hydra = None

        # IP and Port inputs
        ip_label = QLabel("Hydra IP:")
        self.ip_input = QLineEdit(default_ip)
        self.ip_input.setFixedWidth(130)
        port_label = QLabel("Port:")
        self.port_input = QLineEdit(str(default_port))
        self.port_input.setFixedWidth(70)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_hydra)
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_hydra)
        self.disconnect_btn.setEnabled(False)

        # Memory Controls
        self.read_mem_btn = QPushButton("Read Memory (Peek)")
        self.read_mem_btn.clicked.connect(self.read_memory)
        self.write_mem_btn = QPushButton("Write Memory (Poke)")
        self.write_mem_btn.clicked.connect(self.write_memory)

        # Raw JSON command controls
        self.json_input = QLineEdit()
        self.json_input.setPlaceholderText('{"cmd": "peek", "addr": 0x12345678, "size": 16}')
        self.send_json_btn = QPushButton("Send Raw JSON")
        self.send_json_btn.clicked.connect(self.send_raw_json)

        # Log/output area
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(180)

        # Layout setup
        top_row = QHBoxLayout()
        top_row.addWidget(ip_label)
        top_row.addWidget(self.ip_input)
        top_row.addWidget(port_label)
        top_row.addWidget(self.port_input)
        top_row.addWidget(self.connect_btn)
        top_row.addWidget(self.disconnect_btn)

        mem_box = QGroupBox("Memory Operations")
        mem_layout = QHBoxLayout()
        mem_layout.addWidget(self.read_mem_btn)
        mem_layout.addWidget(self.write_mem_btn)
        mem_box.setLayout(mem_layout)

        json_box = QGroupBox("Raw Hydra Command")
        json_layout = QHBoxLayout()
        json_layout.addWidget(self.json_input)
        json_layout.addWidget(self.send_json_btn)
        json_box.setLayout(json_layout)

        layout = QVBoxLayout()
        layout.addLayout(top_row)
        layout.addWidget(mem_box)
        layout.addWidget(json_box)
        layout.addWidget(QLabel("Hydra Log:"))
        layout.addWidget(self.log)
        self.setLayout(layout)

        # State
        self.connected = False

    def connect_hydra(self):
        ip = self.ip_input.text().strip()
        port = int(self.port_input.text().strip())
        try:
            self.hydra = LittleHydraClient(ip, port)
            self.hydra.connect()
            self.append_log(f"[INFO] Connected to LittleHydra at {ip}:{port}")
            self.connected = True
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)

            # === Fetch version/build info right after connect ===
            try:
                info = self.hydra.send_command({"cmd": "Info"})
                if info.get("status") == "Success":
                    ver = info["data"]
                    self.append_log(
                        f"[INFO] LittleHydra Version: {ver.get('app_version','?')} | "
                        f"Build: {ver.get('build_date','?')} | "
                        f"Protocol: {ver.get('protocol_version','?')}"
                    )
                else:
                    self.append_log(f"[WARN] Could not fetch version info: {info}")
            except Exception as e:
                self.append_log(f"[WARN] Could not fetch version info: {e}")

        except Exception as e:
            self.append_log(f"[ERROR] Failed to connect: {e}")
            QMessageBox.critical(self, "Connection Error", str(e))

    def disconnect_hydra(self):
        if self.hydra:
            try:
                self.hydra.close()
                self.append_log("[INFO] Disconnected from LittleHydra")
            except Exception as e:
                self.append_log(f"[ERROR] Disconnection: {e}")
        self.connected = False
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.hydra = None

    def read_memory(self):
        if not self.hydra:
            self.append_log("[ERROR] Not connected.")
            return
        address, ok1 = QInputDialog.getText(self, "Memory Address", "Enter address (hex or decimal):", text="0x100000")
        size, ok2 = QInputDialog.getInt(self, "Size", "Number of bytes to read:", value=32)
        if ok1 and ok2:
            try:
                addr = int(address, 16) if address.lower().startswith("0x") else int(address)
                cmd = {"cmd": "peek", "addr": addr, "size": size}
                result = self.hydra.send_command(cmd)
                if "data" in result:
                    hexdata = result["data"]
                    self.append_log(f"[PEEK] Addr: {hex(addr)} Size: {size}\n{hexdata}")
                elif "error" in result:
                    self.append_log(f"[ERROR] {result['error']}")
                else:
                    self.append_log(f"[WARN] No data returned.")
            except Exception as e:
                self.append_log(f"[ERROR] Peek failed: {e}")

    def write_memory(self):
        if not self.hydra:
            self.append_log("[ERROR] Not connected.")
            return
        address, ok1 = QInputDialog.getText(self, "Memory Address", "Enter address (hex or decimal):", text="0x100000")
        data, ok2 = QInputDialog.getText(self, "Data", "Hex bytes (e.g. DEADBEEF):", text="DEADBEEF")
        if ok1 and ok2:
            try:
                addr = int(address, 16) if address.lower().startswith("0x") else int(address)
                # Convert data string to list of bytes
                data_clean = data.replace(" ", "")
                if data_clean.startswith("0x"):
                    data_clean = data_clean[2:]
                if len(data_clean) % 2 != 0:
                    data_clean = "0" + data_clean  # pad if odd length
                byte_list = [int(data_clean[i:i+2], 16) for i in range(0, len(data_clean), 2)]
                cmd = {"cmd": "poke", "addr": addr, "data": byte_list}
                result = self.hydra.send_command(cmd)
                if result.get("status") == "ok" or result.get("result") == "ok":
                    self.append_log(f"[POKE] Wrote {len(byte_list)} bytes to {hex(addr)}")
                elif "error" in result:
                    self.append_log(f"[ERROR] {result['error']}")
                else:
                    self.append_log(f"[WARN] No response or unknown result.")
            except Exception as e:
                self.append_log(f"[ERROR] Poke failed: {e}")

    def send_raw_json(self):
        if not self.hydra:
            self.append_log("[ERROR] Not connected.")
            return
        json_str = self.json_input.text().strip()
        if not json_str:
            self.append_log("[ERROR] Empty JSON.")
            return
        try:
            cmd = json.loads(json_str)
            result = self.hydra.send_command(cmd)
            self.append_log(f"[RAW CMD] Sent: {json.dumps(cmd)}\n[RESP] {json.dumps(result, indent=2)}")
        except Exception as e:
            self.append_log(f"[ERROR] JSON send failed: {e}")

    def append_log(self, message):
        self.log.append(message)
        self.log.moveCursor(self.log.textCursor().End)

    def closeEvent(self, event):
        self.disconnect_hydra()
        event.accept()
