import hashlib
import hmac
import time
import base64
import os
import json

class Auth:
    def __init__(self):
        self.auth_file = 'auth.json'
        self.data = self._load_auth_data()

    def _load_auth_data(self):
        if os.path.exists(self.auth_file):
            with open(self.auth_file, 'r') as f:
                return json.load(f)
        return {'master_password': None, '2fa_secret': None}

    def _save_auth_data(self):
        with open(self.auth_file, 'w') as f:
            json.dump(self.data, f)

    def _generate_2fa_secret(self):
        return base64.b32encode(os.urandom(20)).decode('utf-8')

    def _get_totp_token(self, secret):
        # Get current 30-second time window
        time_window = int(time.time() // 30)
        # Create HMAC-SHA1 hash
        key = base64.b32decode(secret)
        msg = time_window.to_bytes(8, 'big')
        h = hmac.new(key, msg, hashlib.sha1).digest()
        # Generate 6-digit code
        offset = h[-1] & 0xf
        code = ((h[offset] & 0x7f) << 24 |
                (h[offset + 1] & 0xff) << 16 |
                (h[offset + 2] & 0xff) << 8 |
                (h[offset + 3] & 0xff))
        return f"{code % 1000000:06d}"

    def setup(self, master_password):
        # Hash master password
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
        
        # Generate 2FA secret
        secret = self._generate_2fa_secret()
        
        # Save auth data
        self.data['master_password'] = hashed_password
        self.data['2fa_secret'] = secret
        self._save_auth_data()
        
        return {
            'secret': secret,
            'current_code': self._get_totp_token(secret)
        }

    def verify_password(self, password):
        if not self.data['master_password']:
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == self.data['master_password']

    def verify_2fa(self, code):
        if not self.data['2fa_secret']:
            return False
        current_code = self._get_totp_token(self.data['2fa_secret'])
        return code == current_code

    def is_setup_complete(self):
        return bool(self.data['master_password'] and self.data['2fa_secret'])