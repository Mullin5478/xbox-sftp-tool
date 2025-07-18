import os
import json
import base64

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QFormLayout
)

from hydra_client import LittleHydraClient as HydraClient



class SecurityToolsPanel(QDialog):
    def __init__(self, parent=None, default_ip=""):
        super().__init__(parent)
        self.setWindowTitle("Security Tools Panel")
        self.setMinimumSize(600, 600)

        self.default_ip = default_ip.strip() or "127.0.0.1"

        layout = QVBoxLayout()

        # --- Token Info Section ---
        token_label = QLabel("<b>Token Info</b>")
        layout.addWidget(token_label)

        self.token_info = QTextEdit()
        self.token_info.setReadOnly(True)
        layout.addWidget(self.token_info)

        refresh_token_btn = QPushButton("Refresh Token Info")
        refresh_token_btn.clicked.connect(self.refresh_token_info)
        layout.addWidget(refresh_token_btn)

        # --- Privilege Toggle Section ---
        priv_label = QLabel("<b>Toggle Privileges</b>")
        layout.addWidget(priv_label)

        form = QFormLayout()
        self.priv_name = QLineEdit()
        self.priv_enable = QLineEdit()
        form.addRow("Privilege Name (e.g. SeDebugPrivilege):", self.priv_name)
        form.addRow("Enable (true/false):", self.priv_enable)
        layout.addLayout(form)

        priv_btn = QPushButton("Set Privilege")
        priv_btn.clicked.connect(self.set_privilege)
        layout.addWidget(priv_btn)

        # --- Launch Process Section ---
        launch_label = QLabel("<b>Launch Process with Token</b>")
        layout.addWidget(launch_label)

        self.proc_path = QLineEdit()
        self.proc_args = QLineEdit()

        launch_form = QFormLayout()
        launch_form.addRow("Executable Path:", self.proc_path)
        launch_form.addRow("Arguments (space-separated):", self.proc_args)
        layout.addLayout(launch_form)

        launch_btn = QPushButton("Launch Process")
        launch_btn.clicked.connect(self.launch_process)
        layout.addWidget(launch_btn)

        # --- Xbox API Section ---
        api_label = QLabel("<b>Call Xbox API</b>")
        layout.addWidget(api_label)

        self.api_name = QLineEdit()
        self.api_params = QLineEdit()

        api_form = QFormLayout()
        api_form.addRow("API Name:", self.api_name)
        api_form.addRow("Parameters (JSON):", self.api_params)
        layout.addLayout(api_form)

        api_btn = QPushButton("Call API")
        api_btn.clicked.connect(self.call_api)
        layout.addWidget(api_btn)

        self.api_output = QTextEdit()
        layout.addWidget(self.api_output)

        self.setLayout(layout)

    def _get_hydra_client(self):
        try:
            hydra = HydraClient(self.default_ip)
            hydra.connect()
            return hydra
        except Exception as e:
            self.token_info.append(f"[ERROR] Hydra connection failed: {e}")
            return None

    def refresh_token_info(self):
        client = self._get_hydra_client()
        if not client:
            return

        try:
            payload = {"cmd": "getToken"}
            result = client.send_command(payload)
            if result["status"] == "success":
                text = json.dumps(result["data"], indent=2)
                self.token_info.setPlainText(text)
            else:
                self.token_info.setPlainText(f"[ERROR] {result.get('message')}")
        except Exception as e:
            self.token_info.setPlainText(f"[ERROR] {e}")

    def set_privilege(self):
        client = self._get_hydra_client()
        if not client:
            return

        priv_name = self.priv_name.text().strip()
        enable = self.priv_enable.text().strip().lower() == "true"

        try:
            payload = {
                "cmd": "setPrivilege",
                "name": priv_name,
                "enable": enable
            }
            result = client.send_command(payload)
            self.token_info.append(json.dumps(result, indent=2))
        except Exception as e:
            self.token_info.append(f"[ERROR] {e}")

    def launch_process(self):
        client = self._get_hydra_client()
        if not client:
            return

        path = self.proc_path.text().strip()
        args = self.proc_args.text().strip().split()

        try:
            payload = {
                "cmd": "oneshotSpawn",
                "name": os.path.basename(path) or "NewProcess",
                "config": {
                    "exec_type": "native",
                    "path": path,
                    "args": args,
                    "ports": [],
                    "working_dir": os.path.dirname(path) or "C:\\"
                }
            }
            result = client.send_command(payload)

            # Check for base64 output
            stdout_b64 = result.get("data", {}).get("stdout")
            output_text = ""
            if stdout_b64:
                decoded = self._decode_base64(stdout_b64)
                output_text += decoded + "\n"

            self.token_info.append(json.dumps(result, indent=2))
            if output_text:
                self.token_info.append(output_text)

        except Exception as e:
            self.token_info.append(f"[ERROR] {e}")

    def call_api(self):
        client = self._get_hydra_client()
        if not client:
            return

        api_name = self.api_name.text().strip()
        params_text = self.api_params.text().strip()

        try:
            params = json.loads(params_text) if params_text else {}
            payload = {"cmd": api_name, **params}
            result = client.send_command(payload)
            pretty = json.dumps(result, indent=2)
            self.api_output.setPlainText(pretty)
        except Exception as e:
            self.api_output.setPlainText(f"[ERROR] {e}")

    def _decode_base64(self, b64text):
        try:
            decoded = base64.b64decode(b64text).decode("utf-8", errors="ignore")
            return decoded
        except Exception as e:
            return f"[ERROR decoding base64] {e}"
