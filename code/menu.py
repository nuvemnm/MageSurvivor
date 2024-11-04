import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.options = ["New game", "Login", "Quit"]  # opções do menu 
        self.selected_option = -1  # Nenhuma opção selecionada inicialmente

    def display(self, text, size, position):  # função para as características do menu
        font = pygame.font.SysFont('Corbel', size)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.fill("blue")
        self.screen.blit(text_surface, position)

    def display_menu_options(self):
        while True:
            width = self.screen.get_width()
            height = self.screen.get_height()

           
            self.display("MageSurvivor", 120, (width // 4, height // 4))  # Título do texto

            mouse_x, mouse_y = pygame.mouse.get_pos()  # Posição do mouse

            for index, option in enumerate(self.options):
                text = self.font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(width // 2, height // 2 + index * 100))

                # Desenha um retângulo preenchido para todas as opções
                if text_rect.collidepoint(mouse_x, mouse_y):  # Se o mouse está sobre a opção
                    pygame.draw.rect(self.screen, (170, 170, 170), text_rect.inflate(20, 20))  # Retângulo vermelho
                    self.selected_option = index  # Atualiza a opção selecionada
                else:
                    pygame.draw.rect(self.screen, (100, 100, 100), text_rect.inflate(20, 20))  # Retângulo cinza

                # Blita o texto sobre o retângulo
                self.screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Se o mouse for clicado
                    if event.button == 1:  # Verifica se o botão esquerdo do mouse foi pressionado
                        if self.selected_option == 0:  # Jogar
                            return  # Sai do menu e inicia o jogo
                        elif self.selected_option == 1:  # Login
                            print("Login selected")  # Implementar ação para Login
                            pygame.quit()
                            exit()
                        elif self.selected_option == 2:  # Sair
                            pygame.quit()
                            exit()

            pygame.display.flip()  # Atualiza a tela
