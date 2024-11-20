import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Button:
    def __init__(self,text : str, rect : pygame.Rect, option : str):
        self.text = text
        self.rect = rect
        self.font = pygame.font.Font(None, 60)
        self.option = option

    def draw(self,screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        label = self.font.render(self.text, True, WHITE)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def click(self):
        return self.option