import newGame
import game
import pickle
import newGame
import os
import sys

def safeInput(desired):
    while True:
        try:
            answer = int(input())
            assert answer in desired
            return answer
        except Exception as e:
            print('Invalid input!')

def windowDim():
    rows, columns = os.popen('stty size', 'r').read().split()
    return rows, columns

def printDash():
    rows, columns = windowDim()
    for i in range(0,int(columns)):
        sys.stdout.write('-')
    print()

def loadGame():
    try:
        save = open('save', 'rb')
        saveFile = pickle.load(save)
        player = saveFile.player
        world = saveFile.world
        return player, world
    except:
        print('Load Error')

def mainMenu():
    #-- find source for this
    os.system('cls' if os.name == 'nt' else 'clear')
    
    rows, columns = windowDim()
    printDash()
    printDash()
    print('')
    print('')
    print('ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
    print('o                                                                                                         o')
    print('o    ooooooo   o       o  ooooooooo  oooooooo   ooooooooo  o       o  oooooooo    ooooooo   o         o   o')
    print('o   o       o  o       o  o          o       o      o      o       o  o       o  o       o  o         o   o')
    print('o   o       o  o       o  o          o       o      o      o       o  o       o  o       o  o         o   o')
    print('o   o       o   o     o   ooooooo    oooooooo       o      ooooooooo  oooooooo   o       o  o         o   o')
    print('o   o       o    o   o    o          o     o        o      o       o  o     o    o       o   o   o   o    o')
    print('o   o       o     o o     o          o      o       o      o       o  o      o   o       o    o o o o     o')
    print('o    ooooooo       o      ooooooooo  o       o      o      o       o  o       o   ooooooo      o   o      o')
    print('o                                                                                                         o')
    print('ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
    print('')
    print('')
    sys.stdout.write("What would you like to do?\n")
    sys.stdout.write("1: Load Game \n")
    sys.stdout.write("2: New Game\n")
    sys.stdout.write("3: Exit Game\n")

    while True:
        choice = safeInput([1,2,3])
        if choice == 1:
            print('Loading Game...\n')
            user, world = loadGame()
            #-- add a way to check to see is the load file exists
            game.gameLoop(user, world)
        elif choice == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Creating New Game...\n')
            print('')
            sys.stdout.write("Ever since the king died without appointing an heir, the kindom has fallen to shambles. A mysterious unnamed ")
            sys.stdout.write("tyrant has risen to power, proclaiming themselves as the rightful heir, ruling over the kingdom with absolute power. Followers ")
            sys.stdout.write("of the new tyrant roam the streets freely stealing from the poor. The armies and the nobles are praised by the ")
            sys.stdout.write("new ruler, getting over-the-top special treatment while the peasants are hungrier now than ever before, being ")
            sys.stdout.write("put to work for little compensation. In the rich districts, you can hear music, dancing, and laughter ")
            sys.stdout.write("throughout the night. Everywhere else there is silence. \n\n")
            sys.stdout.write("You wake up every morning clutching your weapon to your chest. A former spy under the reign of the deceased king, you ")
            sys.stdout.write("have seen many different kings and queens rule over different kingdoms. As someone who stood by the dead king ")
            sys.stdout.write("for years, you have a sense of pride and loyalty towards him despite him being gone for almost a year now. ")
            sys.stdout.write("As one of the high-ranking members of the former kings court who didn't accept bribes from the new ruler, ")
            sys.stdout.write("you have a target on your back, as you sense you are constantly being watched. One day, you come home to see that ")
            sys.stdout.write("your door was broken, and a trail of dirt and mud covered your floor. Your gold was stolen, your belongings tampered with ")
            sys.stdout.write("and letters you had received from the previous king were all thrown in the fire. You become enraged and finally decide that ")
            sys.stdout.write("enough is enough and you set out to take for the mysterious tyrant once and for all... \n\n")

            input('Press any key to continue')
            user, world = newGame.newGame()
            game.gameLoop(user, world)
        elif choice == 3:
            quit()

    printDash()
    printDash()


if __name__ == '__main__':
    mainMenu()