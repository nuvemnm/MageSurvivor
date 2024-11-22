import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (100, 100, 100)  # Cor quando o mouse está sobre o botão

class Button:
    def __init__(self, text: str, rect: pygame.Rect, option: str):
        """
        Inicializa o botão com texto, posição e uma opção associada.
        """
        self.text = text
        self.rect = rect
        self.font = pygame.font.Font(None, 74)
        self.option = option
        self.color = BLACK  

    def draw(self, screen):
        """
        Desenha o botão na tela, alterando a cor se o mouse estiver sobre ele.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.color = HOVER_COLOR  
        else:
            self.color = BLACK  

        pygame.draw.rect(screen, self.color, self.rect)  
        label = self.font.render(self.text, True, WHITE) 
        label_rect = label.get_rect(center = self.rect.center)  
        screen.blit(label, label_rect)  

    def click(self):
        """
        Retorna a opção associada ao botão.
        """
        return self.option
