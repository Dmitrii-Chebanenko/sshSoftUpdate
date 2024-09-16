import logging
import subprocess
import pandas as pd

from io import StringIO

logger = logging.getLogger()


class SshCommandExecutor:
    def __init__(self, hostname, username, password):
        self.__hostname = hostname
        self.__username = username
        self.__password = password

    def execute_remote_command(self, command):
        ssh_command = [
            'sshpass', '-p', self.__password,
            'ssh', '-o', 'StrictHostKeyChecking=no', f'{self.__username}@{self.__hostname}', command
        ]
        result = subprocess.run(ssh_command, capture_output=True, text=True)
        if result.stderr != '':
            logger.error(result.stderr)
        logger.info(result.stdout)
        return result.stdout

    def read_file(self, path: str):
        return self.execute_remote_command(f'cat {path}')

    def read_csv(self, path: str):
        try:
            string_csv = self.read_file(path)

            csv_data = StringIO(string_csv)

            df = pd.read_csv(csv_data, sep=';')

            return df

        except FileNotFoundError:
            print(f"Ошибка: Файл по пути {path} не найден.")
        except pd.errors.EmptyDataError:
            print("Ошибка: Файл пуст.")
        except pd.errors.ParserError:
            print("Ошибка: Ошибка при разборе CSV-файла.")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
