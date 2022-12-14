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
    def __init__(self, nCars, smartTLs, typesChance = 0.06, stepsToIncrement = 0):
        super().__init__()
        #self.schedule = ms.time.BaseScheduler(self)
        self.model_stages = ["stage_one", "stage_two", "stage_three"]
        self.schedule = ms.time.StagedActivation(self, self.model_stages, shuffle=False)

        self.servicedCars = 0
        self.reportedCrashes = 0

        self.grid = ms.space.MultiGrid(34, 34, torus=True)
        self.stepsToIncrement = stepsToIncrement
        self.directions = [
            [1,0],
            [0,1],
            [-1,0],
            [0,-1],
        ]
        self.velocities = [1]
        self.typesChance = typesChance
        if smartTLs:
            # adding traffic light agents to grid
            TFS_0 =   TrafficLightAgent(0, self, 0)
            TFS_1 =   TrafficLightAgent(1, self, 1)
            TFS_2 =   TrafficLightAgent(2, self, 2)
            TFS_3 =   TrafficLightAgent(3, self, 3)

            # connecting traffic light agents to each other
            self.TFS_list = [TFS_0, TFS_1, TFS_2, TFS_3]
            for tf in self.TFS_list:
                tf.setTFS(self.TFS_list)
        else:
            TFS_0 =   ScheduledTrafficLightAgent(0, self, 0, 1)
            TFS_1 =   ScheduledTrafficLightAgent(1, self, 1, 7)
            TFS_2 =   ScheduledTrafficLightAgent(2, self, 2, 13)
            TFS_3 =   ScheduledTrafficLightAgent(3, self, 3, 19)
            self.TFS_list = [TFS_0, TFS_1, TFS_2, TFS_3]

        #for TFL in TFS:self.schedule.add(TFL)
        self.schedule.add(TFS_0)
        self.grid.place_agent(TFS_0, (19, 14))   #up
        self.schedule.add(TFS_1)
        self.grid.place_agent(TFS_1, (14, 19))   #down
        self.schedule.add(TFS_2)
        self.grid.place_agent(TFS_2, (19, 19))   #left
        self.schedule.add(TFS_3)
        self.grid.place_agent(TFS_3, (14, 14))   #right

        self.carsInLane = [0, 0, 0, 0]
        self.counter = 4

        for i in range(nCars):
            direction = choice(self.directions)
            #direction = self.directions[i]
           
            #up - down - left - right
            distLeft = 14
            if direction[0] == 0:
                if direction[1] == 1: #going up
                    startingPos = (choice([17, 18]), 0 + self.carsInLane[0])
                    distLeft -= self.carsInLane[0]
                    self.carsInLane[0] += 1
                    trafficLight = TFS_0
                else: #going down
                    startingPos = (choice([15, 16]), 33 - self.carsInLane[1])
                    distLeft -= self.carsInLane[1]
                    self.carsInLane[1] += 1
                    trafficLight = TFS_1
            elif direction[0] == -1: #going left
                startingPos = (33 - self.carsInLane[2], choice([17, 18]))
                distLeft -= self.carsInLane[2]
                self.carsInLane[2] += 1
                trafficLight = TFS_2
            else: #going right
                startingPos = (0 + self.carsInLane[3], choice([15, 16]))
                distLeft -= self.carsInLane[3]
                self.carsInLane[3] += 1
                trafficLight = TFS_3

            typeRes = random()
            if typeRes < typesChance:
                carType = 1
            elif typeRes < typesChance*2:
                carType = 2
            elif typeRes < typesChance*3:
                carType = 3
            elif typeRes < typesChance*4:
                carType = 4
            else:
                carType = 0
            
            carro = CarAgent(self.counter, self, carType, choice(self.velocities), direction, distLeft, trafficLight, startingPos)
            self.schedule.add(carro)
            self.grid.place_agent(carro, startingPos)
            self.counter += 1
        
        """
        carro = CarAgent(self.counter, self, 0, 3, [0, 1], 12, TFS_0, (17, 2))
        self.schedule.add(carro)
        self.grid.place_agent(carro, (17, 2))
        self.counter += 1
        carro = CarAgent(self.counter, self, 0, 3, [0, 1], 11, TFS_0, (17, 3))
        self.schedule.add(carro)
        self.grid.place_agent(carro, (17, 3))
        self.counter += 1
        carro = CarAgent(self.counter, self, 0, 3, [-1, 0], 6, TFS_2, (25, 17))
        self.schedule.add(carro)
        self.grid.place_agent(carro, (25, 17))
        self.counter += 1
        carro = CarAgent(self.counter, self, 0, 2, [-1, 0], 6, TFS_2, (25, 18))
        self.schedule.add(carro)
        self.grid.place_agent(carro, (25, 18))
        self.counter += 1
        carro = CarAgent(self.counter, self, 0, 2, [-1, 0], 6, TFS_2, (27, 17))
        self.schedule.add(carro)
        self.grid.place_agent(carro, (27, 17))
        self.counter += 1
        """
        
        for x in range(34):
            for y in range(34):
                pasto = GrassAgent(0, self)
                if (x >= 0 and x < 15) and ((y >= 0 and y < 15) or y>=19 and y < 34):
                    self.grid.place_agent(pasto, (x, y))
                elif (x >= 19 and x < 232) and ((y>=0 and y < 15) or y>= 19 and y < 34):
                    self.grid.place_agent(pasto, (x, y))
                
        
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
			model (CrossroadModel): simulation model
			
		Returns:
			int: Num of wealthy agents"""

        return sum([1 for agent in model.schedule.agents if agent.id == 0])
    


    def step(self):
        #print("=================")
        self.datacollector.collect(self)
        self.schedule.step()
        if (self.stepsToIncrement > 0 and self.schedule.steps%self.stepsToIncrement == 0):
            # add a new car
            direction = choice(self.directions)
            #direction = self.directions[i]
           
            #up - down - left - right
            distLeft = 14
            if direction[0] == 0:
                if direction[1] == 1: #going up
                    startingPos = (choice([17, 18]), 0 + self.carsInLane[0])
                    distLeft -= self.carsInLane[0]
                    self.carsInLane[0] += 1
                    trafficLight = self.TFS_list[0]
                else: #going down
                    startingPos = (choice([15, 16]), 33 - self.carsInLane[1])
                    distLeft -= self.carsInLane[1]
                    self.carsInLane[1] += 1
                    trafficLight = self.TFS_list[1]
            elif direction[0] == -1: #going left
                startingPos = (33 - self.carsInLane[2], choice([17, 18]))
                distLeft -= self.carsInLane[2]
                self.carsInLane[2] += 1
                trafficLight = self.TFS_list[2]
            else: #going right
                startingPos = (0 + self.carsInLane[3], choice([15, 16]))
                distLeft -= self.carsInLane[3]
                self.carsInLane[3] += 1
                trafficLight = self.TFS_list[3]

            typeRes = random()
            if typeRes < self.typesChance:
                carType = 1
            elif typeRes < self.typesChance*2:
                carType = 2
            elif typeRes < self.typesChance*3:
                carType = 3
            elif typeRes < self.typesChance*4:
                carType = 4
            else:
                carType = 0
            
            carro = CarAgent(self.counter, self, carType, choice(self.velocities), direction, distLeft, trafficLight, startingPos)
            self.schedule.add(carro)
            self.grid.place_agent(carro, startingPos)
            self.counter += 1


