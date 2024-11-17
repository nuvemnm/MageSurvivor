import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.selected_option = -1  # Nenhuma opção selecionada inicialmente
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.text_rect = None
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.menu_type = "main"  # Define o menu inicial como o principal

    def display(self, text, size, position):
        font = pygame.font.SysFont('Corbel', size)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def display_menu(self):

        if self.menu_type == "main":
            title = "MageSurvivor"
            self.options = ["New game", "Login", "Exit"]
        elif self.menu_type == "login":
            title = "Insira seu login e senha:"
            self.options = ["Confirm", "Back"]
        elif self.menu_type == "magias":
            title = "Escolha sua magia:"
            self.options = ["Magia de fogo", "Magia de gelo", "Magia de raio", "Back"]

        self.screen.fill("black")
        self.display(title, 80, (self.width // 3.4, self.height // 4))

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        for index, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            self.text_rect = text.get_rect(center=(self.width // 2, self.height // 2 + index * 100))

            # Destaca a opção em que o mouse está
            if self.text_rect.collidepoint(self.mouse_x, self.mouse_y):
                pygame.draw.rect(self.screen, (170, 170, 170), self.text_rect.inflate(20, 20))
                self.selected_option = index
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), self.text_rect.inflate(20, 20))

            self.screen.blit(text, self.text_rect)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.selected_option >= 0:  # Verifica se uma opção foi selecionada
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


