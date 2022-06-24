import os
import sys
import json
import pickle
from cryptography.fernet import Fernet
from hashlib import sha256

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.globals import PICKLE_ENC, DB_PATH

class Encryption:
    def __init__(self):
        if not self.key_exists(): self.key = self.create_key()
        else: self.key = self.get_key()
        
        
    def create_key(self):
        encryptor = Fernet(PICKLE_ENC.encode())
        key = Fernet.generate_key()
        print("new key has been created")
        encrypted_key = encryptor.encrypt(key)
        json_data = json.dumps({"key": encrypted_key.decode()})
        data = encryptor.encrypt(json_data.encode())
        
        with open(f"{DB_PATH}workmate.pkl", "wb") as file:
            pickle.dump(data, file)
        
        return key
            
    def get_key(self):
        if not os.path.exists(f"{DB_PATH}workmate.pkl"): raise FileNotFoundError
        # print("The key was fetched")
        data = None
        with open(f"{DB_PATH}workmate.pkl", "rb") as file:
            data = pickle.load(file)
            
        decryptor = Fernet(PICKLE_ENC.encode())
        decoded = decryptor.decrypt(data)
        
        encrypted_key = json.loads(decoded.decode())['key']
        
        decrypted_key = decryptor.decrypt(encrypted_key.encode())
        
        return decrypted_key
    
    def key_exists(self):
        return os.path.exists(f"{DB_PATH}workmate.pkl")
    
    def encrypt(self, string: str or int):
        encryptor = Fernet(self.key)
        encrypted_string = encryptor.encrypt(str(string).encode())
        # hashed_hex_string = sha256(encrypted_string).hexdigest()
        return encrypted_string.decode()
        
    
    def decrypt(self, string: str):
        decryptor = Fernet(self.key)
        decrypted_string = decryptor.decrypt(string.encode()).decode()
        return decrypted_string