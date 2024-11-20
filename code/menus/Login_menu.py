import pygame
from menus.Menu import Menu
from menus.Menu import COLORS
from menus.options import Options


class Login_menu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = Options()
        self.title = "Insira seu login e senha:"
        self.button_infos = {"Confirm":self.options.confirm, "Back":self.options.back}

    def display_menu(self,active_menu):
        selected_option = super().display_menu(self.title,self.button_infos)

        if selected_option == self.options.back:
            jogo.active_menu = "main_menu"
        