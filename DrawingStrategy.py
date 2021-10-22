import pygame
from typing import Tuple

class DrawingStrategy:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface

    def draw(self, point: Tuple[int, int]) -> None:
        pass

class ClassicStyle(DrawingStrategy):
    def __init__(self, *args):
        super().__init__(*args)
        self.sideLenght = 10

    def setSideLength(self, sideLenght):
        self.sideLenght = sideLenght

    def draw(self, point: Tuple[int, int]) -> None:
        WHITE = (255, 255, 255)

        x, y = point
        pygame.draw.rect(self.surface, WHITE, pygame.Rect(x*self.sideLenght, y*self.sideLenght, self.sideLenght, self.sideLenght), 2)