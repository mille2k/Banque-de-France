from typing import Optional

import Data
import os


class Notes:
    def __init__(self, user: str):
        self.__user_dir = Data.Data().get_path_to_user_dir(user)

    def create_new_note(self, note_name: str, note_data: bytes) -> bool:
        if isinstance(note_data, bytes) and isinstance(note_name, str) is False:
            print("Неверный тип данных!")
            return False
        if os.path.exists(self.__user_dir + '/NOTES/' + note_name + '.txt'):
            return False
        with open(self.__user_dir + f'/NOTES/{note_name}.txt', 'wb') as file:
            file.write(note_data)
            return True

    def read_note(self, note_name: str) -> Optional[bytes]:
        if isinstance(note_name, str) is False:
            print("Неверный тип данных!")
            return None
        if os.path.exists(self.__user_dir + f'/NOTES/{note_name}.txt'):
            with open(self.__user_dir + f'/NOTES/{note_name}.txt', 'rb') as file:
                data = file.read()
                return data
        else:
            print("Не существует такой заметки!")
            return None

    def update_note(self, note_name: str, note_data: bytes) -> bool:
        if isinstance(note_data, bytes) and isinstance(note_name, str) is False:
            print("Неверный тип данных!")
            return False
        if os.path.exists(self.__user_dir + f'/NOTES/{note_name}.txt'):
            with open(self.__user_dir + f'/NOTES/{note_name}.txt', 'wb') as file:
                file.seek(0)
                file.write(note_data)
                return True
        else:
            return False

    def delete_note(self, note_name: str) -> bool:
        if isinstance(note_name, str) is False:
            raise Exception("Неверный тип данных!")
        if os.path.exists(self.__user_dir + f'/NOTES/{note_name}.txt'):
            os.remove(self.__user_dir + f'/NOTES/{note_name}.txt')
            return True
        else:
            return False

    def notes_count(self) -> None:
        i = 1
        for filename in os.listdir(self.__user_dir + '/NOTES'):
            file = filename.split('.')
            if file[len(file) - 1] == 'txt':
                print(f'{i}. {filename}')
                i += 1
