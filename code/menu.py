import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.selected_option = -1  # Nenhuma opção selecionada inicialmente
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.menu_type = "main"
        self.button_size = (400, 70)  # Largura e altura dos botões
        self.spacing = 20  # Espaço entre os botões
        self.start_y = 50  # Deslocamento do topo da tela

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
            title = "MageSurvivor"
            button_texts = ["New Game", "Login", "Exit"]
        elif self.menu_type == "login":
            title = "Insira seu login e senha:"
            button_texts = ["Confirm", "Back"]
        elif self.menu_type == "magias":
            title = "Escolha sua magia:"
            button_texts = ["Magia de fogo", "Magia de gelo", "Magia de raio", "Back"]
        
        buttons = self.create_buttons(button_texts)
        self.draw_buttons(buttons)
        self.display(title, 80, (self.width // 3.4, self.height // 4))
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
        return None

    def handle_menu_selection(self):
        if self.menu_type == "main":
            if self.selected_option == 0:  # New Game
                self.menu_type ="login"# IMPLEMENTAR LOGICA DE CRIAR CONTA 
            elif self.selected_option == 1:  # Login
                self.menu_type = "login" #RETORNAR JOGO SALVO
            elif self.selected_option == 2:  # Quit game
                pygame.quit()
                exit()
        
        elif self.menu_type == "login": #IMPLEMENTAR LOGICA DE CRIAR LOGIN E DE RECUPERAR JOGO SALVO
            if self.selected_option == 1:  # Voltar para o menu principal
                self.menu_type = "main"
            else:
                self.menu_type = "magias"

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