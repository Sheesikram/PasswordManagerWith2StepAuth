import base64
import os
import hashlib
import hmac

class Fernet:
    def __init__(self, key):
        self.key = base64.urlsafe_b64decode(key)
        if len(self.key) != 32:
            raise ValueError("Invalid key")

    def encrypt(self, data):
        iv = os.urandom(16)
        hmac_key = self.key[:16]
        enc_key = self.key[16:]
        
        # Simple XOR encryption
        encrypted = bytearray()
        for i, byte in enumerate(data):
            key_byte = enc_key[i % len(enc_key)]
            encrypted.append(byte ^ key_byte)
        
        # Calculate HMAC
        h = hmac.new(hmac_key, iv + encrypted, hashlib.sha256)
        
        # Combine IV + encrypted data + HMAC
        result = iv + encrypted + h.digest()
        return base64.urlsafe_b64encode(result)

    def decrypt(self, token):
        try:
            data = base64.urlsafe_b64decode(token)
            iv = data[:16]
            hmac_sig = data[-32:]
            encrypted = data[16:-32]
            
            # Verify HMAC
            hmac_key = self.key[:16]
            h = hmac.new(hmac_key, iv + encrypted, hashlib.sha256)
            if not hmac.compare_digest(h.digest(), hmac_sig):
                raise ValueError("Invalid token")
            
            # Decrypt using XOR
            enc_key = self.key[16:]
            decrypted = bytearray()
            for i, byte in enumerate(encrypted):
                key_byte = enc_key[i % len(enc_key)]
                decrypted.append(byte ^ key_byte)
            
            return bytes(decrypted)
        except Exception:
            raise ValueError("Invalid token")

def generate_key(master_password):
    # Use PBKDF2-like key derivation
    salt = b'secure_salt_value'
    key = hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode(),
        salt,
        100000,
        dklen=32
    )
    return base64.urlsafe_b64encode(key)

def generate_password(length=16):
    """Generate a secure random password"""
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = []
    
    # Ensure at least one of each required character type
    password.append(os.urandom(1)[0] % 26 + 65)  # uppercase
    password.append(os.urandom(1)[0] % 26 + 97)  # lowercase
    password.append(os.urandom(1)[0] % 10 + 48)  # digit
    password.append(ord("!@#$%^&*"[os.urandom(1)[0] % 8]))  # special
    
    # Fill the rest randomly
    while len(password) < length:
        password.append(ord(chars[os.urandom(1)[0] % len(chars)]))
    
    # Shuffle the password
    for i in range(len(password) - 1, 0, -1):
        j = os.urandom(1)[0] % (i + 1)
        password[i], password[j] = password[j], password[i]
    
    return ''.join(chr(c) for c in password)