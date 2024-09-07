import argparse
import logging
import pandas as pd

from LogerConfig import setup_logging
from SSHConnection import SSHConnection
from SftpManager import SftpManager
from FileChecksumHandler import FileChecksumHandler

setup_logging()
logger = logging.getLogger()


def configure_args_comp():
    args_parser = argparse.ArgumentParser(description='Подключение к VM.')

    args_parser.add_argument('--filepath', required=True, help='Путь до файла')
    args_parser.add_argument('--etalon', required=True, help='Путь до файла для сравнения')
    args_parser.add_argument('--username', required=True, help='Имя для подключения')
    args_parser.add_argument('--passwd', required=True, help='Пароль')

    args = args_parser.parse_args()
    return args


def compare_with_etalon(table: pd.DataFrame, etalon: pd.DataFrame) -> pd.DataFrame:
    """

    :param table: первая таблица (должна содержать столбец crc)
    :param etalon: эталон для сравнения
    :return: таблицу, состоящую из строк, где crc != ecrc
    """
    try:
        if not isinstance(table, pd.DataFrame) or not isinstance(etalon, pd.DataFrame):
            logging.error('Один из входных параметров не является DataFrame')
            return None

        if 'crc' not in table.columns or 'crc' not in etalon.columns:
            logging.error('Один из DataFrame не содержит столбца \'crc\'')
            return None
        res = table.copy()
        res['ecrc'] = etalon['crc']
        res = res[res['crc'].str.lower() != res['ecrc'].str.lower()]
        if res.shape[0] == 0:
            print('md5 hash равны')
        return res
    except Exception as e:
        logger.error('Ошибка сравнения: ', e)

def main():
    args = configure_args_comp()
    ssh_connection = SSHConnection(hostname='127.0.0.1', username=args.username, password=args.passwd)
    sftp = ssh_connection.sftp
    sftp_manager = SftpManager(sftp)
    data = sftp_manager.read_csv_sftp(args.filepath)
    table_handler = FileChecksumHandler(data, sftp)

    etalon = sftp_manager.read_csv_sftp(args.etalon)
    etalon_handler = FileChecksumHandler(etalon, sftp)

    res = compare_with_etalon(table_handler.md5_table, etalon_handler.data)
    FileChecksumHandler.print_df(res, ';')

if __name__ == '__main__':
    main()
