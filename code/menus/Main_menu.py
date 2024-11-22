import pygame
from menus.Menu import Menu
from menus.Menu import COLORS
from menus.options import Options


class Main_menu(Menu): # Herança: Main_menu herda da classe base Menu
    def __init__(self, screen):
        """
        Inicializa o menu principal, herdando as funcionalidades da classe Menu
        e adicionando opções específicas para este menu.
        """
        super().__init__(screen)

        self.options = Options()  # Composição: Main_menu utiliza a classe Options
        self.title = "MageSurvivor"  # Título do menu principal
        # Polimorfismo: Configuração específica dos botões para este menu
        self.button_infos = {"Confirm":self.options.confirm, "New Game":self.options.new_game, "Exit":self.options.exit}
        
        

    def display_menu(self, jogo):
        """
        Exibe o menu principal e gerencia as ações selecionadas pelo usuário.

        """
        selected_option = super().display_menu(self.title,self.button_infos)
        # Uso do método da classe base para exibir o menu com configurações específicas

        if selected_option == self.options.confirm: # Ação ao confirmar o login
            if self.data.verify_login(self.user_text, self.password_text): # Verifica credenciais
                jogo.active_state = "running" # Muda o estado do jogo para 'executando'
          
            else: 
                jogo.active_state = "main_menu"  # Retorna ao menu principal

        elif selected_option == self.options.new_game: # Inicia um novo jogo
            jogo.active_state = "register_menu"
            

        elif selected_option == self.options.exit: # Sai do jogo
            pygame.quit()
            exit()

        else:
            jogo.active_state = "main_menu" # Caso nenhuma opção seja selecionada, permanece no menu
            
    def reset(self, jogo):
        """
        Restaura os valores iniciais do jogador e do jogo.

        """
        # Reinicia os atributos do jogador
        jogo.player.alive = True
        jogo.player.score = 0
        jogo.player.actual_level = 1
        jogo.player.speed = 100
        jogo.player.staticLife = 50
        jogo.player.dinamicLife = jogo.player.staticLife
        jogo.player.experience = 0
        jogo.player.experience_threshold = 1
        jogo.player.spell.damage = 5
        jogo.player.spell_cadence = 1500
        
        # Reinicia os atributos do jogo
        jogo.actual_time = 0
        jogo.elapsed_time = 0
        
        # Remove todos os inimigos da tela
        for enemy in jogo.enemy_sprites:
            enemy.kill()
