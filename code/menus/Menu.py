import pygame
import os

from menus.Button import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
COLORS = {"WHITE":WHITE,"BLACK":BLACK,"GRAY":GRAY}

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen = screen
      
        base_path = os.path.dirname(__file__)  # Diretório atual do arquivo
        image_path = os.path.join(base_path, '..','..', 'images', 'menu', 'magesurvivor.png')
        image_path = os.path.abspath(image_path)  # Converte para um caminho absoluto
    # Verifique o caminho da imagem

        # Carrega e ajusta a imagem ao tamanho da tela
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.button_size = (400, 70)  # Largura e altura dos botões
        self.spacing = 20  # Espaço entre os botões
        self.start_y = 50  # Deslocamento do topo da tela
        self.buttons = []


    def display_menu(self, title, button_infos):   
        self.screen.blit(self.background, (0, 0))  # Limpa a tela para evitar sobreposição
        
        self.create_buttons(button_infos=button_infos)
        #self.display_text(title, 80, (self.width // 3.4, self.height // 4))
        self.draw_buttons()

        pygame.display.flip()  # Atualiza a tela
        return self.handle_menu_events()


    def display_text(self, text, size, position):
        font = pygame.font.SysFont('Corbel', size)
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, position)

    def create_buttons(self, button_infos : dict):
        """Cria os botões e adiciona-os ao menu."""
        total_height = len(button_infos) * self.button_size[1] + (len(button_infos) - 1) * self.spacing
        start_x = (self.width - self.button_size[0]) // 2
        current_y = self.start_y + (self.height - total_height) // 2  # Centraliza verticalmente

        for text,option in button_infos.items():

            rect = pygame.Rect(start_x, current_y, *self.button_size)
            button = Button(rect=rect, text=text, option=option)

            self.buttons.append(button)

            current_y += self.button_size[1] + self.spacing

    def draw_buttons(self):
        """Desenha os botões na tela."""
        for button in self.buttons:
            button.draw(self.screen)

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

        return None

