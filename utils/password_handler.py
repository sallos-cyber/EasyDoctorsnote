# -*- coding: utf-8 -*-

from os import path
import os
from kivy.logger import Logger
from cryptography.fernet import Fernet

class PasswordHandler:
    
    def __init__(self):
        if not path.exists("secret.key"):
                self.key = Fernet.generate_key()
                with open("secret.key", "wb") as key_file:
                    key_file.write(self.key)
                    Logger.debug(f'PasswordHandler: __init__, I have opened a secret file - it is here! {os.getcwd()}')
        else:
            with open("secret.key", "rb") as key_file:
                self.key = key_file.read()
                Logger.debug(f'PasswordHandler: __init__, I have opened a secret file - it is here! {os.getcwd()}')


    def encrypt_password(self, password):
        Logger.debug(f'PasswordHandler: encrypt_password, this is the current folder: {os.getcwd()}')
        f = Fernet(self.key)
        encrypted_password = f.encrypt(password.encode('utf-8'))
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        f = Fernet(self.key)
        try: 
            decrypted_password = f.decrypt(encrypted_password).decode('utf-8')
            return decrypted_password
        except Exception as e:
            Logger.error(f'PasswordHandler: decrypt_password, error occurred: {e}')
            return None
