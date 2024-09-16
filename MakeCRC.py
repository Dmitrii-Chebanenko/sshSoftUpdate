import argparse
import logging

from FileChecksumHandler import FileChecksumHandler
from SSHConnection import SshCommandExecutor
from LogerConfig import setup_logging

setup_logging()
logger = logging.getLogger()


def configure_args():
    args_parser = argparse.ArgumentParser(description='Подключение к VM.')

    args_parser.add_argument('--filepath', required=True, help='Путь до файла')
    args_parser.add_argument('--username', required=True, help='Имя для подключения')
    args_parser.add_argument('--passwd', required=True, help='Пароль')

    args = args_parser.parse_args()
    return args


def main():
    args = configure_args()
    command_handler = SshCommandExecutor(hostname='192.168.0.36', username=args.username, password=args.passwd)
    df = command_handler.read_csv(args.filepath)
    file_checksum_handler = FileChecksumHandler(df, command_handler)
    file_checksum_handler.print_df(file_checksum_handler.md5_table, sep=';')


if __name__ == '__main__':
    main()
