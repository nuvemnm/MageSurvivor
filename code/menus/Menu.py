import pygame

from menus.Button import Button
from data_manager import DataManager
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)
COLORS = {"WHITE":WHITE,"BLACK":BLACK,"GRAY":GRAY, "BLUE": BLUE}

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 60)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.button_size = (400, 70)  # Largura e altura dos botões
        self.spacing = 20  # Espaço entre os botões
        self.start_y = 170  # Deslocamento do topo da tela
        self.user_text = ""
        self.password_text = ""
        self.active_input = None
        self.buttons = []
        self.user_rect = pygame.Rect((self.width/2)-200, 260, 400, 50)
        self.password_rect = pygame.Rect((self.width/2)-200, 340, 400, 50)
        self.data = DataManager()


        base_path = os.path.dirname(__file__)  # Diretório atual do arquivo
        image_path = os.path.join(base_path, '..','..', 'images', 'menu', 'magesurvivorlogin.png')
        image_path = os.path.abspath(image_path)  # Converte para um caminho absoluto
    # Verifique o caminho da imagem

        # Carrega e ajusta a imagem ao tamanho da tela
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))

    def display_menu(self, title, button_infos):   
        self.screen.blit(self.background, (0, 0))  # Limpa a tela para evitar sobreposição # Limpa a tela para evitar sobreposição
        
        self.draw_imput()
        
        self.create_buttons(button_infos=button_infos)
        #self.display_text(title, 80, (self.width // 3.4, self.height // 38))
        self.draw_buttons()

        pygame.display.flip()  # Atualiza a tela
        return self.handle_menu_events()


    def display_text(self, text, size, position):
        font = pygame.font.Font(None, size)
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.user_rect.collidepoint(event.pos):
                        self.active_input = "user"
                    elif self.password_rect.collidepoint(event.pos):
                        self.active_input = "password"
                    else:
                        self.active_input = None
                
            if event.type == pygame.KEYDOWN:
                if self.active_input == "user":
                    #pygame.draw.rect(pygame.draw.rect(self.screen, BLUE, self.user_rect, 2))
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

                elif self.active_input == "password":
                    #pygame.draw.rect(self.screen, BLUE, self.password_rect, 2)
                    if event.key == pygame.K_BACKSPACE:
                        self.password_text = self.password_text[:-1]
                    else:
                        self.password_text += event.unicode
        return None

    
    def draw_imput(self):
        
        

        # Desenhar as caixas de entrada
        pygame.draw.rect(self.screen, BLUE if self.active_input == "user" else BLACK, self.user_rect, 2)
        pygame.draw.rect(self.screen,  BLUE if self.active_input == "password" else BLACK, self.password_rect, 2)

        # Renderizar texto
        user_surface = self.font.render(self.user_text, True, BLACK)
        password_surface = self.font.render("*" * len(self.password_text), True, BLACK)

        # Blitar texto nas caixas
        self.screen.blit(user_surface, (self.user_rect.x + 5, self.user_rect.y + 5))
        self.screen.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))

        # Mostrar os títulos
        self.screen.blit(self.font.render("Usuário:", True, BLACK), (160, 260))
        self.screen.blit(self.font.render("Senha:", True, BLACK), (160, 340))