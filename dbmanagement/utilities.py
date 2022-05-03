import hashlib
from django.db import connection

def run_statement(statement):
    cursor= connection.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def encrypt_password(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

#take password as input and compare with "password1"
def check_password(plain_password, hashed_password):
    tmp_sha = encrypt_password(plain_password)
    if(tmp_sha == hashed_password):
        return True
    return False

