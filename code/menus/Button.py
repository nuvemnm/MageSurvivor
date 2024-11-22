import pygame

# Definição de cores
WHITE = (255, 255, 255)  # Cor do texto
BLACK = (0, 0, 0)  # Cor padrão do botão
GRAY = (200, 200, 200)  # Cor alternativa
HOVER_COLOR = (100, 100, 100)  # Cor do botão ao passar o mouse

class Button:
    def __init__(self, text: str, rect: pygame.Rect, option: str):
        """
        Inicializa o botão com texto, posição e uma opção associada.
        """
        self.text = text  # Texto exibido no botão
        self.rect = rect  # Retângulo que define o tamanho e posição
        self.font = pygame.font.Font(None, 74)  # Fonte do texto
        self.option = option  # Opção associada ao botão
        self.color = BLACK  # Cor inicial do botão  

    def draw(self, screen):
        """
        Desenha o botão na tela, alterando a cor se o mouse estiver sobre ele.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtém a posição atual do mouse
        if self.rect.collidepoint(mouse_x, mouse_y):  # Verifica se o mouse está sobre o botão
            self.color = HOVER_COLOR  # Muda para a cor de "hover"
        else:
            self.color = BLACK  # Mantém a cor padrão

        pygame.draw.rect(screen, self.color, self.rect)  # Desenha o retângulo do botão
        label = self.font.render(self.text, True, WHITE)  # Renderiza o texto do botão
        label_rect = label.get_rect(center=self.rect.center)  # Centraliza o texto no botão
        screen.blit(label, label_rect)  # Desenha o texto na tela 

    def click(self):
        """
        Retorna a opção associada ao botão.
        """
        return self.option
