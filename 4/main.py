import os

import Auto
import Data
import Notes
import Security


def main_menu() -> None:
    print('1-Войти в аккаунт')
    print('2-Зарегестрироваться')
    print('3-Выход')
    return None


def account_edit() -> None:
    print('1-Работа с заметками')
    print('2-Изменить пароль')
    print('3-Удалить аккаунт')
    print('4-Выход в главное меню')
    return None


def notes_menu() -> None:
    print('1-Добавить заметку')
    print('2-Получить содержимое заметки заметку')
    print('3-Обновить заметку')
    print('4-Удалить заметку')
    print('5-Количество заметок')
    print('6-Выход в меню управления аккаунтом')
    return None


db = Data.Data()
db.create_new_user_db()
os.chdir('DataBase')
sec = Security.Security()
auth_flag = False
secret_key = b''
while True:
    main_menu()
    main_menu_choice = Auto.Autorise().menu_choice()
    print()
    if main_menu_choice == 1:
        user = ''
        password = ''
        while True:
            user = Auto.Autorise().get_correct_str('логин')
            password = Auto.Autorise().get_password()
            if db.authorized(user, password):
                print('Авторизация прошла успешно')
                auth_flag = True
                master_key = sec.gen_master_key(password)
                secret_key = sec.decrypt(db.get_secret_key(), master_key)
            else:
                auth_flag = False
            if auth_flag:
                print()
                break
        while True:
            account_edit()
            user_choice = Auto.Autorise().menu_choice()
            print()
            if user_choice == 1:
                note = Notes.Notes(user)
                while True:
                    notes_menu()
                    notes_choice = Auto.Autorise().menu_choice()
                    print()
                    if notes_choice == 1:
                        note_name = Auto.Autorise().get_correct_str('название заметки')
                        note_message = Auto.Autorise().get_data_from_file()
                        if note.create_new_note(note_name,
                                                sec.encrypt(bytes(note_message, encoding='utf-8'), secret_key)):
                            print('Заметка успешно создана')
                            print()
                        else:
                            print('Заметка с таким именем уже существует')
                            print()
                    elif notes_choice == 2:
                        note_name = Auto.Autorise().get_correct_str('название заметки')
                        data = note.read_note(note_name)
                        if data is not None:
                            data = sec.decrypt(data, secret_key)
                            print(data.decode())
                            print()
                    elif notes_choice == 3:
                        note_name = Auto.Autorise().get_correct_str('название заметки')
                        note_message = Auto.Autorise().get_data_from_file()
                        if note.update_note(note_name, sec.encrypt(bytes(note_message, encoding='utf-8'), secret_key)):
                            print('Заметка успешна изменена')
                            print()
                        else:
                            print("Такой заметки не существует заметки")
                            print()

                    elif notes_choice == 4:
                        note_name = Auto.Autorise().get_correct_str('название заметки')
                        if note.delete_note(note_name):
                            print('Заметка успешно удалена')
                            print()
                        else:
                            print("Такой заметки не существует заметки")
                            print()
                    elif notes_choice == 5:
                        print('Список заметок: ')
                        note.notes_count()
                        print()
                    elif notes_choice == 6:
                        break

            elif user_choice == 2:
                new_password = Auto.Autorise().get_password()
                db.update(user, new_password)
                print('Пароль успешно изменен')
            elif user_choice == 3:
                db.delete(user)
                break
            elif user_choice == 4:
                break
            else:
                print('Неправильная команда')

    elif main_menu_choice == 2:
        user = Auto.Autorise().get_correct_str('логин')
        password = Auto.Autorise().get_password()
        master_key = sec.gen_master_key(password)
        enc_key = sec.gen_secret_key()
        hash_passw = sec.gen_user_secret_key(password)
        encrypt_user = sec.encrypt(bytes(user, encoding='utf-8'), enc_key)
        db.insert(user, hash_passw, sec.encrypt(enc_key, master_key), encrypt_user)
        print('Теперь можете авторизироваться')
        print()
    elif main_menu_choice == 3:
        break
    else:
        print('Неправильная команда')
