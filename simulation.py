import random
import time

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
def displayGrid(matrix, agentList):
    listOfSameLocations = locationSame(agentList)
    for x in range(len(listOfSameLocations)):
        locationX = getX(listOfSameLocations[x][0].getLocation())
        locationY = getY(listOfSameLocations[x][0].getLocation())
        matrix[locationX][locationY] = "! "
        print("Agent" + listOfSameLocations[x][0].getAgentId() + " collided with Agent " + listOfSameLocations[x][1].getAgentId())
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if (isinstance(matrix[x][y], int)):
                print("- ", end=" ")
            if (isinstance(matrix[x][y], str)): print(matrix[x][y], end=" ")
        print()

#This sets the new location of each agent in the agent list based on the direction provided
def setNewLocations(direction, agents, rows, cols):
    for i in range(len(agents)):
        agentLocation = agents[i].getLocation()
        oldX = agentLocation[0]
        oldY = agentLocation[1]
        #otherwise move up/down if possible
        #once new x and y values obtained, set the new agent location
        if (direction == "stays"):
            continue
        elif (direction == "east" or direction == "west"):                                    #if direction is east or west, move left/right if possible
            newY = movesLeftRight(oldY, direction, cols)
            agents[i].setAgentLocation(oldX, newY)
        else:
            newX = movesUpDown(oldX, direction, rows)
            agents[i].setAgentLocation(newX, oldY)
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
#    print("This is where the agents are initially located")
    print()
    for x in range(len(agentIDList)):                                                           #go through agent id's and create agents
        agentList.append(SusceptibleAgent())
        agentList[x].setAgentId(agentIDList[x])                                                 #set id of agent to the agent id from list
        agentList[x].setAgentLocation(generateRandomX(rows), generateRandomY(columns))          #set the location of each agent randomly'
        print(agentList[x].getAgentId() + " is at location " + "(" + str(getX(agentList[x].getLocation())) + ", " + str(getY(agentList[x].getLocation())) + ")")
    print()
    for x in range(len(agentList)):
        matrix = addAgentsToMatrix(matrix, agentList[x])
    displayGrid(matrix, agentList)                                                                          #prints the matrix with agents on the matrix
    print()

    for i in range(10):                                                                          #This is the loop that would simulate agents moving
        print("This is the location of agents after " + str(i+1) + " iteration")
        print()
        direction = whichWayToMove()
        agentList = setNewLocations(direction, agentList, rows, columns)
        print()
        for x in range(len(agentList)):
            print("Agent " + agentList[x].getAgentId() + " is at: ", end=" ")                       #prints the agent id and their location
            print(agentList[x].getLocation())
        print()
        matrix = createMatrix(rows, columns)                                                    #reinitialize the grid (a.k.a clear the matrix)
        for x in range(len(agentList)):
            matrix = addAgentsToMatrix(matrix, agentList[x])                                           #add agents new positions to the grid
        displayGrid(matrix, agentList)                                                                     #print new grid
        print()
        time.sleep(1)

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
