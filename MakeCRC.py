import argparse

from FileChecksumHandler import FileChecksumHandler
from SSHConnection import SSHConnection
from SftpManager import SftpManager

def configure_args():
    args_parser = argparse.ArgumentParser(description='Подключение к VM.')

    args_parser.add_argument('--filepath', required=True, help='Путь до файла')
    args_parser.add_argument('--username', required=True, help='Имя для подключения')
    args_parser.add_argument('--passwd', required=True, help='Пароль')

    args = args_parser.parse_args()
    return args

def main():
    args = configure_args()
    sshConnection = SSHConnection(hostname='127.0.0.1', username=args.username, password=args.passwd)
    sftp = sshConnection.sftp
    sftpManager = SftpManager(sftp)
    data = sftpManager.read_csv_sftp(args.filepath)
    fileChecksumHandler = FileChecksumHandler(data, sftp)
    fileChecksumHandler.print_df(fileChecksumHandler.md5_table, sep=';')
    sftpManager.send_df_sftp(fileChecksumHandler.md5_table, 'etalon.csv', args.filepath + '/etalon.csv')

if __name__ == '__main__':
    main()