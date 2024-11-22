import pygame
from menus.Menu import Menu
from menus.options import Options
import os

from menus.Menu import COLORS


class Game_over(Menu): # Herança: Game_over herda da classe base Menu
    def __init__(self, screen):
        """
        Inicializa o menu de 'Game Over', configurando o título, botões e o fundo.
        """
        super().__init__(screen)
        self.options = Options()  # Opções disponíveis no menu
        self.title = "Game Over"  # Título do menu
        self.button_infos = {"Main menu":self.options.menu, "Exit":self.options.exit} # Configuração dos botões

        # Carrega e redimensiona a imagem de fundo
        base_path = os.path.dirname(__file__) 
        image_path = os.path.join(base_path, '..','..', 'images', 'menu', 'magesurvivorgameover.png')
        image_path = os.path.abspath(image_path) 
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))


    def display_menu(self, jogo):   
        """
        Exibe o menu de 'Game Over' na tela e gerencia a interação com os botões.
        """
        self.screen.blit(self.background, (0, 0)) # Desenha o fundo na tela
        
        # Cria e exibe os botões
        self.create_buttons(button_infos = self.button_infos)
        self.display_text(f"Pontuação: {jogo.player.score}", 80, (self.width // 3, self.height // 2))
        self.draw_buttons()

        pygame.display.flip()  # Atualiza a tela com as mudanças
        return self.handle_menu_events()  # Gerencia os eventos do menu
    

    def handle_menu_events(self):
        """
        Gerencia os eventos no menu, como cliques do mouse e fechamento da janela.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Fecha o jogo se o evento for QUIT
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Clique esquerdo do mouse
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons: # Verifica se algum botão foi clicado
                    if button.rect.collidepoint(mouse_pos):
                        return button.click()
    

    
    def gameover_options(self, jogo):
        """
        Define as ações com base na opção selecionada no menu.
        """

        selected_option = self.display_menu(jogo)
        
        if selected_option == self.options.menu: # Volta ao menu principal

            jogo.active_state = "main_menu"

        elif selected_option == self.options.exit:  # Sai do jogo
            pygame.quit()
            exit()
            
        
        