import pygame

class UpgradeMenu:
    def __init__(self, screen, options):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.selected_option = -1  # Nenhuma opção selecionada inicialmente
        self.options = options  # opções iniciais do menu
        self.menu_type = "main"  # Define o menu inicial como o principal

    def display(self, text, size, position):
        font = pygame.font.SysFont('Corbel', size)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def display_menu(self, options):
        width = self.screen.get_width()
        height = self.screen.get_height()

        if self.menu_type == "main":
            title = "MageSurvivor"
            self.options = options


        self.screen.fill("black")
        self.display(title, 80, (width // 3.4, height // 4))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for index, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2 + index * 100))

            # Destaca a opção em que o mouse está
            if text_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.screen, (170, 170, 170), text_rect.inflate(20, 20))
                self.selected_option = index
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), text_rect.inflate(20, 20))

            self.screen.blit(text, text_rect)

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
            if self.selected_option == 0: 
                return 0
            elif self.selected_option == 1: 
                return 1 


