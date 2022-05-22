from os import path, getcwd

DEBUG=True 

BASE_DIR = path.abspath(getcwd())
DB_NAME = 'db_homework.db'

DB_URI = f'sqlite+pysqlite3:///{ BASE_DIR }/{ DB_NAME }'
SECRET_KEY = 'dev'
