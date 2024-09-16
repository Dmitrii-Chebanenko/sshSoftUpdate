import hashlib
import logging
import pandas as pd
import sys

from SSHConnection import SshCommandExecutor

logger = logging.getLogger()


class FileChecksumHandler:

    def __init__(self, data: pd.DataFrame, executor: SshCommandExecutor):
        self.__data: pd.DataFrame = data
        self.__md5_table: pd.DataFrame = None
        self.__executor = executor
        self.create_md5_table()

    def create_md5_table(self):
        """
        Создает md5 таблицу, на основании поля __data
        :return:
        """

        if self.__data is not None:
            res = self.__data.copy()
            arr = []
            for i in range(res.shape[0]):
                arr.append(
                    FileChecksumHandler.get_md5(
                        self.__executor.read_file(self.__data.loc[i, 'filename']).encode('utf-8')))
            res['crc'] = arr
            self.__md5_table = res
        else:
            logger.error('Ошибка при создании md5')

    def save_md5(self, name: str):
        """
        Сохраняет таблицу

        :param name: имя файла
        :return:
        """
        try:
            logger.info(f'MD5 сохранен {name}')
            self.__md5_table.to_csv(name, sep=';', index=False)
        except Exception as e:
            logger.error(f'Ошибка сохранения md5 {e}')

    @property
    def md5_table(self) -> pd.DataFrame:
        """
        геттер для md5_table
        :return: md5_table
        """
        return self.__md5_table

    @property
    def data(self) -> pd.DataFrame:
        """
        геттер для data
        :return: data
        """
        return self.__data

    @staticmethod
    def print_df(data: pd.DataFrame, sep: str):
        """
        Метод для принта таблицы в консоль
        :param sep: разделитель м/у ячейками
        :param data: таблица
        :return:
        """
        if data is not None:
            if data.shape[0] == 0:
                print('Датафрейм пустой')
            else:
                data.to_csv(sys.stdout, sep=sep, index=False)
        else:
            logger.info('Объект None')

    @staticmethod
    def get_md5(arg: bytes) -> str:
        """
        Медод для подсчета md5
        :param arg: массив байтов для подсчета md5
        :return: стоку md5
        """
        try:
            md5 = hashlib.md5()
            md5.update(arg)
            return '0x' + md5.hexdigest()
        except Exception as e:
            logger.warning(f'Ошибка вычисления md5 {e}')
            return 'NaN'
