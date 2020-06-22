import os
import shutil

import Auto
import Security


class Data:
    def __init__(self)->None:
        self.__db_path = os.path.abspath('DataBase')
        self.__user_secret_key = b''

    def create_new_user_db(self) -> None:
        if not os.path.exists('DataBase'):
            os.mkdir('DataBase')
        return None

    def authorized(self, user: str, password: str) -> bool:
        if isinstance(user, str) and isinstance(password, str) is False:
            print("Неверный тип данных!")
            return False
        if not os.path.exists(user):
            print('Неверные данные!')
            return False
        with open(os.path.abspath(user) + '/USER_INFO/password.txt', 'r') as file:
            user_password = file.read()
        if Auto.Autorise().check_password(user_password, password):
            with open(os.path.abspath(user) + '/USER_INFO/enc_key.txt', 'rb') as byte_enc_key_file:
                self.__user_secret_key = byte_enc_key_file.read()
            return True
        else:
            print('Неверные данные!')
            return False

    def insert(self, user: str, password: str, enc_key: bytes, hashed_user: bytes) -> bool:
        if isinstance(user, str) and isinstance(password, str) and isinstance(enc_key, bytes) is False:
            print("Неверный тип данных!")
            return False

        if os.path.exists(user):
            print('Репозиторий с таким именем существует!')
            return False
        else:
            home_path = os.getcwd()
            os.mkdir(user)
            nick = hashed_user
            file_pass = password
            nick += enc_key
            os.chdir(user)
            os.mkdir('USER_INFO')
            os.mkdir('NOTES')
            os.chdir(home_path)
            with open(os.path.abspath(user) + '/USER_INFO/login.txt', 'wb') as byte_login_file:
                byte_login_file.write(hashed_user)
            with open(os.path.abspath(user) + '/USER_INFO/password.txt', 'w') as password_file:
                password_file.write(password)
            with open(os.path.abspath(user) + '/USER_INFO/enc_key.txt', 'wb') as file:
                file.write(enc_key)
        print('Создание аккаунта прошло успешно!')

        return True

    def update(self, user: str, password: str) -> bool:
        if isinstance(user, str) and isinstance(password, str) is False:
            print("Неверный тип данных!")
            return False
        hash_password = Security.Security().gen_user_secret_key(password)
        with open(self.__db_path + '/' + user + '/USER_INFO/password.txt', 'w') as file:
            file.seek(0)
            file.write(hash_password)

        return False

    def delete(self, user: str) -> bool:
        if isinstance(user, str) is False:
            print("Неверный тип данных!")
            return False
        os.chdir(self.__db_path)
        if os.path.exists(self.__db_path + '/' + user):
            shutil.rmtree(self.__db_path + '/' + user)
            print('Пользователь удален')
            return True
        print('Не существует такого пользователя!')
        return False

    def get_secret_key(self) -> bytes:
        return self.__user_secret_key

    def get_path_to_user_dir(self, user: str) -> str:
        if os.path.exists(user):
            return os.path.abspath(user)
        else:
            return ''
