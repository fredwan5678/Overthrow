import copy, os, sys
'''
IMPORTANT NOTE ABOUT THE AI:

IT HAS FLAWS AND IS SOMEWHAT UNFINISHED!

The AI surrently has trouble going through every single outcome of battle and *****may even reach the recursion
limit***** if there are enough possible outcomes. We were not able to slove this issue in time. If we did have time
We would put a limit on how many turns into the future it sees and change the best outcome chriteria
accordingly.
'''


class HiddenPrints:
    '''
    #https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python

    An object that stops all print statements by setting the stdout to null.

    It fixes it when exited.
    '''
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def AI(fight, options):
    '''
    The function that is called when the AI is activated in battle.
    It initializes the recusion and chooses the best outcome from the results

    Arguments:
        fight: Th battlefield object where the battle is happening
        options: the options currently available to the AI

    Returns:
        The best option
    '''
    #creates a copy of the current battle, as to not modify it when doing the simulation
    battleground = copy.deepcopy(fight)

    #turns off print statements
    with HiddenPrints():
        allSequences = []
        #the damage done by each sequence
        damages = []
        #the amount of stun inflicted by each sequence
        statuses = []

        #saves the current state of the fight
        savedStatus = copy.deepcopy(battleground.playerDict['status'])
        savedCooldowns = copy.deepcopy(battleground.enemyDict['cooldowns'])

        #for every option: recourse and simulate
        for option in options:
            #restore the fight to the saved state
            battleground.playerDict['status'] = savedStatus
            battleground.enemyDict['cooldowns'] = savedCooldowns
            #recourse
            seq, deltaHP, status = recursiveSimulation(battleground, option, [], 0, 0)
            #add to the lists of data
            allSequences += seq
            damages += deltaHP
            statuses += status

        #find fastest kill times
        fastestKill = min([len(seq) for seq in allSequences])
        fastKillIndexes = [index for index in range(len(allSequences)) if len(allSequences[index]) == fastestKill]

        #of those, find the one that inflicts the most stun
        mostStun = max([statuses[index] for index in fastKillIndexes])
        bestOptionIndexes = [seqIndex for seqIndex in fastKillIndexes if statuses[seqIndex] == mostStun]
        
    #arbritarily return the first of the best sequences(since they all meet the chriteria anyway)
    return allSequences[bestOptionIndexes[0]][0]


def simulationTurn(battleground, choice):
    '''
    A simulated turn, except the chosen move is given at the start and the next options are given after

    Arguments:
        batteground: The battleground object
        choice: the chosen move

    returns:
        The outcomes of the chosen move
    '''
    if choice == 1:
        damage = battleground.enemy.weapon.damage//4+battleground.enemy.strength//4 - battleground.enemyDict['defence']
    elif choice == 2:
        damage = battleground.enemy.Class.ability1(battleground.enemyDict, battleground.playerDict)
    elif choice == 3:
        damage = battleground.enemy.Class.ability2(battleground.enemyDict, battleground.playerDict)

    status = 0
    damageUp, statusUp = simulationTick(battleground)
    status += statusUp
    damage += damageUp

    options = []

    #strike is always an option
    options.append(1)

    for a in range(len(battleground.enemyDict['fighter'].Class.abilities)):
        if ((battleground.enemy.Class.abilities[a] not in battleground.enemyDict['cooldowns'] or battleground.enemyDict['cooldowns'][battleground.enemy.Class.abilities[a]] <= 0) and battleground.enemy.energy >= battleground.enemy.Class.costs[a]):
            options.append(a+2)

    return options, damage, status


def recursiveSimulation(battleground, choice, prevSequence, deltaHPtotal, deltaStatusTotal):
    '''
    Recursivly goes through every possibility of battle.

    Arguments:
        battleground: The current battleground object
        choice: The current choice of move
        prevSequence: a list of the choices before the current one
        +information from the last few choices

    Returns:
        A list of sequences
        +their effects
    '''
    finalSequences = []
    damages = []
    statuses = []

    options, deltaHP, status = simulationTurn(battleground, choice)
    deltaStatusTotal += status
    deltaHPtotal += deltaHP
    prevSequence.append(choice)

    print(deltaHPtotal)

    #save the state of the battle and reset to it after every loop
    savedStatus = copy.deepcopy(battleground.playerDict['status'])
    savedCooldowns = copy.deepcopy(battleground.enemyDict['cooldowns'])

    battleground.playerDict['status'] = savedStatus
    battleground.enemyDict['cooldowns'] = savedCooldowns

    #stop of the player is dead
    if deltaHPtotal >= battleground.player.HP:
        print('return')
        return [prevSequence], [deltaHPtotal], [deltaStatusTotal]

    for option in options:
        seq, deltaHP, status = recursiveSimulation(battleground, option, prevSequence, deltaHPtotal, deltaStatusTotal)
        finalSequences += seq
        damages += deltaHP
        statuses += status
    return finalSequences, damages, statuses


def simulationTick(battleground):
    '''
    Does of turn effect similarly to how the battle does it. It returns data from the outcome

    Argument:
        battleground: The current battle object

    returns:
        information about the outcome
    '''
    fighter = battleground.enemyDict
    target = battleground.playerDict

    stun = False
    damage = 0
    status = 0

    for cooldown in fighter['cooldowns'].keys():
        if fighter['cooldowns'][cooldown] != 0:
            fighter['cooldowns'][cooldown] -= 1


    for effect in target['status'].keys():
        if battleground.status[effect][0] == 'stun' and target['status'][effect] > 0:
            stun = True
            status = 1
        elif battleground.status[effect][0] == 'dot' and target['status'][effect] > 0:
            damage += battleground.status[effect][1]

        target['status'][effect] -= 1

    return damage, status