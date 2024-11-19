import pygame
from menu import Menu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class UpgradeMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.menu_type = "upgrade"

    def display_menu(self):
        self.screen.fill(GRAY)  # Limpa a tela para evitar sobreposição

        self.menu_type = "upgrade"
        title = "Escolha uma melhoria"
        button_texts = ["+20 de vida", "+10 de dano"]

        buttons = self.create_buttons(button_texts)
        self.draw_buttons(buttons)
        self.display(title, 80, (self.width // 3.4, self.height // 4))
        pygame.display.flip()  # Atualiza a tela
        return buttons
    
    def handle_menu_selection(self):
        if self.menu_type == "upgrade":
            if self.selected_option == 0: 
                return 0
            elif self.selected_option == 1: 
                return 1 
            
    def upgrade_menu(self,player):    
        self.display_menu()
        result = None
        while result is None:
            buttons = self.display_menu()
            result = self.handle_menu_events(buttons)
        if result == 0:
            player.upgrade("life")
            return
        
        elif result == 1:
            player.upgrade("damage")
            return 


        return True
