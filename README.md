# COMP4206
COMP4206 Project

This is a simple simulation written in Python that creates a grid and adds agents to the grid. It then simulates the movement of agents on the grid.

The simulation infects a random agent on the grid and then simulates the spread of the infection throughout all agents on the grid. 

Once an agent is infected, if it happens to land on the same spot of an uninfected but susceptible agent, then the infected agent transmits the disease to the susceptible agent. 

User can set how big of a square matrix (recommended size between 10x10 and 30x30), how many agents to place on the board, how long should the simulation run for, and how quickly does the infection kill the agent. 

User can track stats as the simulation progresses. 

**NOTE: You must run this in Python3 as the code is developed in Python3. Also, to view the grid and results, you will need to enable termcolor (pip3 install termcolor). 

Upcoming will be introducing vaccines in some agents to see how the infection is halted over time. 
