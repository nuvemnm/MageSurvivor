import pygame
from menu import Menu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class UpgradeMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.menu_type = "upgrade"
        self.title = "Escolha uma melhoria"
        button_texts = ["+20 de vida", "+10 de dano"]

        self.buttons = self.create_buttons(button_texts)

        self.active = True

    def display(self):
        self.screen.fill(GRAY)  # Limpa a tela para evitar sobreposição

        self.draw_buttons(self.buttons)
        super().display(self.title, 80, (self.width // 3.4, self.height // 4))
        pygame.display.flip()  # Atualiza a tela
    
    def handle_menu_events(self, buttons):
        """
        Lida com os eventos do menu e retorna o índice do botão clicado.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for index, (_, rect) in enumerate(buttons):
                    if rect.collidepoint(mouse_pos):
                        return index  # Retorna o índice do botão clicado

        return None  # Nenhuma ação foi realizada

            
    def input_player(self,player):   
        result = self.handle_menu_events(self.buttons) 

        if result is None:
            return False

        elif result == 0:
            player.upgrade("life")
            player.upgrading = False
            return True
        
        elif result == 1:
            player.upgrade("damage")
            player.upgrading = False
            return True
