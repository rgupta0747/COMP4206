


import random
import time
from matplotlib import pyplot as plt
from termcolor import colored


"""
Function: createMatrix
Parameters: # rows, # columns
Purpose: create a 2d matrix
Method: Creates a 2d list and fills the list with numbers from 0 to N^2
Result: returns NxN matrix as a 2D list
"""
def createMatrix(row, col):
    number = 0
    matrix = [[0 for x in range(row)] for y in range(col)]
    for x in range(row):
        for y in range(col):
            matrix[x][y] = number
            number+=1
    return matrix

"""
Function: isSick
Parameters: agent object
Purpose: determine if agent is sick
Method: Checks if agent's health is infected
Result: Boolean determining if agent is sick or not
"""
def isSick(agent):
    if (agent.getHealth() == "infected"):
        return True
    return False

"""
Function: whichAgentisInfected
Parameters: agent1 object, agent2 object
Purpose: determine which agent is sick
Method: checks if either agent is sick
Result: A string for agent1, agent2, or neither
"""
def whichAgentisInfected(agent1, agent2):
    if (isSick(agent1)):
        return "agent1"
    elif (isSick(agent2)):
        return "agent2"
    else: return "none"

"""
Function: createAgentID
Parameters: number of agents in simulation
Purpose: create a list of agent ids
Method: creates a list of agent ids where each id begins with the letter
A and is a number
Result: A list of containing agent id strings
"""
def createAgentID(size):
    agentList = []
    for x in range(size):
        agentList.append("A" + str(x))
    return agentList

"""
Function: generateRandomX
Parameters: number of rows in grid
Purpose: generate random value
Method: calls randint function in random library to generate random value
Result: random value between 0 and rows-1.
"""
def generateRandomX(row):
    return random.randint(0,row-1)

"""
Function: generateRandomY
Parameters: number of columns in grid
Purpose: generate random value
Method: calls randint function in random library to generate a random value
Result: random value between 0 and columns-1
"""
def generateRandomY(col):
    return random.randint(0,col-1)

"""
Function: getX
Parameters: a tuple corresponding to an (X,Y) coordinate
Purpose: get x value
Method: indexes the first value in the tuple
Result: integer corresponding to x value
"""
def getX(location):
    return location[0]

"""
Function: getY
Parameters: a tuple corresponding to an (X,Y) coordinate
Purpose: get y value
Method: indexes the second value in the tuple
Result: integer corresponding to y value
"""
def getY(location):
    return location[1]

"""
Function: whichWayToMove
Parameters: None
Purpose: get a random direction to move
Method: gets a random value between 1 and 5 to determine the direction to move
Result: A string representing the direction the agent will move
"""
def whichWayToMove():
    direction = random.randint(1,5)
    if (direction == 1): return "north"
    if (direction == 2): return "east"
    if (direction == 3): return "south"
    if (direction == 4): return "west"
    if (direction == 5): return "stays"


"""
Function: movesLeftRight
Parameters: y coordinate, the direction to move, and number of columns in the grid
Purpose: move the agent in a specific direction left or right
Method: first checks boundary cases (if at edges) and if direction moves agent
outside grid. If agent moves off grid, do not move agent. If boundary case not an
issue, then move agent left or right depending on direction
Result: y value with new location
"""
def movesLeftRight(y, direction, cols):
    if (y == 0 and direction == "east"):
        newYLocation = y+1
    elif (y == 0 and direction == "west"):
        newYLocation = y
    elif (y == cols-1 and direction == "west"):
        newYLocation = y-1
    elif (y == cols-1 and direction == "east"):
        newYLocation = y
    elif (direction == "stays"): newYLocation = y
    else:
        if (direction == "east"):
            newYLocation = y+1
        else:
            newYLocation = y-1
    return newYLocation

"""
Function: movesUpDown
Parameters: x coordinate, the direction to move, and number of rows in the grid
Purpose: move the agent in a specific direction up or down
Method: first checks boundary cases (if at edges) and if direction moves agent
outside the grid. If agent moves off grid, do not move agent. If boundary case is
not an issue, then move agent up or down depending on direction.
Result: x value with new location.
"""
def movesUpDown(x, direction, rows):
    if (x == 0 and direction == "south"):
        newXLocation = x+1
    elif (x == 0 and direction == "north"):
        newXLocation = x
    elif (x == rows-1 and direction == "north"):
        newXLocation = x-1
    elif (x == rows-1 and direction == "south"):
        newXLocation = x
    elif (direction == "stays"): newYLocation = x
    else:
        if (direction == "south"):
            newXLocation = x+1
        else:
            newXLocation = x-1
    return newXLocation

"""
Function: addAgentsToMatrix
Parameters: matrix and the agent object
Purpose: add an agent object to the matrix
Method: goes through each location in the matrix and compares is to where the agent is
supposed to be located. When it matches it adds the agent to that location in the matrix
Result: A new matrix with an agent object added
"""
def addAgentsToMatrix(matrix, agent):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
                if (x == getX(agent.getLocation()) and y == getY(agent.getLocation())):
                    matrix[x][y] = agent.getAgentId()
    return matrix

"""
Function: locationSame
Parameters: list of agent objects
Method: Goes through the list of agent objects (assuming there are at least 2) and compares
Purpose: get a list of collisions that occur in the matrix
each agent object's location to all other agent objects following it. If the locations are same,
then a tuple of both agents are added to a new list.
For example: if we have a list of agent objects [a1, a2, a3, a4], then we start with a1 and compare it's
location to a2, a3, and a4. Then we go to a2 and compare it to a3 and a4. Then we go to a3 and compare it to
a4. Any collisions are added to the collision list.
Result: list containing tuples of agents that collided are returned.
"""
def locationSame(agents):
    sameLocation = None
    collisions = []
    if (len(agents) > 1):
        for x in range(0, len(agents)):
            compLocation = agents[x]
            for y in range (x+1, len(agents)):
                if(compLocation.getLocation() == agents[y].getLocation()):
                    sameLocation = agents[y]
                    collisions.append((compLocation, sameLocation))
                else:
                    continue;
    return collisions

"""
Function: displayGrid
Parameters: matrix and list of agents
Purpose: display the matrix to the user with the agents
Method: First we get a list of agents that collided. We then go through the list and print a "!"
at any location a collision occured. Then we go through the matrix and at each location, check if
an agent object resides there. If not, print a white "-". If an agent object does live there, and there
was no collision, then we get the health of the agent. If the agent is healthy, then we print a the agent
id as white. If the agent is infected, we print the agent id as blue and add an "*" next to the id.
We modify the print methods so they print the results evenly and ensure the spacing is satisfied.
Result: None
"""
def displayGrid(matrix, agentList):
    listOfSameLocations = locationSame(agentList)
    for x in range(len(listOfSameLocations)):
        locationX = getX(listOfSameLocations[x][0].getLocation())
        locationY = getY(listOfSameLocations[x][0].getLocation())
        matrix[locationX][locationY] = "!  "
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if (isinstance(matrix[x][y], int)): print(colored("- ", 'white'), end="  ")
            if (isinstance(matrix[x][y], str)):
                if (matrix[x][y] != "!  "):
                    health = getHealth(matrix[x][y], agentList)
                    counter = locationInList(matrix[x][y], agentList)
                    if(health == "susceptible"):
                        if (counter < 10): print(matrix[x][y], end="  ")
                        else: print(matrix[x][y], end=" ")
                    if(health == "infected"):
                        if (counter < 10): print(colored(matrix[x][y] + "*", 'blue'), end=" ")
                        else: print(colored(matrix[x][y] + "*", 'blue'), end="")
                else: print(colored(matrix[x][y], 'yellow'), end=" ")
        print()

"""
Function: getHealth
Parameters: agent id and list of agents
Purpose: get the health of the agent given their id
Method: go through list of agent ids and if the id provided matches the id in the list,
get the health of the agent object
Result: string giving health of the agent object
"""
def getHealth(id, list):
    for x in range(len(list)):
        if (id == list[x].getAgentId()): return list[x].getHealth()

"""
Function: locationInList
Parameters: agent id and list of agents
Purpose: get the index of the id in the agent list
Method: go through list of agent ids and if the id provided matches the id in the list,
return the index position
Result: index position in list of agent provided
"""
def locationInList(id, list):
    for x in range(len(list)):
        if (id == list[x].getAgentId()): return x


"""
Function: setNewLocations
Parameters: direction to move, agent object, the number of rows, and number of columns
Purpose: Set the location of the agent object with a new location
Method: Get the old x and y value location of the agent object. Then using the direction,
determine if the agent should move left right, up down, or stay in place. Then set the new x
or new y value depending on which way the agetn moves.
Result: return the agent object with the new location.
"""
def setNewLocations(direction, agent, rows, cols):
    agentLocation = agent.getLocation()
    oldX = agentLocation[0]
    oldY = agentLocation[1]
    #once x and y values obtained, set the new agent location
    #if direction is stays don't move agent
    if (direction == "stays"):
        return agent
    #if direction is east or west, move left/right if possible
    elif (direction == "east" or direction == "west"):
        newY = movesLeftRight(oldY, direction, cols)
        agent.setAgentLocation(oldX, newY)
    #otherwise move the agent north south
    else:
        newX = movesUpDown(oldX, direction, rows)
        agent.setAgentLocation(newX, oldY)
    return agent


"""
Function: createAgent
Parameters: current agent object, type of agent to create
Purpose: convert an agent object to one of the given type
Method:
Return:
"""
def createAgent(agent, type):
    originalLocation = agent.getLocation()
    originalId = agent.getAgentId()
    if (type == "infected"): agent = InfectedAgent()
    if (type == "removed"): agent = RemovedAgent()
    # agent = InfectedAgent()
    agent.setAgentId(originalId)
    agent.setAgentLocation(getX(originalLocation), getY(originalLocation))
    return agent


#main function that runs the simulation
def runSimulation():
    print("Press q at any time to go back to the main menu")
    rows = input("Enter the size of your matrix (please enter # rows you want): ")
    if (rows == "q"): return
    rows = int(rows)
    columns = rows
    #These three lists are for the purpose of statistical gathering, nothing more
    sickAgents = []
    susceptibleAgents = []
    removedAgents = []
    counter = 0

    #sets the rows and columns
    numberOfAgents = input("Enter the number of agents on the board: ")
    if (numberOfAgents == "q"): return
    numberOfAgents = int(numberOfAgents)
    while(numberOfAgents >= columns*rows):
        numberOfAgents = input("You are putting too many agents on the board. Try Again: ")
        numberOfAgents = int(numberOfAgents)
        #sets number of agents in the grid
    iterations = input("How many iterations should this simulation run: ")
    if (iterations == "q"): return
    iterations = int(iterations)

    timeBeforeDeath = input("How many iterations should a sick agent last for before dying: ")
    if (timeBeforeDeath == "q"): return
    timeBeforeDeath = int(timeBeforeDeath)
    nameOfDisease = input("What is the name of the disease: ")
    proportionVaccinated = input("What percentage of the population is vaccinated? ")
    proportionVaccinated = int(proportionVaccinated)
    proportionVaccinated = float(proportionVaccinated/100)

    matrix = createMatrix(rows, columns)                                                        #creates the grid
    agentIDList = createAgentID(numberOfAgents)                                                 #creates a list of id's for each agent
    agentList = []
    print()
    for x in range(len(agentIDList)):                                                                          #go through list of ids and create a susceptible agent for each id and add it to list
        agentList.append(SusceptibleAgent())
        agentList[x].setAgentId(agentIDList[x])                                                #set id of agent to the agent id from list
        agentList[x].setAgentLocation(generateRandomX(rows), generateRandomY(columns))          #set the location of each agent randomly
        susceptibleAgents.append(agentList[x])
    print()
    #go through and add each agent to the matrix
    for x in range(len(agentList)):
        matrix = addAgentsToMatrix(matrix, agentList[x])
    displayGrid(matrix, agentList)                                                                          #prints the matrix with agents on the matrix
    print()
        #randomly generate a sick agent to be patient zero from the list of agents
        #make them an infected agent and put them in the agent list
    sickAgentIndex = random.randint(0, len(agentList) - 1)
    agentList[sickAgentIndex] = createAgent(agentList[sickAgentIndex], "infected")
    print("The sick agent is " + agentList[sickAgentIndex].getAgentId())
    sickAgents.append(agentList[sickAgentIndex])
    for x in range(len(susceptibleAgents)):
        if (x == sickAgentIndex):
            susceptibleAgents.remove(susceptibleAgents[x])
    biggestWave = 0
    timeOfBiggestWave = 0


    #randomly generate 10% of the total agents and set their vaccination status to true
    numberToVaccinate = int(proportionVaccinated * numberOfAgents)
    for x in range(numberToVaccinate):
        vaccinatedAgentIndex = random.randint(0, len(agentList)-1)
        while(agentList[vaccinatedAgentIndex].getHealth() == "infected"):
            vaccinatedAgentIndex = random.randint(0, len(agentList)-1)
        while(agentList[vaccinatedAgentIndex].getVaccinationStatus() == True):
            vaccinatedAgentIndex = random.randint(0, len(agentList)-1)
        agentList[vaccinatedAgentIndex].setVaccinationStatus()

    #This will store the (x,y) data collected from the simulation - x will measure time and y will
    #measure the changing data
    survivalDataX = []
    survivalDataY = []
    infectedDataX = []
    infectedDataY = []
    removedDataX = []
    removedDataY  = []
    precentDiffData = []
    changeInInfectionX = []
    changeInInfectionY = []
    previousIteration = 0
    for i in range(iterations):
        counter += 1;
        #sleep for 2 seconds so you can see each iteration progress. Lower this to speed up the iterations or increase this to slow down th iterations
        time.sleep(2)
        #This is the loop that would simulate agents moving on the grid
        print()
        #get a direction that each agent will move (each agent moves in a random direction, independent of the other agents.
        for x in range(len(agentList)):
            direction = whichWayToMove()
                #go through the list of agents and set their location to the new direction
            agentList[x] = setNewLocations(direction, agentList[x], rows, columns)
        print()
        print()
        matrix = createMatrix(rows, columns)                                                    #reinitialize the grid (a.k.a clear the matrix)
        for x in range(len(agentList)):
            matrix = addAgentsToMatrix(matrix, agentList[x])                                         #add agents with new positions to the grid
            #go through agent list and check for collisions
        listOfCollisions = locationSame(agentList)
            #if there were any collision, do this
        if(len(listOfCollisions) != 0):
                #go through list of collisions and see if either agent that collided was infected
            for x in range(len(listOfCollisions)):
                    #checks if an agent in the collision was infected
                agent = whichAgentisInfected(listOfCollisions[x][0], listOfCollisions[x][1])
                    #if no agent infected, continue through collision list
                if (agent == "none"): continue
                #if the first agent was sick and second was not (a.ka. susceptible) then make the second agent in the collision infected
                if (agent == "agent1" and not isSick(listOfCollisions[x][1])):
                    if (listOfCollisions[x][1].getVaccinationStatus() == True): continue
                    #go through the list of agents and figure out which agent in the list is infected and make that agent infected
                    for y in range(len(agentList)):
                        if (listOfCollisions[x][1].getAgentId() == agentList[y].getAgentId()):
                            agentList[y] = createAgent(agentList[y], "infected")
                #if the second agent was sick and first was not (a.ka. susceptible) then make the first agent in the collision infected
                elif (agent == "agent2" and not isSick(listOfCollisions[x][0])):
                    #go through the list of agents and figure out which agent in the list is infected and make that agent infected
                    if (listOfCollisions[x][0].getVaccinationStatus() == True): continue
                    for y in range(len(agentList)):
                        if (listOfCollisions[x][0].getAgentId() == agentList[y].getAgentId()):
                            agentList[y] = createAgent(agentList[y], "infected")
        print()
        tempAgentList = []
        tempAgent = None
        flag = False
        finishedBecauseAllDead = False
        finishedBecauseAllSafe = False
        for x in range(len(agentList)):
            if (len(susceptibleAgents) == 0):
                finishedBecauseAllDead = True
                flag = True
                break
            if (agentList[x].getHealth() == "infected" and locationInList(agentList[x].getAgentId(), sickAgents) != None):
                if (timeBeforeDeath == agentList[x].getTimeOfSickness()):
                    tempAgent = agentList[x]
                    for y in range(len(sickAgents)):
                        if (tempAgent.getAgentId() == sickAgents[y].getAgentId()):
                            sickAgents.remove(tempAgent)
                            break
                    tempAgent = createAgent(tempAgent, "removed")
                    removedAgents.append(tempAgent);
                else:
                    agentList[x].increaseTimeOfSickness();
            elif (agentList[x].getHealth() == "infected" and locationInList(agentList[x].getAgentId(), sickAgents) == None):
                    sickAgents.append(agentList[x])
                    tempIndex = x
                    for y in range(len(susceptibleAgents)):
                        if (agentList[x].getAgentId() == susceptibleAgents[y].getAgentId()):
                            susceptibleAgents.remove(susceptibleAgents[y])
                            break;
            if (tempAgent != None):
                if (len(tempAgentList) != 0):
                    for x in range(len(tempAgentList)):
                        if (tempAgent.getAgentId() == tempAgentList[x].getAgentId):
                            tempAgentList.remove(tempAgentList[x])
                else:
                    for i in range(len(agentList)):
                        if (agentList[i].getAgentId() != tempAgent.getAgentId()):
                            tempAgentList.append(agentList[i])

            tempAgent = None
        if (len(tempAgentList) > 0): agentList = tempAgentList
        newSickAgents = []
        for x in range(len(sickAgents)):
            if (sickAgents[x].getTimeOfSickness() < timeBeforeDeath): newSickAgents.append(sickAgents[x])
        agentList = susceptibleAgents + newSickAgents
        if(len(newSickAgents) > biggestWave):
            biggestWave = len(newSickAgents)
            timeOfBiggestWave = counter
        if (len(newSickAgents) == 0):
            finishedBecauseAllSafe = True
            flag = True
            break
        displayGrid(matrix, agentList)                                                                     #print new grid
        if (flag): break
        print("At the end of Time: " + str(counter) + ", here are the stats: ")
        print(colored("--------------------------------------------------------", 'red'))
        print("The number of Susceptible Agents is : " + str(len(susceptibleAgents)))
        print("The number of Infected Agents is : " + str(len(newSickAgents)))
        if (len(removedAgents) + len(newSickAgents) + len(susceptibleAgents) != numberOfAgents):
            numberOfRemovedAgents = numberOfAgents - len(susceptibleAgents) - len(newSickAgents)
            print("The number of Removed Agents is : " + str(numberOfAgents - len(susceptibleAgents) - len(newSickAgents)))
        else:
            numberOfRemovedAgents = len(removedAgents)
            print("The number of Removed Agents is : " + str(len(removedAgents)))
        survivalDataX.append(counter)
        survivalDataY.append(len(susceptibleAgents))
        infectedDataX.append(counter)
        infectedDataY.append(len(newSickAgents))
        removedDataX.append(counter)
        removedDataY.append(numberOfRemovedAgents)
        changeInInfectionX.append(counter)
        if (counter == 1): changeInInfectionY.append(len(newSickAgents))
        else:
            if (previousIteration == len(newSickAgents)):
                valueToAppend = len(changeInInfectionY) - 1
                changeInInfectionY.append(changeInInfectionY[valueToAppend])
            else:
                changeInInfectionY.append(len(newSickAgents)/previousIteration)

        previousIteration = len(newSickAgents)
    print()
    print()
    if (finishedBecauseAllDead):
        print(colored("**************************************************************", 'red'))
        print(colored("   SIMULATION TERMINATED - NO MORE HEALTHY AGENTS REMAINING", 'red'))
        print(colored("**************************************************************", 'red'))
    if (finishedBecauseAllSafe):
        print(colored("**************************************************************", 'red'))
        print(colored("   SIMULATION TERMINATED - NO MORE SICK AGENTS REMAINING", 'red'))
        print(colored("**************************************************************", 'red'))

    print()
    print(colored("SIMULATION COMPLETED", 'yellow'))
    print("--------------------")
    print()
    print("After " + str(counter) + " iterations of the simulator produced the following results:")
    print()
    print("Number of Susceptible: \t\t\t" + str(len(susceptibleAgents)))
    print("Number of Infected: \t\t\t" + str(len(newSickAgents)))
    if (len(removedAgents) + len(newSickAgents) + len(susceptibleAgents) != numberOfAgents):
        removed = (numberOfAgents - len(susceptibleAgents) - len(newSickAgents))
        print("Number of Removed : \t\t\t" + str(numberOfAgents - len(susceptibleAgents) - len(newSickAgents)))
    else:
        removed = len(removedAgents)
        print("Number of Removed : \t\t\t" + str(len(removedAgents)))
    print()
    if (len(susceptibleAgents) == 0): percentRemoved = 1.00
    else: percentRemoved = (removed+(len(newSickAgents)))/numberOfAgents
    percentSurvived = len(susceptibleAgents)/numberOfAgents
    print(format(percentRemoved * 100, ',.0f') + "% of the population was killed by " + nameOfDisease)
    print(format(percentSurvived*100, ',.0f') + "% of the population survived " + nameOfDisease)
    print("At it's peak " + str(biggestWave) + " agents were infected by " + nameOfDisease + " at time " + str(timeOfBiggestWave))
    averageRate = 0
    for x in range(len(changeInInfectionY)):
        averageRate += changeInInfectionY[x]
    averageRate = averageRate/len(changeInInfectionY)
    print("The Average rate of infection is : " + str(averageRate))
    print()
    print(colored("SIMULATION TERMINATED", 'yellow'))
    print("--------------------")
    print()
    plt.plot(survivalDataX, survivalDataY)
    plt.xlabel("Time(t)")
    plt.ylabel("# Susceptible Agents")
    plt.title("Change in Susceptible Population after introduction of " + nameOfDisease )
    plt.axis([0, counter, 0, numberOfAgents])
    plt.show()
    plt.plot(infectedDataX, infectedDataY)
    plt.xlabel("Time(t)")
    plt.ylabel("# Infected Agents")
    plt.title("Change in Infected Population after introduction of " + nameOfDisease)
    plt.axis([0, counter, 0, numberOfAgents])
    plt.show()
    plt.plot(removedDataX, removedDataY)
    plt.xlabel("Time(t)")
    plt.ylabel("# Removed Agents")
    plt.title("Change in Removed Population after introduction of " + nameOfDisease)
    plt.axis([0, counter, 0, numberOfAgents])
    plt.show()
    plt.plot(changeInInfectionX, changeInInfectionY)
    plt.xlabel("Time(t)")
    plt.ylabel("R0")
    plt.title("Change in infection rate over time for " + nameOfDisease)
    maxRate = 0;
    for x in range(len(changeInInfectionY)):
        if (changeInInfectionY[x] > maxRate): maxRate = changeInInfectionY[x]
    plt.axis([0, counter, 0, maxRate])
    plt.show()

    exit = input("Press Any Key to Return to the Main Screen ")





#Help section
def help():
    selection = " "
    while(selection != "q"):
        selection = input("Welcome to the COMP4206 Epidemic Simulator, developed by Ravi Gupta and Shruti Bahl. In this simulator, you can view the spread of infections in an NxN matrix. When you select the run option (2), you will be allowed to enter in the size of the matrix, the number of agents to display, and how many steps the agents should make. The matrix will display and then an agent will be randomly infected. You will then see the matrix after each iteration  so you can track their progress. Press q to return to the menu: ")
    print()


#object definitions
class agent(object):
    def __init__(self,params=None):
        self.id = params
        self.location =  (0, 0)
        self.health = None
        self.timeOfSickness = 0
        self.vaccination = False
    def setAgentLocation(self, x, y):
        locationx = x
        locationy = y
        self.location = (locationx, locationy)
        return self.location
    def setAgentId(self, agentID):
        self.id = agentID
    def getAgentId(self):
        return self.id
    def getLocation(self):
        return self.location
    def getHealth(self):
        return self.health
    def setHealth(self, status):
        self.health = status
    def increaseTimeOfSickness(self):
        self.timeOfSickness += 1
    def getTimeOfSickness(self):
        return self.timeOfSickness
    def setVaccinationStatus(self):
        self.vaccination = True
    def getVaccinationStatus(self):
        return self.vaccination

class SusceptibleAgent(agent):
    def __init__(self,params=None):
        super().__init__()
        self.health = "susceptible"

class InfectedAgent(agent):
    def __init__(self,params=None):
        super().__init__()
        self.health = "infected"

class RemovedAgent(agent):
    def __init__(self,params=None):
        super().__init__()
        self.health = "removed"



#menu
def main():
    selection = 0
    while(selection != 3):
        print("Welcome to The COMP 4206 Epidemic Simulator!")
        print("Menu")
        print("(1) -- Help")
        print("(2) -- Run")
        print("(3) -- Quit")
        print()
        selection = input("Choose a menu option: ")
        while (selection == "q" or selection == "Q"):
            selection = input("Invalid entry. Try again: ")
        selection = int(selection)
        if (selection == 1): help()
        if (selection == 2): runSimulation()
        if (selection == 3): print("Goodbye!")

main()
