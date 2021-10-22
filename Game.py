import GameObjects
from Board import Board
import pygame
from DrawingStrategy import ClassicStyle
from common import Direction, keyMap
from EventHandler import EventHandler
from GUI import State, GUI


DEFAULT_SIZE = (200, 200)
DEFAULT_TILE_LENGTH = 20

class Game(State):
    class GameOver(Exception):
        pass

    class Quit(Exception):
        pass

    def __init__(self, userInterface: GUI):
        self.userInterface = userInterface
        self.size = DEFAULT_SIZE
        self.tileLength = DEFAULT_TILE_LENGTH

    def setSize(self, size):
        self.size = size

    def setTileLength(self, tileLength):
        self.tileLength = tileLength

    def setLoseWindow(self, state):
        self.loseState = state


    def _initGame(self):
        myBoard = Board(tuple([length//self.tileLength for length in self.size]))
        self.screen = pygame.display.set_mode(self.size)

        self.snake = GameObjects.Snake(myBoard)
        self.food = GameObjects.Food(myBoard)

        currentStyle = ClassicStyle(self.screen)
        currentStyle.setSideLength(self.tileLength)
        self.snake.headStyle = currentStyle
        self.snake.bodyStyle = currentStyle
        self.food.style = currentStyle

        self.directionHandler = GameObjects.DirectionManager(Direction.DOWN)
        self.eventHandler = EventHandler()

        for pygameKeyEvent in keyMap:
            self.eventHandler.addEvent(pygameKeyEvent, self.directionHandler.changeDirection, (keyMap[pygameKeyEvent],))


    def _update(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                raise Game.Quit()

            if event.type == pygame.KEYDOWN:
                self.eventHandler.postEvent(event.key)

        try:
            if self.snake.CollidesWith(self.food):
                self.food.eaten()
                self.snake.expand(self.directionHandler.popDirection())
            else:
                self.snake.move(self.directionHandler.popDirection())

        except IndexError:
            raise Game.GameOver("The Snake hit the wall, you lost.")

        if self.snake.intersectsItself():
            raise Game.GameOver("The Snake ate itself, you lost.")

    def _render(self):
        BLACK = (0, 0, 0)

        self.screen.fill(BLACK)
        self.snake.draw()
        self.food.draw()

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        fps = 10

        self._initGame()

        try:
            while True:
                self._update()
                self._render()

                clock.tick(fps)

        except Game.GameOver:
            self.userInterface.changeWindow(self.loseState)
