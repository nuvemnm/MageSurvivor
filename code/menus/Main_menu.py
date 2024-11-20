import pygame
from menus.Menu import Menu
from menus.Menu import COLORS
from menus.options import Options


class Main_menu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        self.options = Options()
        self.title = "MageSurvivor"
        self.button_infos = {"New Game":self.options.new_game, "Login":self.options.login, "Exit":self.options.exit}

    def display_menu(self,jogo):
        selected_option = super().display_menu(self.title,self.button_infos)
        
        if selected_option == self.options.new_game:
            jogo.running = True

        elif selected_option == self.options.login:
            jogo.active_menu = "login_menu"

        elif selected_option == self.options.exit:
            jogo.exit()