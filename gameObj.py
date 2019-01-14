'''
This file contains all the objects in the game
'''
from random import choice as rand
import os
import menu
import game
import sys
#random NPC speak--------------------------------------------------------------------------------
quotes = ['Before the war, this nation was a peaceful place...', 'I like shorts. They are comfortable and easy to wear!',
'May you die with a sword in your hand.', 'I am weary of all of this fighting...', 'If these bastards want a war, we will give them one they will never forget!',
'I miss the peaceful days...', 'At this rate the nobles are going to tax the air we breathe...',
"Tavern's running a great deal on the house mead. It's sweet as honey yet filling as a night's supper.",
"I'm worried about the oncoming winter... The frost from last year destroyed most of our crops, and they say this year will be worse. What are we to do..."]
giftQuotes = ['It is dangerous to go alone. Here take this.', 'I found this on the ground earlier, I think you can make good use of it.',
'I found this earlier. It could be useful for combat, but I am tired of all the fighting so here, you can have it.',
'You will need this if you want to survive...', 'Take this...', "I got a new one of these, so you can have my old one.",
"Here, I have more of these than I know what to do with, take it.", "Listen, I don't want this thing but I don't want to just throw it away, you can have it.",
"I don't know what this thing is, you can have it."]
battleQuotes = ['Gimmie all your gold!', "When I'm through with you, you'll have more holes than a pincushion!",
"Hey! You're not supposed to be here!", 'You there! Spar with me!', "I'm going to send you to the depths of hell!",
"Say your prayers now, and God may accept you into heaven after I send you to his doorstep.", "Put the coin pouch on the ground and no one gets hurt!",
"How dare you enter our territory!", "The voices... I can't stop the voices...", "My sword will be sated by your blood!",
"GET OFF MY LAND!"]
bossQuotes = ["Lets get this over with, I have a date tonight.", "Uh when I crack open your head fruit what color juice comes out?",
"Do you know the definition of insanity...... me.", "There is only enough room for one of us in this world!",
"This is going to hurt!", "This is not your grave, but you are welcome to it.", "Pick a God and pray to it.",
"Your pathetic little adventure ends here, traveller!", "You have caught my attention traveller, but not my respect!",
"Where do you want to be buried?", "Don't you worry, I will make this quick!", "What fun is destruction if no 'precious' lives are lost?"]
finalBossQuotes = ["""I know who you are. You have caused me a lot of grief over the past few weeks. It is nice to finally put a face
to the one who has killed many of my loyal followers. The previous monarchy is dead, you need to let go of the past and join the new age.
Deep down you know I am not the villain! Why should a kingdom be passed along a 'royal' family instead of given to the smartest, strongest
people so it can thrive! The previous king saw this, which is why he never named an heir. The price for freedom is high, it always has been, 
and not everyone has the guts to see that and act accordingly. I know you think what I am doing is wrong, but after
I am done ridding this kingdom of its weaknesses we will be stronger than ever. I gave you many chances to join me! I have had my 
opportunities to take you out of the equation completely, but I wanted you to join me. You made a mistake coming here with your weapons drawn.
 You exist because I allowed it, and you will end because I demand it!"""]
questNPCQuotes = ["is causing everyone grief. Please take care of him!", "has caused me too many sleepless nights.",
"robbed me! Please help!", "stole my money, kill him!", "stole my goat, please get him back!", "is the one who took my chickens.",
"is a bad man!! He has a man hostage in the town square!", "can't be trusted...", "is trying to escape with our son!!",
"is sketchy, I think he has my coin sack.", "doesn't like dogs, he is not a man worth befriending.","will try to kill you.",
"knows who you are, be careful around him!", "is strange, there is something off about him.","has anger problems!"]
finalquestNPCQuotes = ["""I know who you are, and so do they! They know you are coming for them, so make sure that you are prepared when you 
find the new ruler. I am not sure what you should expect, but I know they are very dangerous. I tried putting poison in the water, but got 
caught doing so. I barely made it out alive. If they find me they will kill me!"""]
#random names------------------------------------------------------------------------------------
names = ["Saege", "Clafa", "Nathye", "Cuthfre", "Exard Salte", "Aelsith", "Ealwyn", "Waltin", "Breda", "Gyleon", "Sige",
"Gralphye", "Hearda", "Narder", "Conbern", "Ewis", "Folke Arrot", "Gerey", "Daedhug", "Richye Reyne", "Edmugh", 
"Ealwanc", "Mesym Pyley", "Athyer Borne", "Ecgrert", "Aewan", "Berter Drove", "Lewis Mason", "Aldrer", "Ames", "George", 
"Wine", "Iged", "Liamart", "Hughye Neray", "Edward Illiard", "Helhelmh", "Cyne", "Cirhelm", "Gerey Corby", "Michelle", 
"Eril Pycey", "Ellel", "Burhe", "Eadwith", "Sida", "Frictiue", "Wenberg", "Arior", "Cilia Lyne", "Elen", 
"Helia", "Waerburg", "Wynna", "Wychtlu", "Sunne", "Beatry Geddaye", "Cyna", "Burhe", "Eanswild", "Beornwe", 
"Burgiue", "Ehith", "Hrichtra", "Efrin", "Evel", "Wigswe", "Cily Boley", "Gythiue", "Engen", "Thrakilm", 
"Shari", "Orin", "Bari", "Gimli", "Dainarv", "Throri", "Arral", "Nanain", "Atur", "Gedu", 
"Fari", "Frimah", "Gili", "Zigil", "Frainan", "Ziri", "Bali", "Khatelch", "Muli", "Zuri", 
"Zaghim", "Orin", "Thori", "Thrazur", "Urur", "Grinarv", "Thainarv", "Gwali", "Grakun", "Thrinarv", 
"Thundu", "Zigam", "Thrinan", "Roda", "Kilmin", "Khakurd", "Gamil", "Khundu", "Bifar", "Thori", 
"Zigil", "Ukat", "Gabi", "Bori", "Grinain", "Kada", "Threri", "Udlat", "Dwali", "Muli", 
"Kali", "Umras", "Ukad", "Umur", "Bori", "Kurdu", "Dwoinan", "Ugmaz", "Umund", "Finore", 
"Finethald", "Gwionerdhil", "Quennore", "Guiladan", "Enelel", "Akin", "Elelmil", "Lodire", "Minerdhor", "Egnoror", 
"Maeglomak", "Mionerdhor", "Saerodior", "Aldithin", "Finore", "Imin", "Annael", "Elenlon", "Dilador", "Emmilin", 
"Elellan", "Dirohil", "Danore", "Oron", "Alaglor", "Finasaer", "Edramdil", "Ohin", "Inrod", "Minare", 
"Saerethon", "Orodrel", "Eler", "Galmabli", "Elron", "Milebre", "Olfindin", "Olarfin", "Golioneth", "Elegos", 
"Armil", "Enwendin", "Arfimin", "Finasaer", "Pengoneth", "Athin", "Mothere", "Dorahel", "Amras", "Gonarfin", 
"Argophil", "Dirohilb", "Enlon", "Mothingon", "Enelmir", "Ennalgas", "Alan", "Celemmaedhr", "Golungilg", "Ilmimen", 
"Nelalwe", "Findiser", "Celaser", "Ealoth", "Nelebrie", "Artanen", "Elwis", "Nimlothien", "Elelyel", "Serianye", 
"Celaser", "Nimlaser", "Imel", "Niserie", "Elellas", "Enen", "Nelye", "Nelaser", "Findalye", "Irien", 
"Adrierwel", "Alamas", "Celadrie", "Indellas", "Niserie", "Elyenwen", "Eldalwen", "Artaloth", "Arwel", "Elyelel", 
"Elenwel", "Elenel", "Atiel", "Imis", "Ilatiel", "Galotie", "Eldas", "Nelladrie", "Arwedhel", "Helry", 
"Brobert", "Maco", "Sonod", "Rime", "Gaffo", "Bando Burrubb", "Herog", "Wiso", "Hughye", "Mado", 
"Ancold", "Fastob", "Arthur", "Haroc", "James Mylne", "Adoc", "Gery", "Bardo", "Hamso", "Manas", 
"Raffolk Vere", "Imas", "Baldo", "Gyles Finchey", "Anthol", "Reder", "Warder Tine", "Fastob Took", "Haric", "Mentha", 
"Mela", "Ryllia Owes", "Loba Chilly", "Joyce", "Phera", "Mina", "Hone", "Estel", "Suse", "Ennen", 
"Kathon Parre", "Eryn", "Loba", "Aben Mylne", "Lavia Burrubb", "Sane Wake", "Audreyn Bowe", "Camay", "Ennel", "Wene", 
"Lavy Tunnell", "Joane", "Druba", "Ilil", "Apphilda", "Mars", "Hone", "Mara Urron", "Elix", ]
townNames = ["Garen's Well", "Swadlincote", "Porthaethwy", "Queenstown", "Galssop", "Bredon", "Deathfall", "Aeston", "Whaelrdrake", "Newsham", "Northwich", 
"Wolfwater", "Easthaven", "Farnfoss", "Hampstead", "Blackpool", "Bredon", "Pontybridge", "Carleone", "Woolhope", "Oldham", 
"Doncaster", "Blencogo", "Goldcrest", "Caister", "Lingmell", "Tergaron", "Durnatel", "Chester", "Iyesgarth", "Braedon", 
"Abingdon", "Bredwardine", "Marren's Eve", "Barkamsted", "Forstford", "Doonatel", "Furness", "Colchester", "Alverton", "Cleethorpes", 
"Aquarin", "Coningsby", "Auchendale", "Fanfoss", "Blencathra", "Azmarin", "Aucteraden", "Westray", "Coniston", "Ship's Haven", 
"Little Ivywood", "Anghor Wat", "Peatsland", "Bury", "Aethelney", "Arkmunster", "Bellmare", "Moonbright", "Aylesbury", "Padstow", 
"Clare View Point", "Bromwich", "Blaenau", "Braedwardith", "Farnworth", "Thorpes", "Helmfirth", "Cromer", "Langdale", "Caerfyrddin", 
"Pendle", "Barcombe", "Larton", "Alderdyfi", "City of Fire", "Whiteridge", "Holden", "Briar Glen", "Erith", "Snowmelt", 
"Drumnacanvy", "Norbury", "Durmchapel", "Marclesfield", "Three Streams", "Daemarrel", "Norbury", "Colchester", "Glanchester", "Addersfield", 
"Wakefield", "Hillfar", "Ramshorn", "Barncombe", "Old Ashton", "Lanercost", "Naporia", "Murlayfield", "Stratford", "Helmfirth", 
"Black Hollow", "Far Water", "Swindlincote", "Farnfoss", "Lullin", "Paethsmouth", "Waekefield", "Ruthorham", "Lybster", "Middlesborough", 
"Ecrin", "Alderrdeen", "Guthram", "Merton", "Watford", "Swordbreak", "Laenteglos", "Nantgarw", "Sudbury", "Torrine", 
"Penshaw", "Haerndean", "Claethorpes", "Anghor Wat", "Begger's Hole", "Tenby", "Pantmawr", "Ilfracombe", "Doveport", "Broken Shield", 
"Barnemouth", "Clacton", "Ffestiniog", "Glossop", "Bredon", "Lakeshore", "Penkurth", "Newham", "Berkton", "Panshaw", 
"Runswick", "Saxondale", "Tow", "Narthwich", "Ula'ree", "Cewmann", "Astrakane", "Troutbeck", "Murrayfield", "Cromerth", 
"Llaneybyder", "Porthcrawl", "Acton", "Garrigill", "Openshaw", "Aucteraden", "Clare View Point", "Solaris", "Tardide", "Graycott", 
"Harthwaite", "Bardford", "Drumchapel", "Linemell", "Azmarin", "Matlock", "Harthwaite", "Rochdale", "Aylesbury", "Warrington", 
"Elinmylly", "Pirn", "Airedale", "Brickelwhyte", "Hurtlepool", "Willowdale", "Paethsmouth", "Lakeshore", "Carran", "Hempholme", 
"Beachmarsh", "Fallholt", "Dewsbury", "Worcester", "Palperroth", "Gillamoor", "Rochdale", "Little Ivywood", "Cesterfield", "Peatsland", 
"Poltragow", "Kara's Vale", "Shepshed", "Skystead", "Deathfall", "Anghor Thom", "Sarton", "Aquarine", "Alverton", ]
#weapon names
weaponNames = ['Gauntlet','Dagger','Staff','Spear','Sword']
armourNames = ['Armour','Cloak','Robe','Chainmail','Plate']
charmNames = ['Gem','Fang','Ring','Pendant']
material = ['Infernalbrick', 'Volatile brick', 'Sweet velour', 'Somber hide', 'Demonic bone', 'Gloomy lead', 
'Veilresin', 'Enigma linen', 'Stained lace', 'Ancient paper', 'Exuberant fiber', 'Mighty resin', 'Brainvelvet',
'Eternityresin', 'Fortune fleece', 'Marked lace', 'Tranquil tin', 'Long steel', 'Lunargold', 'Great hide', 'Solarresin',
'Dragonnickel', 'Cloudzinc', 'Glamorous fur', 'Exalted paper', 'Bright silver', 'Shady nickel', 'Nether sand', 'Scaletin',
'Omenweave', 'Grand nickel', 'Spell twill', 'Phantomnickel', 'Phasesatin', 'Feigned stone', 'Stark soil', 'Lucky brick',
'Aero resin', 'Depthglass', 'Aegis hide', 'Demonhide', 'Chain copper', 'Wicked lead', 'Odd cotton', 'Frosty knit',
'Infinite titanium', 'Pyrofleece', 'Solar paper', 'Craven twill', 'Bold wood', 'Putrid knit', 'Pitch cobalt',
'Wicked zinc', 'Lightmarble', 'Frost bone', 'Supreme steel', 'Utopian wood', 'Heavy copper', 'Grim fleece',
'Flawless sand', 'Arctic denim', 'Icebark', 'Halfcloth', 'Mild lead', 'Eternity copper', 'Exhausted gold',
'Glamorous lead', 'Corrupt skin', 'Planar lead', 'Moonsilver']
#player------------------------------------------------------------------------------------------
class player:
    def __init__(self, Class, weapon, armour, inventory):
        self.level = 1
        self.xp = 0
        self.xpDenominator = 75

        self.HP = 150
        self.maxHP = 150
        self.energy = 100
        
        self.strength = 10
        self.dexerity = 10
        self.inteligence = 10
        self.cleaverness = 10
        
        self.gold = 0
        self.weapon = weapon
        self.armour = armour
        self.charm = None

        self.inventory = inventory
        
        self.Class = Class

        self.town = None
        self.questLevel = 0

        
#classes------------------------------------------------------------------------------------------

class default:
    
    def __init__(self):
        self.thing = 'class'
        
        self.name = 'Default Class'
        
        self.HPUp = 10
        self.energyUp = 5
        self.strUp = 5
        self.dexUp = 5
        self.intelUp = 5
        self.clevUp = 5
        
        self.abilities = ['Punch Harder!','Knockout Blow']
        self.costs = [10,10]
        self.value = 50

    def ability1(self, userDict, enemyDict):
        print('Punched Harder!')

        userDict['fighter'].energy -= self.costs[0]

        userDict['cooldowns'][self.abilities[0]] = 4

        damage = int((userDict['fighter'].strength)*.75)

        return damage - enemyDict['defence']

    def ability2(self, userDict, enemyDict):
        print('Knockout Blow was used!')

        userDict['fighter'].energy -= self.costs[1]

        userDict['cooldowns'][self.abilities[1]] = 5

        if (rand(range(2))):
            enemyDict['status']['stun'] = 1
            print('The target is stunned!')
        else:
            print('Failed to Knockout')

        damage = (userDict['fighter'].strength)//3

        return damage - enemyDict['defence']

class warrior:
    
    def __init__(self):
        self.thing = 'class'
        
        self.name = 'Warrior Class'
        
        self.HPUp = 15
        self.energyUp = 2
        self.strUp = 8
        self.dexUp = 6
        self.intelUp = 1
        self.clevUp = 3

        self.abilities = ['Shield Bash','Stab Harder']
        self.costs = [15,15]
        self.value = 50

    def ability1(self, userDict, enemyDict):
        print('Shield Bash was used!')

        userDict['fighter'].energy -= self.costs[0]

        userDict['cooldowns'][self.abilities[0]] = 5

        enemyDict['status']['stun'] = 1
        print('The target is stunned!')

        damage = (userDict['fighter'].strength)//4

        return damage - enemyDict['defence']

    def ability2(self, userDict, enemyDict):
        print('Stabbed Harder!')

        userDict['fighter'].energy -= self.costs[1]

        userDict['cooldowns'][self.abilities[1]] = 5

        damage = (userDict['fighter'].strength)//2

        return damage - enemyDict['defence']


class mage:
    
    def __init__(self):
        self.thing = 'class'
        
        self.name = 'Mage Class'
        
        self.HPUp = 5
        self.energyUp = 15
        self.strUp = 1
        self.dexUp = 5
        self.intelUp = 10
        self.clevUp = 5
        
        self.abilities = ['Fireball','Freeze']
        self.costs = [20,40]
        self.value = 50

    def ability1(self, userDict, enemyDict):
        print('Fireball was used!')

        userDict['fighter'].energy -= self.costs[0]

        userDict['cooldowns'][self.abilities[0]] = 2

        enemyDict['status']['burn'] = 2
        print('The target is ablaze!')

        damage = int((userDict['fighter'].inteligence)*.5)

        return damage - enemyDict['defence']

    def ability2(self, userDict, enemyDict):
        print('Freeze was used!')

        userDict['fighter'].energy -= self.costs[1]

        userDict['cooldowns'][self.abilities[1]] = 5

        enemyDict['status']['stun'] = 2
        print('The target is frozen solid!')

        damage = int((userDict['fighter'].inteligence)*.6)

        return damage - enemyDict['defence']


class rogue:
    
    def __init__(self):
        self.thing = 'class'
        
        self.name = 'Rogue Class'
        
        self.HPUp = 10
        self.energyUp = 5
        self.strUp = 5
        self.dexUp = 10
        self.intelUp = 5
        self.clevUp = 5
        
        self.abilities = ['Crippling Poison','Vantage Strike']
        self.costs = [15,45]
        self.value = 50

    def ability1(self, userDict, enemyDict):
        print('Crippling Poison was used!')

        userDict['fighter'].energy -= self.costs[0]

        userDict['cooldowns'][self.abilities[0]] = 6

        enemyDict['status']['poison'] = 5
        print('The target is poisoned!')

        enemyDict['defence'] -= 1
        print("Target's defence lowered by 1!")

        damage = (userDict['fighter'].dexerity)//2

        return damage - enemyDict['defence']

    def ability2(self, userDict, enemyDict):
        print('Vantage Strike was used!')

        userDict['fighter'].energy -= self.costs[1]

        userDict['cooldowns'][self.abilities[1]] = 8

        bonus = int(0.1*(enemyDict['fighter'].maxHP - enemyDict['fighter'].HP))

        damage = (userDict['fighter'].dexerity) + bonus

        return damage - enemyDict['defence']


listOfNPCClasses = [default, warrior, mage, rogue]
#the world----------------------------------------------------------------------------------------
class world:
    def __init__(self, towns, start):
        self.towns = towns
        self.start = start


#towns--------------------------------------------------------------------------------------------
class townPrototype:
    
    def __init__(self, name, children, NPCs, Y, X, level):
        self.thing = 'town'
        
        self.name = name

        self.level = level

        self.y = Y
        self.x = X
        self.children = children
        self.parent = []
        self.left = None
        self.right = None
        self.exits = []

        self.NPCs = NPCs

    def finalize(self):
        if self.children:
            for t in self.children:
                self.exits.append(t)

        if self.parent:
            for t in self.parent:
                self.exits.append(t)

        if self.left:
            self.exits.append(self.left)

        if self.right:
            self.exits.append(self.right)


#NPCs---------------------------------------------------------------------------------------------
class NPCPrototype:

    def __init__(self, ntype, name):
        self.name = name

        self.thing = 'NPC'

        #One of 5 types
        self.type = ntype

    def initializeShop(self, items):
        self.text = 'Hello there! Please have a look at my fine wares.'
        self.inventory = items

    def initializeNone(self, text):
        self.text = text

    def initializeGift(self, text, item):
        self.text = text
        self.item = item

    def initializeBattle(self, stats, text):
        self.text = text

        #needs random weapon
        self.level = stats[0]
        self.xpReward = stats[1]
        self.goldReward = stats[2]
        self.HP = stats[3]
        self.maxHP = self.HP
        self.energy = stats[4]
        self.strength = stats[5]
        self.dexerity = stats[6]
        self.inteligence = stats[7]
        self.cleaverness = stats[8]
        self.Class = stats[9]
        self.weapon = stats[10]
        self.armour = stats[11]

    def interact(self, player, NPClist, index):
        os.system('cls' if os.name == 'nt' else 'clear')
        game.hud(player)
        print(self.text)

        if self.type == 'shop':
            while(True):
                os.system('cls' if os.name == 'nt' else 'clear')
                game.hud(player)
                print(self.text)

                for item in range(len(self.inventory)):
                    if self.inventory[item].thing == 'class':
                        print('(' +  str(item+1) + ')', self.inventory[item].name + '\033[0;33m' + ' (cost: ' + str(self.inventory[item].value) + ')' + '\033[0;m')   
                    else:
                        print('(' +  str(item+1) + ')', self.inventory[item].name + ' - lvl: ' + str(self.inventory[item].level) + ' -' + '\033[0;33m' + ' (cost: ' + str(self.inventory[item].value) + ')' + '\033[0;m')
                print('(0) Back')

                choice = menu.safeInput( range(len(self.inventory)+1) )

                if choice == 0:
                    print('Thank you, come again!')
                    return
                else:
                    item = self.inventory[choice-1]

                    # displays an item, comparing it to the one the player is currently wearing
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(item.name)
                    print('Cost:', item.value)
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
                    print('(1) Buy')
                    print('(0) Back')

                    # auto-equip option
                    choice = menu.safeInput(range(2))
                    if choice == 0:
                        pass
                    elif choice == 1 and player.gold >= item.value:
                        player.inventory.append(item)
                        player.gold -= item.value
                        print(item.name, 'was bought!')
                        input()
                        print()
                        print('Would you like to equip ' + item.name + '?')
                        print('(1) Equip')
                        print('(0) Back')

                        choice = menu.safeInput(range(2))
                        if choice == 0:
                            pass
                        elif choice == 1:
                            if item.thing == 'weapon':
                                player.weapon = item
                            elif item.thing == 'armour':
                                player.armour = item
                            elif item.thing == 'charm':
                                player.charm = item
                            elif item.thing == 'Class':
                                player.Class = item
                            print(item.name, 'equipped!')
                            input()
                        else:
                            print('You cannot afford this item!');
                            input()

        elif self.type == 'none':
            input()
            del NPClist[index]
            
        elif self.type == 'gift':
            player.inventory.append(self.item)
            print('You obtained', self.item.name+'!')
            input()
            del NPClist[index]

        elif self.type == 'battle':
            input()
            if game.battle(self, player):
                del NPClist[index]

    #define NPC abilities

class questNPC:
    def __init__(self, name, boss, bossName, text):
        self.name = name

        self.thing = 'NPC'

        self.type = 'quest'

        self.text = text

        #area boss you need to kill in order to advance
        self.quest = boss
        self.bossName = bossName

    def interact(self, player, NPClist, index):
        os.system('cls' if os.name == 'nt' else 'clear')
        game.hud(player)
        if self.quest.HP > 0:
            print(self.bossName + ' ' + self.text) #temp
        else:
            print('Thank you for killing ' + self.bossName + ', the world is a better place without them!') #temp
            player.questLevel += 1
            del NPClist[index]
            # would like to get rid of the hard-coded number here (mapSize - 1) - this is for mapSize = 7
            if self.quest.level >= 6:
                input("Press enter to continue: ")
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.stdout.write("Congratulations! You have killed the ruler and will now be crowned as the new ruler of the kingdom. ")
                sys.stdout.write("Many saw the ruler as tyrranical, and others as progressive. ")
                sys.stdout.write("Everything comes at a cost, and only you can determine if it is worth paying for. \n\n\n\n\n")
                print("Thank you for playing corruption!")
                input("Press enter to continue: ")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("You may continue exploring this world, however you have completed the main quest line.")
                input("Press enter to continue")


        input()

class bossNPC:
    def __init__(self, stats, name, text):
        #self.name = 'BOSS'
        self.name = name

        self.thing = 'NPC'

        self.type = 'battle'

        self.text = text

        self.level = stats[0]
        self.xpReward = stats[1]
        self.goldReward = stats[2]
        self.HP = stats[3]
        self.maxHP = self.HP
        self.energy = stats[4]
        self.strength = stats[5]
        self.dexerity = stats[6]
        self.inteligence = stats[7]
        self.cleaverness = stats[8]
        self.Class = stats[9]
        self.weapon = stats[10]
        self.armour = stats[11]

    def interact(self, player, NPClist, index):
        os.system('cls' if os.name == 'nt' else 'clear')
        game.hud(player)
        print(self.text)

        input()
        if game.battle(self, player):
            del NPClist[index]

#weapons------------------------------------------------------------------------------------------
class weaponPrototype:

    def __init__(self, name, thing, damage, strength, dexerity, inteligence, cleaverness, value, level):
        self.name = name

        self.thing = thing
        
        self.damage = damage

        self.strength = strength
        self.dexerity = dexerity
        self.inteligence = inteligence
        self.cleaverness = cleaverness

        self.value = value
        self.level = level


#armours------------------------------------------------------------------------------------------
class armourPrototype:

    def __init__(self, name, thing, defence, strength, dexerity, inteligence, cleaverness, value, level):
        self.name = name

        self.thing = thing
        
        self.defence = defence

        self.strength = strength
        self.dexerity = dexerity
        self.inteligence = inteligence
        self.cleaverness = cleaverness

        self.value = value
        self.level = level


#charms-------------------------------------------------------------------------------------------
class charmPrototype:

    def __init__(self, name, thing, strength, dexerity, inteligence, cleaverness, value, level):
        self.name = name

        self.thing = thing

        self.strength = strength
        self.dexerity = dexerity
        self.inteligence = inteligence
        self.cleaverness = cleaverness

        self.value = value
        self.level = level


#random generation functions----------------------------------------------------------------------
def randomItem(level, itype):
    choices = []
    if itype == 3:
        for i in listOfNPCClasses:
            choices.append(i)
        return rand(choices)()
    else:
        return proceduralItem(level, itype)

def proceduralItem(level, itype):

    statTotal = level*10
    numberOfStats = 5
    if itype == 2:
        numberOfStats = 4
    remainder = statTotal%numberOfStats
    upperBound = statTotal//numberOfStats+1

    stats = []
    for stat in range(numberOfStats):
        stats.append(rand(range(upperBound)))

    remainder += statTotal-sum(stats)

    stat1 = rand(range(numberOfStats))
    stat2 = rand(range(numberOfStats))

    subType = stat1

    stats[stat1] += (remainder//3)*2
    remainder -= (remainder//3)*2
    stats[stat2] += remainder

    if itype == 1:
        stats[4] = (stats[4]*level)-3
    elif itype == 0:
        stats[4] = int(stats[4]*1.25)+3

    if itype == 0:
        return weaponPrototype(rand(material)+' '+weaponNames[subType], 'weapon', stats[4], stats[0], stats[1], stats[2], stats[3], statTotal, level)
    elif itype == 1:
        return armourPrototype(rand(material)+' '+armourNames[subType], 'armour', stats[4], stats[0], stats[1], stats[2], stats[3], statTotal, level)
    else:
        return charmPrototype(rand(material)+' '+charmNames[subType], 'charm', stats[0], stats[1], stats[2], stats[3], statTotal, level)


#-------------------------------------------------------------------------------------------------