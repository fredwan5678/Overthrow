'''
Generates all the objects needed for the game world and then pickles the objects as a save file
'''
import gameObj
from random import choice as rand
from random import randint
import pickle
import os
import sys
import game

class saveFile():
    '''
    The object that is saved in the save file. It contains the player and the world.
    '''
    def __init__(self, player, world):
        self.player =  player
        self.world = world


def townGen(children, level, y, x):
    '''
    Generates a town. And most importantly, it's NPCs.

    Town needs the following:
        Town size
        Mandatory NPCs
        Random NPCs

        These are all random
        Mandatory NPCs are added later
    '''
    #start with NPC generation
    townLevel = level
    #the different NPC types
    ntypes = ['shop','none','gift','battle']
    #The different types of items the merchants can have
    shopItems = ['weapon','armour','charm', 'class']
    #a list to be filled with NPCs
    NPCs = []

    minTownSize = 3
    maxTownSize = 10
    townSize = rand(range(minTownSize, maxTownSize+1))

    #generate random NPCs of amount equal to townsize
    for i in range(townSize):
        currentType = rand(ntypes)
        currentName = rand(gameObj.names)
        currentNPC = gameObj.NPCPrototype(currentType, currentName)

        #setup the NPCs depending on their type
        if currentType == 'shop':
            #set an invintory for the NPC and a size
            inventory = []
            inventorySize = townLevel*2
            #generate the item
            for i in range(inventorySize):
                newItem = gameObj.randomItem( townLevel, rand(range(len(shopItems))) )
                #generate new items till a unique one is made
                while newItem.name in [item.name for item in inventory]:
                    newItem = gameObj.randomItem( townLevel, rand(range(len(shopItems))) )
                inventory.append(newItem)
            currentNPC.initializeShop(inventory)

        elif currentType == 'none':
            currentNPC.initializeNone(rand(gameObj.quotes))

        elif currentType == 'gift':
            #create a gift object for the gift NPC to give out
            giftLevel = townLevel
            if townLevel > 1:
                giftLevel = townLevel - 1
            currentNPC.initializeGift( rand(gameObj.giftQuotes), gameObj.randomItem( giftLevel, rand(range(len(shopItems))) ))

        elif currentType == 'battle':
            giftLevel = townLevel
            if townLevel > 1:
                giftLevel = townLevel - 1
            stats = [
            #level
            townLevel,
            #xp reward
            townLevel*20,
            #gold reward
            townLevel*10,
            #HP
            50+(townLevel*25 + rand(range((-townLevel*5), townLevel*5+1))),
            #energy
            50+(townLevel*25 + rand(range((-townLevel*5), townLevel*5+1))),
            #strength
            5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
            #Dexerity
            5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
            #Inteligence
            5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
            #Cleaverness
            5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
            #class
            rand(gameObj.listOfNPCClasses)(),
            #weapon
            gameObj.randomItem(giftLevel, 0),
            #armour
            gameObj.randomItem(giftLevel, 1)
            ]
            currentNPC.initializeBattle(stats, rand(gameObj.battleQuotes))

        #add them to the NPC list for the town
        NPCs.append(currentNPC)

    #generate and return the town
    return gameObj.townPrototype(rand(gameObj.townNames),children,NPCs, y, x, level);


def link(towns):
    '''
    Links the towns with the same Y coordinate togather

    Arguments:
        towns: the towns with identical Y coordinates

    Returns:
        none
    '''
    if len(towns) > 1:
        towns[0].right = towns[1]
        towns[-1].left = towns[-2]

        for t in range(1, len(towns)-1):
            towns[t].right = towns[t+1]
            towns[t].left = towns[t-1]


def mapGen(centre, direction, level):
    '''
    psudo-randomly generates the levels that extend out from the centre

    Arguments:
        centre: list of centre levels
        direction: 1 on -1 depending on which side is being generated
        level: the level of the centre towns

    Returns:
        list of all towns created
    '''
    y = 0
    parent = centre
    allTowns = []

    #generates the levels between the centre towns and the end town
    for i in range(level-2):
        #The current layer of town being generated
        y += direction
        #the x coordinate of the current town being generated
        x = 0
        #the level of the town
        level += direction
        #the index of the central towns from where they will be assigned the new towns
        index = 0
        #assign the central levels. Every loop makes the last set of town generated into the next set of sentral towns
        children = parent
        #the amount if central towns left unassigned to new towns
        townsLeft = len(children)
        #the current list of new towns
        parent = []

        #generate a new town until all central towns are connected to new towns
        while(True):
            #each outer town is assigned 1-3 of the central towns

            #the amount of central towns assigned to the new town
            connections = rand(range(1,4))

            if connections < townsLeft:
                #if the amount of towns assigned is less than the amount of towns left

                #count down the amount of towns still left to assign
                townsLeft -= connections

                #generate new town and assign its central towns to it
                town = townGen(children[index:index*3],level,y,x)
                #add it to the list of new towns
                parent.append(town)
                #add it to the list of all towns
                allTowns.append(town)
                #move the index
                index += connections
                #iterate the x coordinate
                x+=1
                #link the central towns with the new town
                for child in children[index:index*3]:
                    child.parent.append(town)

            elif connections >= townsLeft:
                #if the amount of towns assigned is more than or equal to the amount of towns left

                #generate new town and assign its central towns to it
                town = townGen(children[index:],level,y,x)
                parent.append(town)
                allTowns.append(town)
                #link the central towns with the new town
                for child in children[index:]:
                    child.parent.append(town)
                break
        #links the newly generated towns togather with the ones next to them
        link(parent)

    #generate the outer town
    endTown = townGen(parent, level + direction, y + direction, 0)
    allTowns.append(endTown)
    #link the end town with the inner towns
    for child in parent:
        child.parent.append(endTown)

    #return all towns generated
    return allTowns


def worldGen():
    '''
    Generates the world. To be more spicific, it generates the final town followed by a desired number of other towns.
    As the towns are generated, they are linked with the town that comes after them. Afterwards they are linked with
    the towns that come before them.

    The world will be generated in a psudo-random diamond shape.

    Arguments:
        None

    Returns:
        The world
    '''
    print('Initializing world generation...')
    mapSize = 7
    #https://stackoverflow.com/questions/2356501/how-do-you-round-up-a-number-in-python
    halfMap = mapSize // 2 + (mapSize % 2 > 0)

    #Generating central levels
    print('Generating central levels...')
    
    allTowns = []
    #generate the levels at the very centre and add them to the list of all towns
    for a in range(rand(range(halfMap,halfMap*3))):
        allTowns.append(townGen([],halfMap,0,a))

    link(allTowns)


    #Generate the rest of the levels. That being the upper and lower triangles
    print('Generating the rest of the levels...')
    allTowns = allTowns + mapGen(allTowns, 1, halfMap) + mapGen(allTowns, -1, halfMap)
    for town in allTowns:
        town.finalize()

    #generate mandatory NPCs in a 2D list, where list[y] is a list of NPCs
    #These are all quest NPCs and bosses
    print('Generating main NPCs...')
    questNPCGen(allTowns, halfMap)

    #store the towns in the world object
    print('World generation complete!')
    return gameObj.world(allTowns, allTowns[-1])


def playerGen():
    '''
    Generates the player and all entities initially attached to it. 
    Generates the independant entities first and then the player.

    Arguments:
        None

    Returns:
        The player
    '''
    #generate the basic gear
    print('Generating starting equipment...')
    startClass = gameObj.default()
    startWeapon = gameObj.proceduralItem(1,0)
    startArmour = gameObj.proceduralItem(1,1)
    startInventory = [startWeapon, startArmour]

    print('Generating player...')
    return gameObj.player(startClass, startWeapon, startArmour, startInventory)

def questNPCGen(towns, halfMap):
    '''
    Generates the bosses and quest NPCs

    Arguments:
        towns: Every town in the game
        halfmap: The size of the world divided by 2 and rounded up

    returns:
        none
    '''
    for i in range(-halfMap+1, halfMap):
        levelTowns = [town for town in towns if town.y == i]

        # gives index of town in a certain y-coordinate
        questNPCLocation = rand(range(len(levelTowns)))
        bossNPCLocation = rand(range(len(levelTowns)))

        townLevel = i + halfMap

        #BOSS
        #added multiplier for each boss stat
        giftLevel = townLevel
        if townLevel > 1:
            giftLevel = townLevel - 1
        stats = [
        #level
        townLevel + 1,
        #xp reward
        townLevel*80,
        #gold reward
        townLevel*35+15,
        #HP
        60+(townLevel*30 + rand(range((-townLevel*5), townLevel*5+1))),
        #energy
        50+(townLevel*30 + rand(range((-townLevel*5), townLevel*5+1))),
        #strength
        5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
        #Dexerity
        5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
        #Inteligence
        5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
        #Cleaverness
        5+(townLevel*6 + rand(range((-townLevel*3), townLevel*3+1))),
        #class
        rand(gameObj.listOfNPCClasses)(),
        #weapon
        gameObj.randomItem(giftLevel, 0),
        #armour
        gameObj.randomItem(giftLevel, 1)
        ]
        
        # creates the boss and quest NPCs (the NPCs on the final level are different)
        if i < halfMap - 1:
            BOSS = gameObj.bossNPC(stats, rand(gameObj.names), rand(gameObj.bossQuotes))
            QUEST = gameObj.questNPC(rand(gameObj.names),BOSS, BOSS.name, rand(gameObj.questNPCQuotes))
        elif i == halfMap - 1:
            BOSS = gameObj.bossNPC(stats, rand(gameObj.names), rand(gameObj.finalBossQuotes))
            QUEST = gameObj.questNPC(rand(gameObj.names),BOSS, BOSS.name, rand(gameObj.finalquestNPCQuotes))

        # adds quest NPCs to the lost of NPCs in the current town
        for town in towns:
            if town.x == bossNPCLocation and town.y == i:
                town.NPCs.append(BOSS)
            if town.x == questNPCLocation and town.y == i:
                town.NPCs.append(QUEST)

def saver(player, world):
    '''
    Takes the player and the world stores the two in a saveFile object.
    This object is then pickled.

    Arguments:
        player: The player object
        world: The world object

    Returns:
        none
    '''
    #set the player's starting position

    #initialize save object
    save = saveFile(player, world)
    
    try:
        #save to file
        f = open('save', 'wb')
        pickle.dump(save, f)
        f.close()
        os.system('cls' if os.name == 'nt' else 'clear')
        game.hud(player)
        print('Saved successfully!')
        input('Press any key to continue')
    except:
        print('Something went wrong with the file I/O')

def newGame():
    '''
    Takes the player and the world and performs final setup before storing the two in a saveFile object.
    This object is then pickled

    Arguments:
        player: The player object
        world: The world object

    Returns:
        none
    '''
    #set the player's starting position
    player = playerGen()
    world = worldGen()
    player.town = world.start
    player.questLevel = world.start.y

    #initialize save object
    save = saveFile(player, world)
    
    try:
        #save to file
        f = open('save', 'wb')
        pickle.dump(save, f)
        f.close()
    except:
        print('Something went wrong with the file I/O')

    return player, world