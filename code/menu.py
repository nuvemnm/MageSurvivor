import pygame
from login import Login
import os
from os.path import join

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 60)
        self.selected_option = -1  # Nenhuma opção selecionada inicialmente
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.menu_type = "main"
        self.button_size = (400, 70)  # Largura e altura dos botões
        self.spacing = 20  # Espaço entre os botões
        self.start_y = 50  # Deslocamento do topo da tela
        self.user_rect = pygame.Rect((self.width/2)-150, 200, 300, 50)
        self.password_rect = pygame.Rect((self.width/2)-150, 280, 300, 50)
        self.user_text = ""
        self.password_text = ""
        self.title = ""
        self.active_input = None
        

    def display(self, text, size, position):
        font = pygame.font.SysFont('Corbel', size)
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, position)

    def create_buttons(self, button_texts):
        """Cria uma lista de botões organizados verticalmente."""
        buttons = []
        total_height = len(button_texts) * self.button_size[1] + (len(button_texts) - 1) * self.spacing
        start_x = (self.width - self.button_size[0]) // 2
        current_y = self.start_y + (self.height - total_height) // 2  # Centraliza verticalmente

        for text in button_texts:
            rect = pygame.Rect(start_x, current_y, *self.button_size)
            buttons.append((text, rect))
            current_y += self.button_size[1] + self.spacing
        return buttons
    
    def draw_buttons(self, buttons):
        """Desenha os botões na tela."""
        for text, rect in buttons:
            pygame.draw.rect(self.screen, BLACK, rect)
            label = self.font.render(text, True, WHITE)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

    def display_menu(self):
        self.screen.fill(GRAY)  # Limpa a tela para evitar sobreposição

        if self.menu_type == "main":
            self.title = "MageSurvivor"
            button_texts = ["New Game", "Login", "Exit"]
        elif self.menu_type == "new_game":
            self.title = "Insira nickname e senha"
            self.draw_imput()
            button_texts = ["Criar conta", "Voltar"]
        elif self.menu_type == "login":
            self.title = "Insira seu login e senha:"
            self.draw_imput()
            button_texts = ["Confirm", "Voltar"]
        """
        elif self.menu_type == "magias":
            self.title = "Escolha sua magia:"
            button_texts = ["Magia de fogo", "Magia de gelo", "Magia de raio", "Back"]
        """
        
        buttons = self.create_buttons(button_texts)
        self.draw_buttons(buttons)
        self.display(self.title, 80, (self.width // 3.4, self.height // 8))
        
        pygame.display.flip()  # Atualiza a tela
        return buttons



    def handle_menu_events(self, buttons):
          # Atualiza a posição do mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for index, (_, rect) in enumerate(buttons):
                    if rect.collidepoint(mouse_pos):
                        self.selected_option = index
                        print(f"Retângulo do botão: {rect}, Posição do mouse: {mouse_pos}")
                        print(f"Clique detectado em: {mouse_pos}, Botão: {index}")
                        return self.handle_menu_selection()
            
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

    
    def handle_menu_selection(self):
        login = Login()

        if self.menu_type == "main":
            if self.selected_option == 0:  # New Game
                self.menu_type ="new_game"# IMPLEMENTAR LOGICA DE CRIAR CONTA 
            elif self.selected_option == 1:  # Login
                self.menu_type = "login" #RETORNAR JOGO SALVO
            elif self.selected_option == 2:  # Quit game
                pygame.quit()
                exit()

        elif self.menu_type == "new_game": 

            if self.selected_option == 1:  # Voltar para o menu principal
                self.menu_type = "main"
            
            else:
                login.cadastrar(self.user_text, self.password_text)
                return 1
                
        elif self.menu_type == "login":
            
            if self.selected_option == 1:  # Voltar para o menu principal
                self.menu_type = "main"
            
            else:
                
                if login.verify_login(self.user_text, self.password_text):
                    return 1
                else:
                    self.menu_type = "login"
        """
        elif self.menu_type == "magias":
            if self.selected_option == 3:  # Voltar para o menu principal
                self.menu_type = "main"
            else: #IMPLEMENTAR A LOGICA DE ESCOLHA DAS MAGIAS AQUI
                if self.selected_option==0:
                    return 1
                elif self.selected_option==1:
                    return 1
                elif self.selected_option==2:
                    return 1
                
        return None
        """


    


    def draw_imput(self):

        # Desenhar as caixas de entrada
        pygame.draw.rect(self.screen, BLUE if self.active_input == "user" else BLACK, self.user_rect, 2)
        pygame.draw.rect(self.screen, BLUE if self.active_input == "password" else BLACK, self.password_rect, 2)

        # Renderizar texto
        user_surface = self.font.render(self.user_text, True, BLACK)
        password_surface = self.font.render("*" * len(self.password_text), True, BLACK)

        # Blitar texto nas caixas
        self.screen.blit(user_surface, (self.user_rect.x + 5, self.user_rect.y + 5))
        self.screen.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))

        # Mostrar os títulos
        self.screen.blit(self.font.render("Usuário:", True, BLACK), (200, 200))
        self.screen.blit(self.font.render("Senha:", True, BLACK), (200, 300))


    