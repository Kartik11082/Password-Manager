from cryptography.fernet import Fernet

class EncryptDeCrypt():

    def generate_key(self):
        if not (self.checkKeyExist()):
            key  = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)

    def load_key(self):
        return (open("secret.key", "rb").read())

    def checkKeyExist(self):
        try:
            if(open("secret.key", "rb").read()):
                return True
        except:
            return False

    def encrypt_message(self,message):
        key = self.load_key()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)
        return encrypted_message

    def decrypt_message(self,message):
        key = self.load_key()
        # encoded_message = message.encode()
        f = Fernet(key)
        decrypted_message = f.decrypt(message)
        return decrypted_message