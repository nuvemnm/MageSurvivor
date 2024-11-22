import pygame
from menus.Menu import Menu
from menus.options import Options
import os

from menus.Menu import COLORS


class Game_over(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = Options()
        self.title = "Game Over"
        self.button_infos = {"Main menu":self.options.menu, "Exit":self.options.exit}

        base_path = os.path.dirname(__file__)  # Diretório atual do arquivo
        image_path = os.path.join(base_path, '..','..', 'images', 'menu', 'magesurvivorgameover.png')
        image_path = os.path.abspath(image_path)  # Converte para um caminho absoluto
    # Verifique o caminho da imagem

        # Carrega e ajusta a imagem ao tamanho da tela
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))


    def display_menu(self, jogo):   
        self.screen.blit(self.background, (0, 0)) # Limpa a tela para evitar sobreposição 
        
        self.create_buttons(button_infos = self.button_infos)
        self.display_text(f"Pontuação: {jogo.player.score}", 80, (self.width // 3, self.height // 2))
        self.draw_buttons()

        pygame.display.flip()  # Atualiza a tela
        return self.handle_menu_events()
    

    def handle_menu_events(self):
          # Atualiza a posição do mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        return button.click()
    

    
    def gameover_options(self, jogo):

        selected_option = self.display_menu(jogo)
        
        if selected_option == self.options.menu:
            jogo.active_state = "main_menu"
            
         

        elif selected_option == self.options.exit:
            pygame.quit()
            exit()
            
        
        