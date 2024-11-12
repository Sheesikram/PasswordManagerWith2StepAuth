import getpass
import os
from auth import Auth
from database import Database
from crypto import generate_key, generate_password

class PasswordManager:
    def __init__(self):
        self.auth = Auth()
        self.db = None

    def setup(self):
        if self.auth.is_setup_complete():
            print("Password manager is already set up!")
            return

        print("\n=== Password Manager Setup ===")
        master_password = getpass.getpass("Create master password: ")
        confirm_password = getpass.getpass("Confirm master password: ")

        if master_password != confirm_password:
            print("Passwords don't match!")
            return

        # Setup authentication
        setup_data = self.auth.setup(master_password)
        
        print("\nYour 2FA secret key:", setup_data['secret'])
        print("Current 2FA code:", setup_data['current_code'])
        print("\nIMPORTANT: Save this secret key securely!")
        print("You can use any TOTP-compatible authenticator app (Google Authenticator, Authy, etc.)")
        input("\nPress Enter when you've saved your 2FA secret...")

    def login(self):
        if not self.auth.is_setup_complete():
            print("Please set up the password manager first!")
            return False

        master_password = getpass.getpass("Enter master password: ")
        if not self.auth.verify_password(master_password):
            print("Invalid master password!")
            return False

        code = input("Enter 2FA code: ")
        if not self.auth.verify_2fa(code):
            print("Invalid 2FA code!")
            return False

        # Initialize database with derived key
        key = generate_key(master_password)
        self.db = Database(key)
        return True

    def add_password(self):
        service = input("Service name: ")
        username = input("Username: ")
        use_generated = input("Generate password? (y/n): ").lower() == 'y'
        
        if use_generated:
            password = generate_password()
            print(f"Generated password: {password}")
        else:
            password = getpass.getpass("Password: ")

        self.db.add_password(service, username, password)
        print("Password saved successfully!")

    def get_password(self):
        service = input("Service name: ")
        data = self.db.get_password(service)
        if data:
            print(f"\nUsername: {data['username']}")
            print(f"Password: {data['password']}")
        else:
            print("Service not found!")

    def list_services(self):
        services = self.db.list_services()
        if services:
            print("\nSaved services:")
            for service in services:
                print(f"- {service}")
        else:
            print("No saved passwords!")

    def delete_password(self):
        service = input("Service name: ")
        if self.db.delete_password(service):
            print("Password deleted successfully!")
        else:
            print("Service not found!")

    def run(self):
        while True:
            if not self.db:
                print("\n=== Password Manager ===")
                print("1. Setup")
                print("2. Login")
                print("3. Exit")
                
                choice = input("\nChoice: ")
                
                if choice == '1':
                    self.setup()
                elif choice == '2':
                    if self.login():
                        print("Login successful!")
                    else:
                        continue
                elif choice == '3':
                    break
                else:
                    print("Invalid choice!")
                    continue
            
            else:
                print("\n=== Password Manager ===")
                print("1. Add password")
                print("2. Get password")
                print("3. List services")
                print("4. Delete password")
                print("5. Logout")
                print("6. Exit")
                
                choice = input("\nChoice: ")
                
                if choice == '1':
                    self.add_password()
                elif choice == '2':
                    self.get_password()
                elif choice == '3':
                    self.list_services()
                elif choice == '4':
                    self.delete_password()
                elif choice == '5':
                    self.db = None
                elif choice == '6':
                    break
                else:
                    print("Invalid choice!")

if __name__ == "__main__":
    manager = PasswordManager()
    manager.run()