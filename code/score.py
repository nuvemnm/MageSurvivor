import pygame
import os
from os import join
from jogador import Jogador



class Score:
    def __init__(self, player):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.archive = os.path.join(self.base_path, 'data_login', 'user.txt')
        self.player = player

    def read_score(self, serch_nickname):
        try:
            with open(self.archive, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if linha:
                        partes = linha.split(",")
                        if len(partes) == 3:
                            nickname = partes[0]
                            score = partes[1]
                            if serch_nickname == nickname:
                               return score
                            else:
                                print("Pontuação não encontrada.")
                                return None
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
            return None

    def write_score(self):
        
        last_score = self.read_score()
        updated_line = []

        new_line = f"{self.player.nickname},{last_score},{self.player.password}\n"
        if last_score != None:
            try:
                with open(self.archive, 'a', encoding = 'utf-8') as arquivo:
                    for linha in arquivo:
                        if last_score <= self.player.score:
                            updated_line.append(new_line)
                        else:
                            new_line.append(linha)

                print(f"Dados salvos com sucesso: {linha.strip()}")
            except Exception as e:
                print(f"Erro ao escrever no arquivo: {e}")