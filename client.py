import paramiko

class XboxSFTPClient:
    def __init__(self, host, port=22, username='app', password=''):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.sftp = None
        self.ssh = None

    def connect(self):
        self.transport = paramiko.Transport((self.host, self.port))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.username, password=self.password)

    def list_dir(self, path="."):
        return self.sftp.listdir_attr(path)

    def download_file(self, remote_path, local_path):
        self.sftp.get(remote_path, local_path)

    def upload_file(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    def execute_command(self, command):
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        return '', 'SSH client not connected'

    def read_memory(self, address, size):
        if self.ssh:
            command = f"readmem {address} {size}"
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        return '', 'SSH client not connected'

    def get_game_info(self):
        command = "cat /proc/gameinfo"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        if self.ssh:
            self.ssh.close()
