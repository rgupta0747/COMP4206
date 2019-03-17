import random

def createMatrix(row, col):
    number = 0
    matrix = [[0 for x in range(row)] for y in range(col)]
    for x in range(row):
        for y in range(col):
            matrix[x][y] = number
            number+=1
    return matrix

def isSick(agent):
    if (agent.getHealth() == "infected"):
        return True
    return False

def createAnEdge(agent1, agent2):
    listOfEdges = []
    if (agent1.getLocation() == agent2.getLocation()):
        if (isSick(agent1) & isSick(agent2) == False):
            listOfEdges.append(agent1,agent2)
        if(isSick(agent2) & isSick(agent1) == False):
            listOfedges.append(agent2,agent1)
    return listOfEdges

def becomesSick(agent1, agent2):
    new_agent = None
    if (isSick(agent1)):
        if (agent1.getLocation() == agent2.getLocation()):
            new_agent = InfectedAgent()
            agent2 = new_agent
            return new_agent
    elif (isSick(agent2)):
        if (agent1.getLocation() == agent2.getLocation()):
            new_agent = InfectedAgent()
            agent1 = new_agent
            return new_agent

def createAgentID(size):
    agentList = []
    for x in range(size):
        agentList.append("A" + str(x))
    return agentList

def main():
    rows = columns = 10
    numberOfAgents = 5
    matrix = createMatrix(rows, columns)
    agentIDList = createAgentID(numberOfAgents)
    agentList = []
    for x in range(len(agentIDList)):
        agentList.append(SusceptibleAgent())
        agentList[x].setAgentId(agentIDList[x])
        agentList[x].setAgentLocation(rows, columns)
    agent1 = InfectedAgent()
    agent2 = SusceptibleAgent()
    agent = becomesSick(agent1, agent2)
    # if (agent.getAgentId() == agent1.getAgentId()):
    #     new_agent = InfectedAgent()
    #     agent1 = new_agent
    # if (agent.getAgentId() == agent2.getAgentId()):
    #     new_agent = InfectedAgent()
    #     agent2 = new_agent
    print(agent2.getHealth())

class agent(object):
    def __init__(self,params=None):
        self.id = params
        self.location =  (0, 0)
        self.health = None
    def setAgentLocation(self, row, col):
        locationx = random.randint(0, row)
        locationy = random.randint(0, col)
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
