import random
import time

#creates a square grid that is row x col
def createMatrix(row, col):
    number = 0
    matrix = [[0 for x in range(row)] for y in range(col)]
    for x in range(row):
        for y in range(col):
            matrix[y][x] = number
            number+=1
    return matrix

#determines if the given agent is infected or not
def isSick(agent):
    if (agent.getHealth() == "infected"):
        return True
    return False

#creates an edge between an infected and susceptible agent only if
#one agent is sick and the other is susceptible and they are at the
#same locations. The function adds to edge to the current list of edges
def createAnEdge(agent1, agent2, listOfEdges):
    if (agent1.getLocation() == agent2.getLocation()):
        if (isSick(agent1) & isSick(agent2) == False):
            listOfEdges.append(agent1,agent2)
        if(isSick(agent2) & isSick(agent1) == False):
            listOfedges.append(agent2,agent1)
    return listOfEdges

#determines which agent is sick and returns the agent that is sick
#the susceptible agent becomes infected.
def whichAgentisInfected(agent1, agent2):
    if (isSick(agent1)):
        return "agent2"
    elif (isSick(agent2)):
        return "agent1"

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
    direction = random.randint(1,4)
    if (direction == 1): return "north"
    if (direction == 2): return "east"
    if (direction == 3): return "south"
    if (direction == 4): return "west"


#generates movement of the agent from left to right on the grid based on a given direction
def movesLeftRight(x, direction, rows):
    if (x == 0 and direction == "east"):
        newXLocation = x+1
    elif (x == 0 and direction == "west"):
        newXLocation = x
    elif (x == rows-1 and direction == "west"):
        newXLocation = x-1
    elif (x == rows-1 and direction == "east"):
        newXLocation = x
    else:
        if (direction == "east"):
            newXLocation = x+1
        else:
            newXLocation = x-1
    return newXLocation

#this moves the agent up or down based on a provided direction
def movesUpDown(y, direction, cols):
    if (y == 0 and direction == "south"):
        newYLocation = y+1
    elif (y == 0 and direction == "north"):
        newYLocation = y
    elif (y == cols-1 and direction == "north"):
        newYLocation = y-1
    elif (y == cols-1 and direction == "south"):
        newYLocation = y
    else:
        if (direction == "south"):
            newYLocation = y+1
        else:
            newYLocation = y-1
    return newYLocation

#this adds the agent to the matrix
def addAgentsToMatrix(matrix, agents):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            for z in range(len(agents)):
                if (x == getX(agents[z].getLocation()) and y == getY(agents[z].getLocation())):
                    matrix[y][x] = agents[z].getAgentId()
    return matrix


#This prints out the matrix with the agents's id displayed on the matrix
def displayGrid(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if (isinstance(matrix[y][x], int)): print("- ", end=" ")
            else: print(matrix[y][x], end=" ")
        print()

#This sets the new location of each agent in the agent list based on the direction provided
def setNewLocations(direction, agents, rows, cols):
    for i in range(len(agents)):
        agentLocation = agents[i].getLocation()
        newX = agentLocation[0]
        newY = agentLocation[1]
        if (direction == "east" or direction == "west"):                                    #if direction is east or west, move left/right if possible
            newX = movesLeftRight(newX, direction, rows)
        else:
            newY = movesUpDown(newY, direction, cols)                                       #otherwise move up/down if possible
        agents[i].setAgentLocation(newX, newY)                                              #once new x and y values obtained, set the new agent location
#        print("Agent " + agents[i].getAgentId() + " is at: ", end=" ")
#        print(agents[i].getLocation())
    return agents


def main():
    rows = columns = 10                                                                         #sets the rows and columns
    numberOfAgents = 5                                                                          #sets number of agents in the grid
    matrix = createMatrix(rows, columns)                                                        #creates the grid
    agentIDList = createAgentID(numberOfAgents)                                                 #creates a list of id's for each agent
    agentList = []
    print()
    print("This is where the agents are initially located")
    print()
    for x in range(len(agentIDList)):                                                           #go through agent id's and create agents
        agentList.append(SusceptibleAgent())
        agentList[x].setAgentId(agentIDList[x])                                                 #set id of agent to the agent id from list
        agentList[x].setAgentLocation(generateRandomX(rows),generateRandomY(columns))           #set the location of each agent randomly
#        print("Agent " + agentList[x].getAgentId() + " is at: ", end=" ")                       #prints the agent id and their location
#        print(agentList[x].getLocation())
    print()
    matrix = addAgentsToMatrix(matrix, agentList)
    displayGrid(matrix)                                                                          #prints the matrix with agents on the matrix
    time.sleep(2)
    print()
    for i in range(3):                                                                          #This is the loop that would simulate agents moving
        print("This is the location of agents after " + str(i+1) + " iteration")
        print()
        direction = whichWayToMove()
        agentList = setNewLocations(direction, agentList, rows, columns)
        print()
        matrix = createMatrix(rows, columns)                                                    #reinitialize the grid (a.k.a clear the matrix)
        matrix = addAgentsToMatrix(matrix, agentList)                                           #add agents new positions to the grid
        displayGrid(matrix)                                                                     #print new grid
        print()
        time.sleep(2)

#    agent = whichAgentisInfected(agent1, agent2)
#    if (agent == "agent2"):
#        agent2 = InfectedAgent()
#    print(agent2.getHealth())



class agent(object):
    def __init__(self,params=None):
        self.id = params
        self.location =  (0, 0)
        self.health = None
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


main()
