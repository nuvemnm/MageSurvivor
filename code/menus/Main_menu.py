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
        
        

    def display_menu(self, jogo):
        selected_option = super().display_menu(self.title,self.button_infos)

        if selected_option == self.options.confirm:
            if self.login.verify_login(self.user_text, self.password_text):
                
                jogo.active_state = "running"
                #return self.active_state
          
            else: 
                jogo.active_state = "main_menu"
                #return self.active_state

        elif selected_option == self.options.new_game:
            jogo.active_state = "register_menu"
            #return self.active_state


        elif selected_option == self.options.exit:
            pygame.quit()
            exit()

        else:
            jogo.active_state = "main_menu"
            #return self.active_state

    def reset(self, jogo):
        jogo.player.alive = True
        jogo.player.score = 0
        jogo.player.actual_level = 1
        jogo.player.speed = 300
        jogo.player.staticLife = 50
        jogo.player.dinamicLife = jogo.player.staticLife
        jogo.player.rect = jogo.player.right_image.get_rect(topleft = jogo.map.player_spawn_position)
        jogo.player.experience = 0
        jogo.player.experience_threshold = 1
        
        jogo.actual_time = 0
        jogo.elapsed_time = 0
        #jogo.init_time = 0
        for enemy in jogo.enemy_sprites:
            enemy.kill()
