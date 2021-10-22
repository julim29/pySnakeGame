import pygame
import pygame_gui
from EventHandler import EventHandler
from abc import ABC, abstractmethod


class GUI:
    pass


class State(ABC):
    class Quit(Exception):
        pass

    userInterface: GUI

    @abstractmethod
    def run(self):
        pass


class GUI:
    currentWindow: State

    def __init__(self):
        pass

    def changeWindow(self, state: State):
        self.state = state


class SimpleMenuState:
    options: list
    userInterface: GUI

    def __init__(self, userInterface: GUI):
        self.userInterface = userInterface
        self.optionNames = []
        self.states = []
        self.size = (200, 200)
        self._buttonSize = (40, 10)
        self.color = '#000000'

    def addOption(self, optionName: str, nextState: State):
        self.optionNames.append(optionName)
        self.states.append(nextState)

    def setSize(self, size):
        self.size = size

    def setColor(self, color):
        self.color = color

    def setButtonsDimension(self, buttonSize: tuple):
        self._buttonSize = buttonSize

    def _initMenu(self):
        self._windowSurface = pygame.display.set_mode(self.size)
        self._background = pygame.Surface(self.size)
        self._background.fill(pygame.Color(self.color))

        self._manager = pygame_gui.UIManager(self.size)

        self._clock = pygame.time.Clock()

        self._buttons = []

        self._eventHandler = EventHandler()

        x, y = self.size

        for index, buttonName in enumerate(self.optionNames):
            self._buttons += [
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x//2 - self._buttonSize[0]//2, (y*index+y//2)//len(self.optionNames)- self._buttonSize[1]//2), self._buttonSize),
                                             text=buttonName,
                                             manager=self._manager)]

        for button, state in zip(self._buttons, self.states):
            self._eventHandler.addEvent(button, self.userInterface.changeWindow, (state, ))

    def _updateMenu(self):
        stop = False

        time_delta = self._clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise State.Quit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    self._eventHandler.postEvent(event.ui_element)
                    stop = True

            self._manager.process_events(event)

        self._manager.update(time_delta)

        return stop

    def _render(self):
        self._windowSurface.blit(self._background, (0, 0))
        self._manager.draw_ui(self._windowSurface)
        pygame.display.update()

    def run(self):
        self._initMenu()

        stop = False
        while not stop:
            stop = self._updateMenu()
            self._render()
