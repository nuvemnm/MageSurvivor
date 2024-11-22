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
        self.create_buttons(button_infos = self.button_infos)
        self.display_text(self.title, 200, (self.width/3.5, self.height /5))
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
    

    def pause(self, jogo):
        while True:
            selected_option = self.display_menu()
            
            if selected_option == self.options.continuar:
                jogo.active_state = "running"
                break
                #return self.active_state

            elif selected_option == self.options.exit:
                jogo.active_state = "main_menu"
                break
                #return self.active_state