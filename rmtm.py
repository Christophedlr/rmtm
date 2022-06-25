import paramiko
from scp import SCPClient

class Rmtm:
    ssh_connection: paramiko.SSHClient = paramiko.SSHClient()

    def open(self, host: str, user: str, password: str):
        self.ssh_connection.load_system_host_keys()
        self.ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_connection.connect(hostname=host, username=user, password=password)

    def close(self):
        self.ssh_connection.close()

    def reboot_command(self):
        self.ssh_connection.exec_command('/sbin/reboot')

    def halt_command(self):
        self.ssh_connection.exec_command('/sbin/poweroff')
