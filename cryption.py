from cryptography.fernet import Fernet

class SimpleEnDecrypt:

    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()
        self.key = key
        self.f = Fernet(self.key)

    def encrypt(self, data):
        out = self.f.encrypt(data.encode('UTF-8'))
        return out.decode('UTF-8')

    def decrypt(self, data):
        out = self.f.decrypt(data.encode('UTF-8'))
        return out.decode('UTF-8')