import random
import time
from termcolor import colored

#creates a square grid that is row x col
def createMatrix(row, col):
    number = 0
    matrix = [[0 for x in range(row)] for y in range(col)]
    for x in range(row):
        for y in range(col):
            matrix[x][y] = number
            number+=1
    return matrix

#determines if the given agent is infected or not
def isSick(agent):
    if (agent.getHealth() == "infected"):
        return True
    return False


#determines which agent is sick and returns the agent that is sick
def whichAgentisInfected(agent1, agent2):
    if (isSick(agent1)):
        return "agent1"
    elif (isSick(agent2)):
        return "agent2"
    else: return "none"

#creates a list of id's for all the agents in the simulation
def createAgentID(size):
    agentList = []
    for x in range(size):
        agentList.append("A" + str(x))
    return agentList

#create a random X location on the grid to initially place the agent
def generateRandomX(row):
    return random.randint(0,row-1)

#create a random Y location on the grid to initially place the agent
def generateRandomY(col):
    return random.randint(0,col-1)

#gets the x of the location
def getX(location):
    return location[0]

#gets y of the location
def getY(location):
    return location[1]

#determines the direction the agent will move
def whichWayToMove():
    direction = random.randint(1,5)
    if (direction == 1): return "north"
    if (direction == 2): return "east"
    if (direction == 3): return "south"
    if (direction == 4): return "west"
    if (direction == 5): return "stays"


#generates movement of the agent from left to right on the grid based on a given direction
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

#this moves the agent up or down based on a provided direction
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

#this adds the agent to the matrix
def addAgentsToMatrix(matrix, agent):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
                if (x == getX(agent.getLocation()) and y == getY(agent.getLocation())):
                    matrix[x][y] = agent.getAgentId()
    return matrix

#checks if the two agents are at the same location and adds them to a list as a tuple
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

#This prints out the matrix with the agents's id displayed on the matrix
#First it determines where the collisions occur and replaces the locations
#in the matrix that collided with !
#Then it goes through the matrix and if their is no id at the location, prints -
#If there is an ID, then it determines if that id is healthy or sick and prints the
#id or id with an * if it is sick.
#Print is done to ensure spacing is satisfied.
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

#This checks the health of the agent ID in the agent list
def getHealth(id, list):
    for x in range(len(list)):
        if (id == list[x].getAgentId()): return list[x].getHealth()

#determines the index of the agent id in the list
def locationInList(id, list):
    for x in range(len(list)):
        if (id == list[x].getAgentId()): return x


#This sets the new location of each agent in the agent list based on the direction provided
def setNewLocations(direction, agent, rows, cols):
    agentLocation = agent.getLocation()
    oldX = agentLocation[0]
    oldY = agentLocation[1]
    #once x and y values obtained, set the new agent location
    #if direction is stays don't move agent
    if (direction == "stays"):
        return agent
    elif (direction == "east" or direction == "west"):                                    #if direction is east or west, move left/right if possible
        newY = movesLeftRight(oldY, direction, cols)
        agent.setAgentLocation(oldX, newY)
    #otherwise move the agent north south
    else:
        newX = movesUpDown(oldX, direction, rows)
        agent.setAgentLocation(newX, oldY)
    return agent


#creates an infected agent
def createAgent(agent, type):
    originalLocation = agent.getLocation()
    originalId = agent.getAgentId()
    if (type == "infected"): agent = InfectedAgent()
    if (type == "removed"): agent = RemovedAgent()
    agent = InfectedAgent()
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
                    #go through the list of agents and figure out which agent in the list is infected and make that agent infected
                    for y in range(len(agentList)):
                        if (listOfCollisions[x][1].getAgentId() == agentList[y].getAgentId()):
                            agentList[y] = createAgent(agentList[y], "infected")
                #if the second agent was sick and first was not (a.ka. susceptible) then make the first agent in the collision infected
                elif (agent == "agent2" and not isSick(listOfCollisions[x][0])):
                    #go through the list of agents and figure out which agent in the list is infected and make that agent infected
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
            print("The number of Removed Agents is : " + str(numberOfAgents - len(susceptibleAgents) - len(newSickAgents)))
        else: print("The number of Removed Agents is : " + str(len(removedAgents)))
#        print("The infected agents are: ")
#        print(colored("--------------------------------------------------------", 'red'))
#        print("Agent ID\t\t\tTime Remaining before Death")
#        for x in range(len(newSickAgents)):
#            print(newSickAgents[x].getAgentId() + "\t\t\t\t\t" + str(newSickAgents[x].getTimeOfSickness()))
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
        print("Number of Removed : \t\t\t" + str(numberOfAgents - len(susceptibleAgents) - len(newSickAgents)))
    else: print("Number of Removed : \t\t\t" + str(len(removedAgents)))
    print()
    print(colored("SIMULATION TERMINATED", 'yellow'))
    print("--------------------")
    print()





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
        selection = int(selection)
        if (selection == 1): help()
        if (selection == 2): runSimulation()
        if (selection == 3): print("Goodbye!")
        if(isinstance(selection, str)): selection = input("Not a valid option. Enter selection: ")

main()
