import socket
import json

class LittleHydraClient:
    def __init__(self, host='127.0.0.1', port=9000):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port))

    def send_command(self, command_dict):
        data = json.dumps(command_dict) + '\n'
        self.sock.sendall(data.encode('utf-8'))
        response = self._read_response()
        return json.loads(response)

    def _read_response(self):
        buf = b""
        while not buf.endswith(b"\n"):
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            buf += chunk
        return buf.decode('utf-8').strip()

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
