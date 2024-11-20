import pygame
from menus.Menu import Menu
from menus.options import Options

from menus.Menu import COLORS


class Upgrade_menu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = Options()
        self.menu_type = "upgrade"
        self.title = "Escolha uma melhoria"
        self.button_infos = {"+20 de vida":self.options.upgrade_life, "+10 de dano":self.options.upgrade_damage, "+0.5 de velocidade de ataque":self.options.attack_speed}

    def display_menu(self,jogo):

        selected_option = super().display_menu(self.title,self.button_infos)
        
        if selected_option == self.options.upgrade_life:
            jogo.player.upgrade("life")
            jogo.active_menu = None

        elif selected_option == self.options.upgrade_damage:
            jogo.player.upgrade("damage")
            jogo.active_menu = None