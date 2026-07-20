import sqlite3

from repositories import user_repository

def get_all_users(db: sqlite3.Connection):
    return user_repository.get_all_users(db)
