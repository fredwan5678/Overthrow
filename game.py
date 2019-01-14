import menu
import os
import newGame
import random
import copy
import sys
import AI

'''
Todo:
    Fix menu indexing(m) --done
    abstract scaling
    beating the game(m) --done
    AI

Done:
    Highlighted items in inventory that are equipped
    changed battle layout - red/green, added total energy and energy needed for class attacks
    added item levels to all menus (except gifts)
    added costs to each item in shop inventory - yellow to see easier
    auto-equip option when purchasing items (can add it to gifts too if wanted)
    HUD now shows attribute boosts from items in brackets
    when looking at inventory and shop items stats are compared so user doesn't go back and forth between currently equipped and new item
    indexing is fixed - added a statement when nobody is left in town
    added a statement when only able to travel to 1 town
    added game title when game is opened
    added text when user opens a new game - backstory
    added text when user kills final boss (hardcoded atm - couldn't import mapSize)

My version doesn't have some of the balance changes that you put in yours, and I dont have the thing fixed where you couldn't travel to 
the next level in a really narrow world. But a lot of functions across all the files were changed, so be careful when implementing some 
of the stuff you have. 

I did a full playthrough with rogue, and BARELY killed the final boss. I needed fully maxed gear and had to use abilities at optimal times
so he shouldn't need much of a balance even though the midgame was easy


'''

def battle(enemy, player):
    '''
    The battling loop, where the characters fight untill one dies. All the data is held in the
    battlefield object. Returns when the battle is concluded.

    Arguments:
        enemy: The enemy NPC object
        player: The player object

    Returns
    '''
    fight = battleground(enemy, player)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(enemy.name, 'starts a fight!')
    input()

    chance = (player.cleaverness/(player.cleaverness+enemy.cleaverness))
    if (random.uniform(0, 1) < chance):
        fight.playerTurn()
        if not fight.conclusion():
            return True


    while(True):
        tickOut = fight.tick(0)
        if tickOut == 'next':
            fight.enemyTurn()
            if not fight.conclusion():
                return True
        elif tickOut == 'end':
            return True
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            input('STUNNED!')
        tickOut = fight.tick(1)
        if tickOut == 'next':
            fight.playerTurn()
            if not fight.conclusion():
                return True
        elif tickOut == 'end':
            return True
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            input('STUNNED!')

class battleground():
    '''
    The data structure where all the fighers and their combat data is held.
    '''
    def __init__(self, enemy, player):
        self.originalPlayer = player
        self.originalEnemy = enemy
        self.player = copy.deepcopy(player)
        self.enemy = copy.deepcopy(enemy)

        self.playerDict = {
        'fighter':self.player,
        'defence':self.player.armour.defence,
        'cooldowns': {},
        'status': {}
        }

        self.enemyDict = {
        'fighter':self.enemy,
        'defence':self.enemy.armour.defence,
        'cooldowns': {},
        'status': {}
        }

        self.status = {
        'stun':['stun',2],
        'burn':['dot',3],
        'poison':['dot',1]
        }

        self.player.strength = self.player.strength + self.player.weapon.strength + self.player.armour.strength
        self.player.dexerity = self.player.dexerity + self.player.weapon.dexerity + self.player.armour.dexerity
        self.player.inteligence = self.player.inteligence + self.player.weapon.inteligence + self.player.armour.inteligence
        self.player.cleaverness = self.player.cleaverness + self.player.weapon.cleaverness + self.player.armour.cleaverness
        if self.player.charm:
            self.player.strength += self.player.charm.strength
            self.player.dexerity += self.player.charm.dexerity
            self.player.inteligence += self.player.charm.inteligence
            self.player.cleaverness += self.player.charm.cleaverness

        self.enemy.strength = self.enemy.strength + self.enemy.weapon.strength + self.enemy.armour.strength
        self.enemy.dexerity = self.enemy.dexerity + self.enemy.weapon.dexerity + self.enemy.armour.dexerity
        self.enemy.inteligence = self.enemy.inteligence + self.enemy.weapon.inteligence + self.enemy.armour.inteligence
        self.enemy.cleaverness = self.enemy.cleaverness + self.enemy.weapon.cleaverness + self.enemy.armour.cleaverness


    def playerTurn(self):
        '''
        Gives options to the player and carries out their move
        '''
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\033[0;32m')
        print('It is your turn!\n\n')
        print('Player:')
        print('HP: ' + str(self.player.HP) + '/' + str(self.player.maxHP))
        print('Energy:', str(self.player.energy) + '/' + str(self.originalPlayer.energy))
        print('Weapon:', self.player.weapon.name)
        print('Armour:', self.player.armour.name)
        if (self.player.charm):
            print('Charm:', self.player.charm.name)
        print('Defence:', self.playerDict['defence'])
        print('Str:', self.player.strength)
        print('Dex:',self.player.dexerity)
        print('Int:',self.player.inteligence)
        print('Clv:',self.player.cleaverness, '\n\n')
        print('\033[0;m')

        print('\033[0;31m')
        print('Enemy:')
        print('HP: ' + str(self.enemy.HP) + '/' + str(self.enemy.maxHP))
        print('Energy:', str(self.enemy.energy) + '/' + str(self.originalEnemy.energy))
        print('Weapon:', self.enemy.weapon.name)
        print('Armour:', self.enemy.armour.name)
        print('Defence:', self.enemyDict['defence'])
        print('Str:',self.enemy.strength)
        print('Dex:',self.enemy.dexerity)
        print('Int:',self.enemy.inteligence)
        print('Clv:',self.enemy.cleaverness)
        print('\033[0;m')
        print()

        options = []

        print('(1) strike')
        options.append(1)

        for a in range(len(self.playerDict['fighter'].Class.abilities)):
            if ((self.player.Class.abilities[a] not in self.playerDict['cooldowns'] or self.playerDict['cooldowns'][self.player.Class.abilities[a]] <= 0) and self.player.energy >= self.player.Class.costs[a]):
                print('(%d) %s - (%d energy)' % ((a+2), self.player.Class.abilities[a], self.player.Class.costs[a]))
                options.append(a+2)

        choice = menu.safeInput(options)
        
        if choice == 1:
            damage = self.player.weapon.damage//4+self.player.strength//4 - self.enemyDict['defence']
        elif choice == 2:
            damage = self.player.Class.ability1(self.playerDict, self.enemyDict)
        elif choice == 3:
            damage = self.player.Class.ability2(self.playerDict, self.enemyDict)

        if (damage > 1):
            self.enemy.HP -= damage
            print('You did', damage,'damage!')
        else:
            self.enemy.HP -= 2
            print('You did 2 damage!')

        input()


    def enemyTurn(self):
        '''
        Takes input from the AI and carries out it's move
        '''
        os.system('cls' if os.name == 'nt' else 'clear')
        print("It is the enemy's turn!")

        options = []

        options.append(1)

        for a in range(len(self.enemyDict['fighter'].Class.abilities)):
            if ((self.enemy.Class.abilities[a] not in self.enemyDict['cooldowns'] or self.enemyDict['cooldowns'][self.enemy.Class.abilities[a]] <= 0) and self.enemy.energy >= self.enemy.Class.costs[a]):
                options.append(a+2)

        choice = AI.AI(self, options) #replace with "AI"
        
        if choice == 1:
            damage = self.enemy.weapon.damage//4+self.enemy.strength//4 - self.enemyDict['defence']
        elif choice == 2:
            damage = self.enemy.Class.ability1(self.enemyDict, self.playerDict)
        elif choice == 3:
            damage = self.enemy.Class.ability2(self.enemyDict, self.playerDict)

        if (damage > 0):
            self.player.HP -= damage
            print('The enemy did', damage,'damage!')
        else:
            self.player.HP -= 2
            print('The enemy did 2 damage!')

        input()


    def tick(self, turn):
        '''
        Carries out any processes that happen between moves

        Arguments:
            turn: A 1 or 0 depending on whe's turn it last was. 0 means enemy, and vice versa.

        returns:
            None
        '''
        if turn:
            fighter = self.playerDict
        else:
            fighter = self.enemyDict

        stun = False

        for cooldown in fighter['cooldowns'].keys():
            if fighter['cooldowns'][cooldown] != 0:
                fighter['cooldowns'][cooldown] -= 1


        for effect in fighter['status'].keys():
            if self.status[effect][0] == 'stun' and fighter['status'][effect] > 0:
                stun = True
            elif self.status[effect][0] == 'dot' and fighter['status'][effect] > 0:
                fighter['fighter'].HP -= self.status[effect][1]
                print('The target takes damage from status effects...')

            fighter['status'][effect] -= 1

        if not self.conclusion():
            return 'end'
        elif stun:
            return False
        else:
            return 'next'

    def conclusion(self):
        '''
        Concludes the battle if someone dies. If The player dies, the game closes.
        If the enemy dies, rewards are given to the player and the fight ends.
        Returns False on battle conclution and true on battle continuation.
        '''
        if self.playerDict['fighter'].HP <= 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            input('You died!\n Please restart from your last save point...')
            quit()

        if self.enemyDict['fighter'].HP <= 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('YOU WIN!')
            self.originalEnemy.HP = 0
            self.originalPlayer.gold += self.originalEnemy.goldReward
            print('You got', self.originalEnemy.goldReward, 'gold!')
            self.originalPlayer.xp += self.originalEnemy.xpReward
            print('You gained', self.originalEnemy.xpReward, 'experience!')
            input()
            while (self.originalPlayer.xp >= self.originalPlayer.xpDenominator):
                self.originalPlayer.level += 1
                self.originalPlayer.xp -= self.originalPlayer.xpDenominator
                self.originalPlayer.xpDenominator += 10*self.originalPlayer.level #temp
                print('You leveled up!')
                self.originalPlayer.HP += self.originalPlayer.Class.HPUp
                self.originalPlayer.maxHP += self.originalPlayer.Class.HPUp
                print('HP increased by', self.originalPlayer.Class.HPUp)
                self.originalPlayer.energy += self.originalPlayer.Class.energyUp
                print('Energy increased by', self.originalPlayer.Class.energyUp)
                self.originalPlayer.strength += self.originalPlayer.Class.strUp
                print('Strength increased by', self.originalPlayer.Class.strUp)
                self.originalPlayer.dexerity += self.originalPlayer.Class.dexUp
                print('Dexterity increased by', self.originalPlayer.Class.dexUp)
                self.originalPlayer.inteligence += self.originalPlayer.Class.intelUp
                print('Intelligence increased by', self.originalPlayer.Class.intelUp)
                self.originalPlayer.cleaverness += self.originalPlayer.Class.clevUp
                print('Cleaverness increased by', self.originalPlayer.Class.clevUp)
                input()
            return False

        return True

def hud(player):
    os.system('cls' if os.name == 'nt' else 'clear')
    # gets the width of the console to properly display right-justified words
    rows, columns = menu.windowDim()
    # displays dashes to make HUD clearly visible
    menu.printDash()

    # need sys.stdout to format the text properly
    # \033[1;33m ... \033[1;m turns encompassed text into different color
    # defines text colors
    green = ['','']
    green[0] = '\033[0;32m'
    green[1] = '\033[0;m'
    red = ['','']
    red[0] = '\033[0;31m'
    red[1] = '\033[0;m'
    stuff = ['','']
    stuff[0] = '\033[0;46;35m'
    stuff[1] = '\033[0;m'
    # text and background
    goldOnGreen = ['','']
    goldOnGreen[0] = '\033[0;42;33m'
    goldOnGreen[1] = '\033[0;m'

    # can be easily changed to one of the above text color options
    color = green

    # used if player doesn't have a charm (like at beginning of game)
    if not player.charm:
        charmStr = 0
        charmDex = 0
        charmInt = 0
        charmClv = 0
    else:
        charmStr = player.charm.strength
        charmDex = player.charm.dexerity
        charmInt = player.charm.inteligence
        charmClv = player.charm.cleaverness

    # used to display all players' item stats on hud aling with base stats
    itemStr = player.weapon.strength + player.armour.strength + charmStr
    itemDex = player.weapon.dexerity + player.armour.dexerity + charmDex
    itemInt = player.weapon.inteligence + player.armour.inteligence + charmInt
    itemClv = player.weapon.cleaverness + player.armour.cleaverness + charmClv

    sys.stdout.write(color[0])
    sys.stdout.write(('Current Town: %s' % (player.town.name).ljust(0)))
    sys.stdout.write(('HP: %d/%d\n' % (player.HP, player.maxHP)).rjust((int(columns) - len(player.town.name) -13)))
    sys.stdout.write(('XP: %d/%d\n' % (player.xp, player.xpDenominator)).rjust((int(columns) + 1)))
    sys.stdout.write(('Level: %d' % (player.level)))
    sys.stdout.write(('Gold: %d\n' % (player.gold)).rjust(int(columns) - 6 - len(str(player.level))))
    sys.stdout.write(('Class: %s' % (player.Class.name)))
    sys.stdout.write(('Strength: %d (+%d)\n' % (player.strength, itemStr)).rjust(int(columns) - len(player.Class.name) - 6))
    sys.stdout.write(('Weapon: %s (lvl: %d)' % (player.weapon.name, player.weapon.level))) #-- fix this
    sys.stdout.write(('Dexterity: %d (+%d)\n' % (player.dexerity, itemDex)).rjust(int(columns) - 15 - len(player.weapon.name) - len(str(player.weapon.level))))
    sys.stdout.write(('Armour: %s (lvl: %d)') % (player.armour.name, player.armour.level)) #-- fix this
    sys.stdout.write(('Intelligence: %d (+%d)\n' % (player.inteligence, itemInt)).rjust(int(columns) - 15 - len(player.armour.name) - len(str(player.armour.level))))
    if player.charm:
        sys.stdout.write(('Charm: %s (lvl: %d)') % (player.charm.name, player.charm.level))
        sys.stdout.write(('Cleverness: %d (+%d)\n\n' % (player.cleaverness, itemClv)).rjust(int(columns) - 13 - len(player.charm.name) - len(str(player.charm.level))))
    else: 
        sys.stdout.write(('Charm: None'))
        sys.stdout.write(('Cleverness: %d (+%d)\n\n' % (player.cleaverness, itemClv)).rjust(int(columns) - 9))

    sys.stdout.write(color[1])
    sys.stdout.flush()

def gameLoop(player, world):
    '''
    The main game loop. Displays the overworld menu for the game. 
    Runs forever till the player chooses to exit the game.

    Arguments:
        player: The player object
        World: The world object

    Returns:
        None
    '''

    while(True):
        hud(player)

        print()
        print('Select one of the following options')
        print('1: Open Inventory')
        print('2: Open Map')
        print('3: Explore Current Town')
        print('4: Travel to a New Town')
        print('5: Save Game')
        print('6: Exit The Game')

        choice = menu.safeInput([1,2,3,4,5,6])
        if choice == 1:
            inventory(player)#done
        elif choice == 2:
            map(player, world)
        elif choice == 3:
            explore(player, player.town)
        elif choice == 4:
            travel(player, world)
        elif choice == 5:
            newGame.saver(player, world)#done
        elif choice == 6:
            print('Exiting game...')#done
            quit()

def map(player, world):
    '''
    Generate a map of the world

    Arguments:
        World: The world object
        Player: The player object

    Returns:
        None
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    hud(player)

    print('Generating...')

    #https://stackoverflow.com/questions/13067615/python-getting-the-max-value-of-y-from-a-list-of-objects
    maxY = max(town.y for town in world.towns)
    minY = min(town.y for town in world.towns)
    maxX = max(town.x for town in world.towns)

    grid = [[0 for x in range(maxX+2)] for y in range(minY, maxY+2)]

    for town in world.towns:
        grid[town.y][town.x] = town

    os.system('cls' if os.name == 'nt' else 'clear')

    for row in range(maxY, minY-2, -1):
        for col in range(maxX+2):
            if grid[row][col] and player.town.x == col and player.town.y == row:
                print('P ', end='')
            elif grid[row][col]:
                print('T ', end='')
            #Axis
            elif col == maxX+1 and row == minY-1:
                pass
            elif col == maxX+1:
                if row < 0:
                    print(row, end='')
                else:
                    print(' '+str(row), end='')
            elif row == minY-1:
                print(str(col)+' ', end='')
            else:
                print('  ', end='')
        print()

    input('Press enter to go back')

def inventory(player):
    '''
    Displays the player's inventory and allows the player to interact with their items.

    Arguments:
        player: The player object

    Returns:
        None
    '''
    while(True):
        os.system('cls' if os.name == 'nt' else 'clear')
        hud(player)
        green = ['','']
        green[0] = '\033[0;32m'
        green[1] = '\033[0;m'
        blue = ['','']
        blue[0] = '\033[0;34m'
        blue[1] = '\033[0;m'
        color = blue

        # changes the color of the equipped items from the default to blue
        print('INVENTORY: (All equipped items are shown in blue)')
        for item in range(len(player.inventory)):
            if player.inventory[item] == player.weapon:
                sys.stdout.write(color[0])
                print('(' + str(item+1) + ') ' + str(player.inventory[item].name) + ' (level: ' + str(player.inventory[item].level) + ')')
                sys.stdout.write(color[1])
            elif player.inventory[item] == player.armour:
                sys.stdout.write(color[0])
                print('(' + str(item+1) + ') ' + str(player.inventory[item].name) + ' (level: ' + str(player.inventory[item].level) + ')')
                sys.stdout.write(color[1])
            elif player.inventory[item] == player.Class: 
                sys.stdout.write(color[0])
                print('(' + str(item+1) + ') ' + str(player.inventory[item].name))
                sys.stdout.write(color[1])
            elif player.inventory[item] == player.charm: 
                sys.stdout.write(color[0])
                print('(' + str(item+1) + ') ' + str(player.inventory[item].name) + ' (level: ' + str(player.inventory[item].level) + ')')
                sys.stdout.write(color[1])
            elif player.inventory[item].thing == 'weapon': 
                print('(' + str(item+1) + ') ' + str(player.inventory[item].name) + ' (level: ' + str(player.inventory[item].level) + ')')
            elif player.inventory[item].thing == 'armour':
                print('(' + str(item+1) + ') ' + str(player.inventory[item].name) + ' (level: ' + str(player.inventory[item].level) + ')')
            elif player.inventory[item].thing == 'charm':
                print('(' + str(item+1) + ') ' + str(player.inventory[item].name) + ' (level: ' + str(player.inventory[item].level) + ')')
            else:
                print('(' + str(item+1) + ')', player.inventory[item].name)
        print('(0) Back')

        choice = menu.safeInput( range(len(player.inventory)+1) )

        # gives user  choice to equip a certain item, comparing the stats with the currently equipped item
        if choice == 0:
            return
        else:
            item = player.inventory[choice-1]

            os.system('cls' if os.name == 'nt' else 'clear')
            print(item.name)
            if (item.thing != 'class'):
                if (item.thing == 'weapon'):
                    print('Damage: %d (%d)' % (item.damage, item.damage - player.weapon.damage))
                    print('Strength: %d (%d)' % (item.strength, item.strength - player.weapon.strength))
                    print('Dexterity: %d (%d)' % (item.dexerity, item.dexerity - player.weapon.dexerity))
                    print('Intelligence: %d (%d)' % (item.inteligence, item.inteligence - player.weapon.inteligence))
                    print('Cleverness: %d (%d)' % (item.cleaverness, item.cleaverness - player.weapon.cleaverness))
                if (item.thing == 'armour'):
                    print('Defence: %d (%d)' % (item.defence, item.defence - player.armour.defence))
                    print('Strength: %d (%d)' % (item.strength, item.strength - player.armour.strength))
                    print('Dexterity: %d (%d)' % (item.dexerity, item.dexerity - player.armour.dexerity))
                    print('Intelligence: %d (%d)' % (item.inteligence, item.inteligence - player.armour.inteligence))
                    print('Cleverness: %d (%d)' % (item.cleaverness, item.cleaverness - player.armour.cleaverness))
                if (item.thing == 'charm'):
                    if player.charm:
                        print('Strength: %d (%d)' % (item.strength, item.strength - player.charm.strength))
                        print('Dexterity: %d (%d)' % (item.dexerity, item.dexerity - player.charm.dexerity))
                        print('Intelligence: %d (%d)' % (item.inteligence, item.inteligence - player.charm.inteligence))
                        print('Cleverness: %d (%d)' % (item.cleaverness, item.cleaverness - player.charm.cleaverness))
                    else:
                        print('Strength: %d (%d)' % (item.strength, item.strength))
                        print('Dexterity: %d (%d)' % (item.dexerity, item.dexerity))
                        print('Intelligence: %d (%d)' % (item.inteligence, item.inteligence))
                        print('Cleverness: %d (%d)' % (item.cleaverness, item.cleaverness))
            print()
            print('(1) Equip')
            print('(0) Back')

            choice = menu.safeInput(range(2))
            if choice == 0:
                pass
            else:
                if item.thing == 'weapon':
                    player.weapon = item
                if item.thing == 'armour':
                    player.armour = item
                if item.thing == 'charm':
                    player.charm = item
                if item.thing == 'class':
                    player.Class = item
                print(item.name, 'was equipped!')
                input()


def explore(player, town):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        hud(player)

        NPCList = player.town.NPCs
        #going to be from game instead of menu
        print('List of people in the town of %s:' % (player.town.name))
        print('0: Exit')
        for i in range(len(player.town.NPCs)):
            print('%d: ' % (i + 1) + player.town.NPCs[i].name)
        if len(player.town.NPCs) == 0:
            print('\n%s Looks deserted, press 0 to exit.' % (player.town.name))
        elif len(player.town.NPCs) == 1:
            print('Choose a person to interact with (1): ')
        else:
            print('Choose a person to interact with (Enter a number between 1 - %d): ' % (len(player.town.NPCs)))
        choice = menu.safeInput(range(len(player.town.NPCs) + 1))
        if choice == 0:
            return
        else:
            print(player.town.NPCs[choice - 1].name)
            NPCList[choice - 1].interact(player, NPCList, choice - 1)

def travel(player, town):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        hud(player)
        print('List of towns you may travel to: ')
        print('0: Exit')
        for i in range(len(player.town.exits)):
            print('%d: ' % (i + 1) + player.town.exits[i].name, '('+str(player.town.exits[i].x)+','+str(player.town.exits[i].y)+')') #print level of town
        if len(player.town.exits) == 1:
            print('You may only travel to %s from %s (Enter 1 to travel or press 0 to exit):' % (player.town.name, player.town.exits[0].name))
        else:
            print('Choose a town to travel to (Enter a number between 1 - %d) or press 0 to exit: ' %(len(player.town.exits)))
        choice = menu.safeInput(range(len(player.town.exits) + 1))
        print(player.town.exits[choice - 1].name)

        if choice == 0:
            return
        elif ((player.town.exits[choice - 1].y) <= player.questLevel):
            player.town = player.town.exits[choice - 1]
            print("You have arrived in %s" % player.town.name)
            input()
            return
        else:
            print("You feel you are not strong enough to advance...")
            print('Try exploring more!')
            input()
            return