import pygame
from menus.Menu import Menu
from menus.Menu import COLORS
from menus.options import Options


class Pause_menu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        self.options = Options()
        self.title = "Pause"
        self.button_infos = {"Continuar":self.options.continuar, "Exit":self.options.exit}
        

    def display_menu(self):   
        self.screen.fill(COLORS["GRAY"])  # Limpa a tela para evitar sobreposição
        
        self.create_buttons(button_infos = self.button_infos)
        self.display_text(self.title, 80, (self.width // 3.4, self.height // 38))
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
    

    def pause(self):

        selected_option = self.display_menu()
        
        if selected_option == self.options.continuar:
            return  True
            
         

        elif selected_option == self.options.exit:
            return False