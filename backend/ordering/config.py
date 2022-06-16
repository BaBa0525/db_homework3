from os import path, getcwd

DEBUG = True
LOGGING = False 

BASE_DIR = path.abspath(getcwd())
DB_NAME = 'db_homework.db'

DB_URI = f'sqlite:///{ BASE_DIR }/{ DB_NAME }'
SECRET_KEY = 'dev'
