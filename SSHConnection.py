import paramiko
import logging

from paramiko.client import SSHClient
from paramiko.sftp_client import SFTPClient

logger = logging.getLogger()


class SSHConnection:
    def __init__(self, hostname, username, password):
        self.__hostname = hostname
        self.__username = username
        self.__password = password
        self.__ssh = None
        self.__sftp = None
        self.configure()

    def connect(self):
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.__ssh.connect(hostname=self.__hostname, username=self.__username, password=self.__password)
            logger.debug('SSH-подключение установлено.')
        except paramiko.AuthenticationException:
            logger.error('Не удалось аутентифицироваться, проверьте свои учетные данные.')
        except paramiko.SSHException as e:
            logger.error(f'Произошла ошибка: {e}')

    def open_sftp(self):
        if self.__ssh is not None:
            try:
                self.__sftp = self.__ssh.open_sftp()
                logger.debug('SFTP-соединение установлено.')
            except Exception as e:
                logger.warning(f'Ошибка при открытии SFTP: {e}')
        else:
            logger.error('SSH-соединение не установлено, SFTP открыть невозможно.')

    def configure(self):
        self.connect()
        self.open_sftp()

    @property
    def ssh(self) -> SSHClient:
        if self.__ssh is None:
            logger.error('SSH-соединение не установлено.')
            return None
        return self.__ssh

    @property
    def sftp(self) -> SFTPClient:
        if self.__sftp is None:
            logger.error('SFTP-соединение не установлено.')
            return None
        return self.__sftp
