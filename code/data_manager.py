import pygame
import os
from os.path import join
#from jogador import Jogador
import utils

#Clasee responsável por lidar com o banco de dados que armazna nome de usuário, pontuação e senha
class DataManager:
    def __init__(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.archive = os.path.join(self.base_path, 'data_login', 'user.txt')
        self.nickname = None
        self.password = None
        self.score = 0
        
    #Verifica se certo usuário existe
    def extrair_dados(self, search_name):
        try:
            with open(self.archive, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    partes = linha.split(",")
                    if len(partes) == 3:
                        nickname, score, _ = partes
                        if nickname == search_name:
                            print("Usuário encontrado!")
                            print(f"Nome: {nickname}")
                            print(f"Score: {score}")
                            return True

                #Se terminar o loop sem encontrar o usuário
                print("Usuário não cadastrado.")
                return False
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
            return None

    #Insere os dados do jogador no banco de dados
    def cadastrar(self, nickname, password):
        self.nickname = nickname
        self.password = utils.encrypt_password(password)

        password_hash_str = self.password.decode('utf-8')

        linha = f"{self.nickname},{self.score},{password_hash_str}\n"
        if not self.extrair_dados(self.nickname):
            try:
                with open(self.archive, 'a', encoding = 'utf-8') as arquivo:
                    arquivo.write(linha)
                print(f"Dados salvos com sucesso: {linha.strip()}")
            except Exception as e:
                print(f"Erro ao escrever no arquivo: {e}")


    #Verifica se nome usuáio e senha existem no banco de dados
    def verify_login(self, nick_input, pass_input):
        try:
            with open(self.archive, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    partes = linha.split(",")
                    if len(partes) == 3:
                        self.nickname, score, self.password = partes
                        stored_password_bytes = self.password.encode('utf-8')

                        if self.nickname == nick_input:
                            if utils.verify_password(stored_password_bytes, pass_input):
                                print("Usuário encontrado!")
                                print(f"Nome: {self.nickname}")
                                print(f"Score: {score}")
                                return True
                            
                            else:
                                print("Senha incorreta tente novamente.")
                                return False
                            
                # Se terminar o loop sem encontrar o usuário
                print("Usuário não cadastrado.")
                return False
            
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
            return None
        
    #Atuliza a pontuação do jogador caso ela seja maior que a pontuação armazenada no banco de dados
    def write_score(self, nick_input, score_input):
        try:
            # Ler todas as linhas do arquivo
            with open(self.archive, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()

            # Reescrever o arquivo com as alterações
            with open(self.archive, 'w', encoding='utf-8') as arquivo:
                usuario_encontrado = False
                for linha in linhas:
                    linha = linha.strip()
                    partes = linha.split(",")
                    if len(partes) == 3:
                        nickname, score, password = partes
                        score = int(score)  # Converte o score armazenado para inteirow

                        if nick_input == nickname:
                            usuario_encontrado = True
                            if score_input > score:
                                # Atualiza o score somente se for maior
                                new_line = f"{nickname},{score_input},{password}\n"
                                arquivo.write(new_line)
                                print(f"Score atualizado para {score_input}!")
                            else:
                                # Mantém a linha inalterada se o novo score não for maior
                                arquivo.write(linha + "\n")
                                print("O novo score não é maior que o atual. Nenhuma alteração feita.")
                        else:
                            # Mantém a linha inalterada
                            arquivo.write(linha + "\n")
                    else:
                        # Caso a linha não seja válida, mantém como está
                        arquivo.write(linha + "\n")

                if not usuario_encontrado:
                    print("Usuário não encontrado!")

        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
        except Exception as e:
            print(f"Erro: {e}")
