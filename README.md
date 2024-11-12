# Secure Password Manager with 2FA

A secure password manager implementation with two-factor authentication support.

## Features

- Master password protection
- Two-factor authentication (2FA) using TOTP
- Encrypted password storage
- Generate secure random passwords
- Add, retrieve, list, and delete passwords
- QR code generation for easy 2FA setup

## Security Features

- PBKDF2 key derivation from master password
- Fernet symmetric encryption for password storage
- TOTP-based two-factor authentication
- Secure random password generation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the password manager:
```bash
python password_manager/main.py
```

3. Follow the setup process to:
   - Create a master password
   - Set up 2FA using the displayed QR code or secret key

## Usage

1. Login with your master password and 2FA code
2. Choose from available options:
   - Add new password
   - Retrieve existing password
   - List saved services
   - Delete password
   - Logout
   - Exit

## Security Notes

- Master password is never stored directly
- Passwords are encrypted before storage
- 2FA is required for each login
- Generated passwords include uppercase, lowercase, numbers, and special characters