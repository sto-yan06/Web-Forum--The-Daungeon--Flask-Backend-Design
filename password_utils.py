from flask_bcrypt import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode("utf-8"), hashed_password)