import pygame
import os
from os import join
from jogador import Jogador


class Login:
    def __init__(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.archive = os.path.join(self.base_path, 'data_login', 'user.txt')
        self.nickname = None
        self.password = None
        self.score = 0
        
    
    def extrair_dados(self, search_name):
        try:
            with open(self.archive, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if linha:
                        partes = linha.split(",")
                        if len(partes) == 3:
                            nickname, score, _ = partes
                            if nickname == search_name:
                                print("Usuário encontrado!")
                                print(f"Nome: {nickname}")
                                print(f"Score: {score}")
                                return True

                # Se terminar o loop sem encontrar o usuário
                print("Usuário não cadastrado.")
                return False
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
            return None


    def cadastrar(self):
        
        while not self.nickname or not self.password:
            self.nickname = input("Digite um nickname: ").strip()
            self.password = input("Digite uma senha: ").strip()

        linha = f"{self.nickname},{self.score},{self.password}\n"
        if not self.extrair_dados(self.nickname):
            try:
                with open(self.archive, 'a', encoding = 'utf-8') as arquivo:
                    arquivo.write(linha)
                print(f"Dados salvos com sucesso: {linha.strip()}")
            except Exception as e:
                print(f"Erro ao escrever no arquivo: {e}")



