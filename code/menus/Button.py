import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (100, 100, 100)  # Cor quando o mouse está sobre o botão

class Button:
    def __init__(self, text: str, rect: pygame.Rect, option: str):
        self.text = text
        self.rect = rect
        self.font = pygame.font.Font(None, 74)
        self.option = option
        self.color = BLACK  # Cor inicial do botão

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtém a posição do mouse
        if self.rect.collidepoint(mouse_x, mouse_y):  # Verifica se o mouse está dentro do retângulo
            self.color = HOVER_COLOR  # Muda a cor para a cor de "hover"
        else:
            self.color = BLACK  # Retorna para a cor original

        pygame.draw.rect(screen, self.color, self.rect)  # Desenha o botão com a cor atual
        label = self.font.render(self.text, True, WHITE)  # Cria o texto
        label_rect = label.get_rect(center=self.rect.center)  # Centraliza o texto
        screen.blit(label, label_rect)  # Desenha o texto na tela

    def click(self):
        return self.option
