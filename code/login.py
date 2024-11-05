import pygame
import sqlite3 

#GPT CRIOPU MAS NAO TESTEI COLOQUEI SO PRA DAR DE EX

class Login:
    def __init__(self, database_path):
        self.database_path = database_path

    def create_database(self):
        # Cria a tabela de usuários se ainda não existir
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          username TEXT PRIMARY KEY,
                          password TEXT NOT NULL)''')
        conn.commit()
        conn.close()

    def authenticate(self, username, password):
        # Verifica se o usuário e senha são válidos
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def register_user(self, username, password):
        # Registra um novo usuário (para teste ou novas contas)
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False  # Usuário já existe
        conn.close()
        return success