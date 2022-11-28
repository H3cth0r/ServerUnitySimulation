import mesa as ms
from Agents import GrassAgent, TrafficLightAgent, ScheduledTrafficLightAgent, CarAgent
from random import choice, random
from math import floor

def numberOfStepsATrafficLichtIsRed(model) :
    return [agent.counterStepsBeingGreen for agent in model.schedule.agents if type(agent)==TrafficLightAgent and  agent.counterStepsBeingGreen > 0]

def getLightStatusOfEachLane(model):
    return [agent.light for agent in model.schedule.agents if type(agent) == TrafficLightAgent]

def getDesiredVelocities(model):
    return [agent.desiredVelocity for agent in model.schedule.agents if type(agent) == CarAgent]

def getCarsVelocities(model):
    return [agent.velocity for agent in model.schedule.agents if type(agent) == CarAgent]

def getCarsDirections(model):
    return [agent.direction for agent in model.schedule.agents if type(agent) == CarAgent]

def getNumberOfCarsInEachLane(model):
    return model.carsInLane

def getServicedCars(model):
    return model.servicedCars

def getReportedCrashes(model):
    return model.reportedCrashes

def getCarsStuckInTraffic(model):
    return sum([1 for agent in model.schedule.agents if isinstance(agent, CarAgent) and agent.velocity == 0])

class CrossroadModel(ms.Model):
    def __init__(self, nCars, types, smartTLs):
        super().__init__()
        #self.schedule = ms.time.BaseScheduler(self)
        self.model_stages = ["stage_one", "stage_two", "stage_three"]
        self.schedule = ms.time.StagedActivation(self, self.model_stages, shuffle=False)
        
        self.servicedCars = 0
        self.reportedCrashes = 0

        self.grid = ms.space.MultiGrid(32, 32, torus=True)
        self.directions = [
            [1,0],
            [0,1],
            [-1,0],
            [0,-1],
        ]
        self.velocities = [1]
        self.nTypes = {"t2":floor(types["t2"]*nCars)}
        if smartTLs:
            # adding traffic light agents to grid
            TFS_0 =   TrafficLightAgent(0, self, 0)
            TFS_1 =   TrafficLightAgent(1, self, 1)
            TFS_2 =   TrafficLightAgent(2, self, 2)
            TFS_3 =   TrafficLightAgent(3, self, 3)

            # connecting traffic light agents to each other
            TFS_list = [TFS_0, TFS_1, TFS_2, TFS_3]
            for tf in TFS_list:
                tf.setTFS(TFS_list)
        else:
            TFS_0 =   ScheduledTrafficLightAgent(0, self, 0, 1)
            TFS_1 =   ScheduledTrafficLightAgent(1, self, 1, 7)
            TFS_2 =   ScheduledTrafficLightAgent(2, self, 2, 13)
            TFS_3 =   ScheduledTrafficLightAgent(3, self, 3, 19)

        #for TFL in TFS:self.schedule.add(TFL)
        self.schedule.add(TFS_0)
        self.grid.place_agent(TFS_0, (17, 14))   #up
        self.schedule.add(TFS_1)
        self.grid.place_agent(TFS_1, (14, 17))   #down
        self.schedule.add(TFS_2)
        self.grid.place_agent(TFS_2, (17, 17))   #left
        self.schedule.add(TFS_3)
        self.grid.place_agent(TFS_3, (14, 14))   #right

        self.carsInLane = [0, 0, 0, 0]
        self.counter = 4

        for i in range(nCars):
            #direction = choice(self.directions)
            direction = self.directions[i]
           
            #up - down - left - right
            distLeft = 14
            if direction[0] == 0:
                if direction[1] == 1: #going up
                    startingPos = (16, 0 + self.carsInLane[0])
                    distLeft -= self.carsInLane[0]
                    self.carsInLane[0] += 1
                    trafficLight = TFS_0
                else: #going down
                    startingPos = (15, 31 - self.carsInLane[1])
                    distLeft -= self.carsInLane[1]
                    self.carsInLane[1] += 1
                    trafficLight = TFS_1
            elif direction[0] == -1: #going left
                startingPos = (31 - self.carsInLane[2], 16)
                distLeft -= self.carsInLane[2]
                self.carsInLane[2] += 1
                trafficLight = TFS_2
            else: #going right
                startingPos = (0 + self.carsInLane[3], 15)
                distLeft -= self.carsInLane[3]
                self.carsInLane[3] += 1
                trafficLight = TFS_3

            if self.nTypes["t2"] > 0:
                carType = 2
                self.nTypes["t2"] -= 1
            else:
                carType = 0
            
            carro = CarAgent(self.counter, self, carType, choice(self.velocities), direction, distLeft, trafficLight, startingPos)
            self.schedule.add(carro)
            self.grid.place_agent(carro, startingPos)
            self.counter += 1

        for x in range(32):
            for y in range(32):
                pasto = GrassAgent(self.counter, self)
                if (x >= 0 and x < 15) and ((y >= 0 and y < 15) or y>=17 and y < 32):
                    self.grid.place_agent(pasto, (x, y))
                elif (x >= 17 and x < 232) and ((y>=0 and y < 15) or y>= 17 and y < 32):
                    self.grid.place_agent(pasto, (x, y))
                self.counter += 1
        
        self.datacollector = ms.DataCollector(
            model_reporters={
                             "MaxStepsBeingGreen" : numberOfStepsATrafficLichtIsRed,
                             "StatusTFLs"         : getLightStatusOfEachLane,
                             "AgentsVelocities"   : getCarsVelocities,
                             "CarsDirections"     : getCarsDirections,
                             "DesiredVelocities"  : getDesiredVelocities,
                             "NumberOfCarsPerLane": getNumberOfCarsInEachLane,
                             "ServicedCars": getServicedCars,
                             "ReportedCrashes": getReportedCrashes,
                             "CarsStuckInTraffic": getCarsStuckInTraffic}
        ) 

    @staticmethod
    def current_non_weathy_agents(model) -> int:
        """Return the total of number of weathy agents
		
		Args:
			model (CrossroadModel): tee simulation model
			
		Returns:
			int: Num of wealthy agents"""

        return sum([1 for agent in model.schedule.agents if agent.id == 0])
    


    def step(self):
        #print("=================")
        self.datacollector.collect(self)
        self.schedule.step()

