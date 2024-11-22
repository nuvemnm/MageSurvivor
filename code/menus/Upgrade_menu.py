import pygame
from menus.Menu import Menu
from menus.options import Options

from menus.Menu import COLORS


class Upgrade_menu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = Options()
        self.title = "Escolha uma melhoria"
        self.button_infos = {"+10 de vida":self.options.upgrade_life, "+5 de dano":self.options.upgrade_damage, "+10 de velocidade":self.options.speed}

    def display_menu(self):   
        self.screen.fill(COLORS["GRAY"])  # Limpa a tela para evitar sobreposição 
        
        self.create_buttons(button_infos = self.button_infos)
        self.display_text(self.title, 80, (self.width // 6, self.height // 4))
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
    

    
    def upgrade_choice(self, jogo):

        selected_option = self.display_menu()
        
        if selected_option == self.options.upgrade_life:
            jogo.player.upgrade("life")
            
        elif selected_option == self.options.upgrade_damage:
            jogo.player.upgrade("damage")

        elif selected_option  == self.options.speed:
            jogo.player.upgrade("speed")
            
        
        