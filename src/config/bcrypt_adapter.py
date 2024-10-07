import bcrypt
class BcryptAdapter:
    def hash(self, password: str):
        salt = bcrypt.gensalt()
        password_utf8 = password.encode('utf-8')
        return bcrypt.hashpw(password_utf8, salt)
    def compare(self, password:str, hashed):
        password_utf8 = password.encode('utf-8')
        # hash_utf8 = hashed.encode('utf-8')
        return bcrypt.checkpw(password_utf8, hashed)