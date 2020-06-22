import hashlib
import random

from Crypto import Random
from Crypto.Cipher import AES


class Security:

    def __init__(self) -> None:
        self._SALT = b'8_TuDUK9IpJKaM7NWkpSQcMlVh0ZoEmYdeIOjvItOSk='
        self._BLOCK_SIZE = 16  # Размер блока
        self._IV456 = b'yo_esK1DOHg2x-3L'  # Вектор инициализации

    def gen_user_secret_key(self, password: str) -> str:
        if isinstance(password, str) is False:
            raise TypeError("Неверный тип данных!")
        salt_s = '8_TuDUK9IpJKaM7NWkpSQcMlVh0ZoEmYdeIOjvItOSk='
        salt_b = self._SALT
        hash_pass = hashlib.sha256(salt_b + password.encode()).hexdigest() + '|' + salt_s
        return hash_pass

    def gen_master_key(self, password: str) -> bytes:
        if isinstance(password, str) is False:
            raise TypeError("Неверный тип данных!")
        master_key = hashlib.pbkdf2_hmac('sha256', password.encode(), self._SALT, 100000)
        return master_key

    def gen_secret_key(self) -> bytes:
        return Random.new().read(32)

    def __fill_random_bytes(self, text: bytes, length: int) -> bytes:
        while len(text) % length != 0:  # кратно 16 байт
            symbol = bytes()
            if len(text) > 0:
                pos = random.randint(0, len(text))
                symbol = text[pos: pos + 1]
            text += symbol
        return text

    def encrypt(self, message: bytes, secret_key: bytes) -> bytes:
        if isinstance(message, bytes) is False:
            raise TypeError("Тип текста не подходит")
        if isinstance(secret_key, bytes) is False:
            raise TypeError("Тип ключа не подходит")
        len_block = len(message).to_bytes(length=self._BLOCK_SIZE, byteorder='big')
        message = len_block + message
        message_byte = self.__fill_random_bytes(message, self._BLOCK_SIZE)
        obj = AES.new(secret_key, AES.MODE_CBC, self._IV456)
        ciphertext = obj.encrypt(message_byte)
        return ciphertext

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        if isinstance(ciphertext, bytes) is False:
            raise TypeError("Тип текста не подходит")
        if isinstance(key, bytes) is False:
            raise TypeError("Тип ключа не подходит ")
        if len(ciphertext) % self._BLOCK_SIZE != 0:
            raise ValueError("Длина шифротекста не кратна блоку")
        obj = AES.new(key, AES.MODE_CBC, self._IV456)
        text = obj.decrypt(ciphertext)
        size = int.from_bytes(text[:self._BLOCK_SIZE], byteorder='big')
        text = text[self._BLOCK_SIZE:size + self._BLOCK_SIZE]
        return text
