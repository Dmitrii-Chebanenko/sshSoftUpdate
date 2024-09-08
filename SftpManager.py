import os
import pandas as pd
import logging
from io import StringIO
from paramiko import SFTPClient

logger = logging.getLogger()


class SftpManager:
    def __init__(self, sftp: SFTPClient):
        self.__sftp = sftp

    def send_sftp_file(self, filepath: str, remote: str):
        """

        :param filepath: путь до файла
        :param remote: путь для отправки
        :return:
        """
        try:
            self.__sftp.put(filepath, remote)
            logger.info(f'Файл {filepath} успешно отправлен в {remote}')
        except FileNotFoundError as e:
            logger.error(f'Файл не найден {e}')
        except Exception as e:
            logger.error(f'Ошибка отправки файла {e}')

    def read_bit_file(self, path: str) -> bytes:
        """
        считываем файл в поток байтов
        :param path: путь файла
        :return: содержание файла в байтах
        """
        try:
            with self.__sftp.open(path, 'r') as file:
                file_content = file.read()
                return file_content
        except Exception as e:
            logger.warning(f'Ошибка чтения файла {path} {e}')
            return None

    def read_csv_sftp(self, path: str) -> pd.DataFrame:
        """
        считываем csv из sftp и заполяем float(nan) на str(NaN)
        :param path
        :return: таблицу
        """
        try:
            dec = self.read_bit_file(path).decode('utf-8')
            data = pd.read_csv(StringIO(dec), sep=';', dtype=str)
            data = data.fillna('NaN')
            return data
        except Exception as e:
            logger.error(f'Ошибка при декодировании {e}')

    def send_df_sftp(self, data: pd.DataFrame, filepath: str, remotepath: str):
        """

        :param filepath: путь до файла
        :param remotepath: путь отправки
        :param data: таблица для отправки
        :return:
        """
        SftpManager.save_data(data, filepath)
        self.send_sftp_file(filepath, remotepath)
        os.remove(filepath)

    @staticmethod
    def save_data(data: pd.DataFrame, name):
        """
        сохранить файла на
        :param data: таблица
        :param name: имя
        :return:
        """
        data.to_csv(name, sep=';', index=False)

    def get_sftp(self) -> SFTPClient:
        """
        гетер для sftp
        :return: sftp
        """
        return self.__sftp
