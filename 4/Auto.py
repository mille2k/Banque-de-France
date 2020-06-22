import hashlib
import os


class Autorise:

    def get_correct_str(self, type: str) -> str:
        bad_symbols = ["\\", "/", ":", "*", "?", "\"", "|", "<", ">"]
        while True:
            flag = True
            user = str(input(f'Введите {type}: '))
            if len(user) == 0:
                print('Недопустимая длина!')
                flag = False
            else:
                for i in range(len(user)):
                    for j in range(len(bad_symbols)):
                        if user[i] == bad_symbols[j]:
                            print('Недопустимые символы!')
                            flag = False
            if flag:
                return user

    def get_password(self) -> str:
        while True:
            password = str(input('Введите пароль: '))
            if len(password) == 0:
                print('Недопустимая длина!')
            else:
                break
        return password

    def get_data_from_file(self) -> str:
        while True:
            file_path = str(input('Введите путь к файлу с заметкой в формате ".txt": '))
            file_expansion = file_path.split('.')
            if file_expansion[len(file_expansion) - 1] == 'txt':
                if os.path.exists(file_path):
                    break
                else:
                    print('Такого файла не существует!')
            else:
                print('Расширение не .TXT!')
        with open(file_path, 'r',encoding= 'utf-8') as file:
            return file.read()

    def check_password(self, hashed_password: str, user_pass: str) -> bool:
        if isinstance(hashed_password, str) is False:
            raise TypeError("Тип хеш-пароля не подходит")
        if isinstance(user_pass, str) is False:
            raise TypeError("Тип пользовательского пароля не подходит")
        hash_password = hashed_password.split('|')
        password = hash_password[0]
        salt = hash_password[1]
        check_password = hashlib.sha256(salt.encode() + user_pass.encode()).hexdigest()
        return password == check_password

    def menu_choice(self) -> int:
        while True:
            try:
                choice = int(input('Ваш выбор:'))
            except ValueError:
                print('Неправильный тип! Нужно число!!')
            else:
                break
        return choice
