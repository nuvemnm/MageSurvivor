import pygame
from menus.Menu import Menu
from menus.Menu import COLORS
from menus.options import Options


class Main_menu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        self.options = Options()
        self.title = "MageSurvivor"
        self.button_infos = {"Confirm":self.options.confirm, "New Game":self.options.new_game, "Exit":self.options.exit}
        

    def display_menu(self):
        selected_option = super().display_menu(self.title,self.button_infos)

        if selected_option == self.options.confirm:
            if self.login.verify_login(self.user_text, self.password_text):
                self.current_state = "running"
                return self.current_state
            else: 
                self.current_state = "main_menu"
                return self.current_state
        
        elif selected_option == self.options.new_game:
            self.current_state = "register_menu"
            return self.current_state


        elif selected_option == self.options.exit:
            pygame.quit()
            exit()

        else:
            self.current_state = "main_menu"
            return self.current_state