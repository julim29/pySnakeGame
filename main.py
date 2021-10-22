from Game import Game
import pygame
import pygame_gui
from GUI import GUI, SimpleMenuState, State


def main():
    pygame.init()
    userInterface = GUI()
    mainMenu = SimpleMenuState(userInterface)
    userInterface.changeWindow(mainMenu)
    mainMenu.setSize((400, 400))
    mainMenu.setButtonsDimension((100, 50))

    game = Game(userInterface)
    game.setSize((400, 400))
    game.setTileLength(20)

    mainMenu.addOption('Start', game)
    mainMenu.addOption('Options', None)
    mainMenu.addOption('Exit', Game.Quit)

    game.setLoseWindow(mainMenu)

    try:
        while True:
            userInterface.state.run()
    except State.Quit:
        pass




if __name__ == "__main__":
    main()
