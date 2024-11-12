import json
import os
from crypto import Fernet

class Database:
    def __init__(self, key):
        self.fernet = Fernet(key)
        self.db_file = 'passwords.enc'
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.db_file):
            return {}
        
        with open(self.db_file, 'rb') as f:
            encrypted_data = f.read()
            if encrypted_data:
                decrypted_data = self.fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data)
            return {}

    def save_data(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.data).encode())
        with open(self.db_file, 'wb') as f:
            f.write(encrypted_data)

    def add_password(self, service, username, password):
        if service not in self.data:
            self.data[service] = {}
        self.data[service]['username'] = username
        self.data[service]['password'] = password
        self.save_data()

    def get_password(self, service):
        return self.data.get(service)

    def list_services(self):
        return list(self.data.keys())

    def delete_password(self, service):
        if service in self.data:
            del self.data[service]
            self.save_data()
            return True
        return False