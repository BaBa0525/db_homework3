from random import choices
from hashlib import sha256

ALL_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def generateSalt(*, saltLength: int = None):
    if saltLength is None:
        raise 'Please always specify the salt length'

    characters = choices(ALL_CHARACTERS, k=saltLength)
    return ''.join(characters)

def getHashed(*args: str):
    hasher = sha256()

    for arg in args:
        hasher.update(arg.encode('utf8'))

    return hasher.hexdigest()

