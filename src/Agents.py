import mesa as ms
from math import ceil
from Models import *
from random import choice, randrange, random, randint

# TODO / IMPROVEMENTS
# Yellow light
# Priority for waiting cars

class GrassAgent(ms.Agent):
    def __init__(self, id_t, model):
        super().__init__(id_t, model)
        self.id = id_t

class VaccumAgentModel(ms.Agent):
    myCoordinates = (0, 0)
    def __init__(self, id_t, model):
        super().__init__(id_t, model)
        self.id = id_t
        self.state = False

    def move(self):
        next_move = self.model.grid.get_neighborhood(
		    self.pos, moore = True, include_center = False
	    )
        new_position = self.random.choice(next_move)
        self.model.grid.move_agent(self, new_position)
    def step(self):
        pass
"""
{
    "type": 0,
    "direction": ([1, 0] || [0, 1] || [-1, 0] || [0, -1]),
    "velocity" 2 u/s
}
"""

class TrafficLightAgent(ms.Agent):
    first_it = True

    # Data collector variables
    counterStepsBeingGreen = 0
    
    def __init__(self, unique_id, model, lane):
        super().__init__(unique_id, model)
        self.lane = lane    #0 = up, 1 = down, 2 = left, 3 = right
        self.light = 1      #0 = red, 1 = yellow, 2 = green
        self.gracePeriod = 0
        self.localArrival = ()
        self.globalArrivals = {}
        self.tfs = {}
        self.maxGreenTime = 20
        self.greenCounter = 0
        new_pos = (17, 14)
        self.nextArrival = (-1, 100000, -1)

    def setTFS(self, tfs):
        self.tfs = tfs

    def checkCar(self):
        if self.distLeft == 0:
            self.velocity = 0
        elif self.distLeft <= self.velocity:
            self.velocity = ceil(self.velocity/2)

        dx = (self.direction[0] * self.velocity)
        dy = (self.direction[1] * self.velocity)

        newPos = (self.pos[0] + dx, self.pos[1] + dy)
        self.distLeft -= self.velocity
        self.model.grid.move_agent(self, newPos)
    
    def checkLane(self, start, end):
        if self.lane == 0 or self.lane == 1:
            while(start[1] != end[1]):
                #print(f"checking cells {[start, (end[0], start[1])]}")
                current_cells = self.model.grid.get_cell_list_contents([start, (end[0], start[1])])
                car = None
                maxVel = -1
                #print(f"agents in cells: {current_cells}")
                for obj in current_cells:
                    if isinstance(obj, CarAgent) and obj.velocity > maxVel:
                        car = obj
                        maxVel = obj.velocity
                if maxVel != -1:
                    #print(f"returning agent: {car.unique_id}")
                    return car
                if self.lane == 0:
                    start = (start[0], start[1]-1)
                else:
                    start = (start[0], start[1]+1)
            return CarAgent(-1, self.model, -1, 2, [1, 0], 14, None, [0, 0])
        else:
            while(start[0] != end[0]):
                current_cells = self.model.grid.get_cell_list_contents([start, (start[0], end[1])])
                car = None
                maxVel = -1
                for obj in current_cells:
                    if isinstance(obj, CarAgent) and obj.velocity > maxVel:
                        car = obj
                        maxVel = obj.velocity
                if maxVel != -1:
                    return car
                
                if self.lane == 3:
                    start = (start[0]-1, start[1])
                else:
                    start = (start[0]+1, start[1])
            return CarAgent(-1, self.model, -1, 2, [1, 0], 14, None, [0, 0])
            

        """
        if coords_before_crossroad[0] == coords_start_of_street[0]:    # Case horizontal
            it_coords = list(coords_before_crossroad)
            if coords_before_crossroad < coords_start_of_street:
                for i in range(coords_before_crossroad[1], coords_start_of_street[1]):
                    it_coords[1] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
            else:
                for i in reversed(range(coords_start_of_street[1], coords_before_crossroad[1])):
                    it_coords[1] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
        else:
            it_coords = list(coords_before_crossroad)
            if coords_before_crossroad < coords_start_of_street:
                for i in range(coords_before_crossroad[0], coords_start_of_street[0]):
                    it_coords[0] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
            else:
                for i in reversed(range(coords_start_of_street[0], coords_before_crossroad[0])):
                    it_coords[0] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
        return CarAgent(33, self.model, -1, 2, [1, 0], 14, None, [0, 0])
        """

    def checkBacklane(self, start, end):
        if self.lane == 0 or self.lane == 1:
            while(start[1] != end[1]):
                #print(f"checking cells {[start, (end[0], start[1])]}")
                current_cells = self.model.grid.get_cell_list_contents([start, (end[0], start[1])])
                #print(current_cells)
                for obj in current_cells:
                    #print(f"found object {obj.unique_id}")
                    #print(f"nextArrival: {self.nextArrival[0]}")
                    if isinstance(obj, CarAgent) and obj.unique_id == self.nextArrival[0]:
                        #print("Car passed")
                        return True
                if self.lane == 0:
                    start = (start[0], start[1]+1)
                else:
                    start = (start[0], start[1]-1)
            return False
        else:
            while(start[0] != end[0]):
                current_cells = self.model.grid.get_cell_list_contents([start, (start[0], end[1])])
                for obj in current_cells:
                    if isinstance(obj, CarAgent) and obj.unique_id == self.nextArrival[0]:
                        return True
                if self.lane == 3:
                    start = (start[0]+1, start[1])
                else:
                    start = (start[0]-1, start[1])
            return False


    def hasTheCarPassed(self):
        if self.lane == 0:
            return self.checkBacklane((18, 19), (17, 34))
        elif self.lane == 1:
            return self.checkBacklane((15, 14), (16, -1))
        elif self.lane == 2:
            return self.checkBacklane((14, 18), (-1, 17))
        elif self.lane == 3:
            return self.checkBacklane((19, 15), (34, 16))
        else:
            #print(f"not crossed = {self.nextArrival[0]}\tlane {self.lane}")
            return False


    def checkNextCar(self):
        nextCar = CarAgent(-1, self.model, 0, 2, [1, 0], 14, None, [0, 0])
        if self.lane == 0:      # up
            nextCar = self.checkLane((18, 14), (17, -1))
        elif self.lane == 1:    # down
            nextCar = self.checkLane((15, 19), (16, 34))
        elif self.lane == 2:    # left
            nextCar = self.checkLane((19, 18), (34, 17))
        elif self.lane == 3:    # right
            nextCar = self.checkLane((14, 15), (-1, 16))

        #print(f"TFL : {self.unique_id},\tlane: {self.lane},\tvel: {nextCar.velocity},\tCar_id: {nextCar.unique_id}, Position: {nextCar.pos}")
        return nextCar

    def stage_one(self):
        #print("---")
        #print(f"TFL: {self.lane}, STAGE ONE")
        #check if self should still be green
        if self.light == 2:
            if self.hasTheCarPassed() or self.greenCounter == self.maxGreenTime:
                #maybe wait x steps in yellow?
                self.light = 1
                self.greenCounter = 0
            else:
                self.counterStepsBeingGreen += 1
                self.greenCounter += 1
        else:
            self.counterStepsBeingGreen = 0
        
        #change local arrivals
        
        nextCar = self.checkNextCar()
        #print(f"nextCar.type: {nextCar.type}")
        if nextCar.unique_id != -1:
            nextCarSpeed = nextCar.velocity
            if nextCarSpeed == 0:
                nextCarSpeed = 1
            self.nextArrival = (nextCar.unique_id, self.model.schedule.steps + (nextCar.distLeft/nextCarSpeed), self.lane)
        elif self.light != 2:
            self.nextArrival = (-1, 100000, -1)
        
        #print(f"TFL: {self.lane}, nextArrival: {self.nextArrival}")
        # if nextCar.pos == (self.pos[0], self.pos[1])

    def stage_two(self):
        #change global arrivals
        #print("---")
        #print(f"TFL: {self.lane}, STAGE TWO, light: {self.light}")
        greenLane = -1
        maxPriority = -1
        nextGlobalArrival = (-1, 100000, -1)
        for tf in self.tfs:
            if tf.light == 2:
                greenLane = tf.lane
                nextGlobalArrival = tf.nextArrival 
                break
            #print(f"Comparing {tf.nextArrival} to {nextGlobalArrival}")
            if tf.nextArrival[1] < nextGlobalArrival[1]:
                nextGlobalArrival = tf.nextArrival
            
        #print(f"Next global arrival: {nextGlobalArrival}")
        #print(f"greenLane: {greenLane}, nextGlobalArrival: {nextGlobalArrival}, self.lane: {self.lane}")
        # if there's no cars, then nextGlobalArrival[0] == -1
        if nextGlobalArrival[0] == -1:
            self.light = 1

        # if there's no green light, a green light can be chosen based on nextGlobalArrival
        # ideally, we should wait until prior greenlight turns red
        elif self.light == 2 or (greenLane == -1 and nextGlobalArrival[2] == self.lane):
            self.light = 2
            #print(f"CHANGED {self.lane} LIGHT TO {self.light}")
        else:
            self.light = 0
            #print(f"CHANGED {self.lane} LIGHT TO {self.light}")

        #change lights
        #choices = [0, 1, 2]
        #self.light = random.choice(choices)
        
    def stage_three(self):
        pass

class ScheduledTrafficLightAgent(ms.Agent):
    first_it = True
    def __init__(self, unique_id, model, lane, counter):
        super().__init__(unique_id, model)
        self.lane = lane    #0 = up, 1 = down, 2 = left, 3 = right
        self.light = 0      #0 = red, 1 = yellow, 2 = green
        self.counter = counter

    def stage_one(self):
        if self.counter == 25:
            self.counter = 1
        
        if self.counter == 1:
            self.light = 2
        elif self.counter == 4:
            self.light = 1
        elif self.counter == 6:
            self.light = 0
        
        self.counter += 1

    def stage_two(self):
        pass

    def stage_three(self):
        pass

"""
--- CAR AGENT TYPES ---
(0) No special behaviours. Slows at a decent distance from a red/yellow light
(1) Carefull type. Will slow down at a further (semi-random) distance from a red/yellow light.
(2) Unlawful type. Will ignore red lights, and will speed up the closer it is to one.
(3) Lazy type. Will slow down when crossing the intersection.
(4) Drunk type. Will change velocity and even full stop at random.
"""
class CarAgent(ms.Agent):
    def __init__(self, unique_id, model, type, velocity, direction, distLeft, trafficLight, initPos):
        super().__init__(unique_id, model)
        self.type = type
        self.velocity = velocity
        self.desiredVelocity = velocity
        self.direction = direction
        self.distLeft = distLeft #14
        self.vision = 3
        self.initialPos = initPos
        self.TFL = trafficLight
        if self.type == 1: #carefull type
            self.carefullnessMod = randrange(1,4)
        else:
            self.carefullnessMod = 0
        
    def reposition(self):
        self.model.grid.move_agent(self, self.initialPos)
    
    def getDirectionInt(self):
        match self.direction:
            case [0,  1]:
                return 0
            case [0, -1]:
                return 1
            case [-1, 0]:
                return 2
            case [1,  0]:
                return 3
            case _:
                return -1

    def checkTrafficLight(self):
        if self.direction == [1, 0]:
            TFL_cell = self.model.grid.get_cell_list_contents([(14, 14)])
            TFL = [obj for obj in TFL_cell if isinstance(obj, TrafficLightAgent)][0]
            return TFL
        elif self.direction == [0, 1]:
            TFL_cell = self.model.grid.get_cell_list_contents([(17, 14)])
            TFL = [obj for obj in TFL_cell if isinstance(obj, TrafficLightAgent)][0]
            return TFL
        elif self.direction == [-1, 0]:
            TFL_cell = self.model.grid.get_cell_list_contents([(17, 17)])
            TFL = [obj for obj in TFL_cell if isinstance(obj, TrafficLightAgent)][0]
            return TFL
        else: # [0, -1]
            TFL_cell = self.model.grid.get_cell_list_contents([(14, 17)])
            TFL = [obj for obj in TFL_cell if isinstance(obj, TrafficLightAgent)][0]
            return TFL

    def checkCarFront(self, dist_t = -1):
        #print(f"Looking for cars, from car : {self.unique_id}, pos: {self.pos}")
        if dist_t == -1:
            dist_t = self.velocity
        
        if dist_t == 0:
            dist_t = 1

        for i in range(1, dist_t+1):
            #print(f"In distance: {i}")
            currCell = (self.pos[0] + i*self.direction[0], self.pos[1] + i*self.direction[1])
            #print(f"currCell: {currCell}")
            if currCell[0] > 33 or currCell[0] < 0 or currCell[1] > 33 or currCell[1] < 0:
                #print("Off limits")
                break
            CA_cell = self.model.grid.get_cell_list_contents([currCell])
            for obj in CA_cell:
                if isinstance(obj, CarAgent):
                    return i-1
        
        return -1
        """
        if ((self.direction == [1, 0]) and (self.pos[0] < 30)):
            for i in range(dist_t):
                if self.pos[0]+i+1 < 34:
                    CA_cell = self.model.grid.get_cell_list_contents([(self.pos[0]+i+1, self.pos[1])])
                    CA = [obj for obj in CA_cell if isinstance(obj, CarAgent)]
                    if (CA != []):
                        distanceFromCar = True
                return distanceFromCar
        elif ((self.direction == [0, 1]) and (self.pos[1] < 30)):
            for i in range(dist_t):
                if self.pos[1]+i+1 < 34:
                    CA_cell = self.model.grid.get_cell_list_contents([(self.pos[0], self.pos[1]+i+1)])
                    CA = [obj for obj in CA_cell if isinstance(obj, CarAgent)]
                    if (CA != []):
                        distanceFromCar = True
                return distanceFromCar
        elif ((self.direction == [-1, 0]) and (self.pos[0] >= 3)):
            for i in range(dist_t):
                CA_cell = self.model.grid.get_cell_list_contents([(self.pos[0]-i-1, self.pos[1])])
                CA = [obj for obj in CA_cell if isinstance(obj, CarAgent)]
                if (CA != []):
                    distanceFromCar = True
            return distanceFromCar
        elif ((self.direction == [0, -1]) and (self.pos[1] >= 3)): # [0, -1]
            for i in range(dist_t):
                CA_cell = self.model.grid.get_cell_list_contents([(self.pos[0], self.pos[1]-i-1)])
                CA = [obj for obj in CA_cell if isinstance(obj, CarAgent)]
                if (CA != []):
                    distanceFromCar = True
            return distanceFromCar
        else:
            return distanceFromCar
        """


    def move(self):
        # TFL = self.checkTrafficLight()
        distanceFromNextCar = self.checkCarFront()
        # print(f"Car: {self.unique_id}, direction: {self.direction}, type: {self.type}, dist from next car: {distanceFromNextCar}, dist left: {self.distLeft}")
        # print(f"Starting velocity: {self.velocity}")

        if (self.type == 4 and random() < 0.25):
            self.desiredVelocity = randint(1, 4)
        
        if (self.type == 4 and random() < 0.1):
            self.velocity == 0
        elif (distanceFromNextCar != -1 and not (self.distLeft - distanceFromNextCar < 0)):
            # car in front is worth considering
            # print("Car in front is worth considering")
            # print(f"The velocity is: {self.velocity}")
            self.velocity = distanceFromNextCar
            #print(f"New velocity: {self.velocity}")
            """
            if self.velocity <= 2:
                if self.velocity == 2:
                    self.velocity = 1
                else:
                    self.velocity = 0
            else:
                self.velocity = 1"""
        elif (self.distLeft >= 0 and self.distLeft <= self.velocity + self.carefullnessMod and ((self.TFL.light == 0) or (self.TFL.light == 1))):
            #print("At considerable distance from red/yellow light")
            if self.type == 2:
                self.velocity += 1
            else:
                if self.distLeft == 0:
                    self.velocity = 0
                else:
                    self.velocity = ceil(self.velocity/2)
        elif (self.type == 3 and self.distLeft <= self.velocity and self.TFL.light == 2):
            if self.velocity == 0:
                self.velocity = 1
            else:
                self.velocity = ceil(self.velocity/2)
        else:
            if self.velocity < self.desiredVelocity:
                self.velocity += 1
            elif self.velocity > self.desiredVelocity:
                self.velocity -= 1

        # Sprint(f"New velocity: {self.velocity}")
        dx = (self.direction[0] * self.velocity) 
        dy = (self.direction[1] * self.velocity)

        prevDistLeft = self.distLeft
        self.distLeft -= self.velocity
        # print(f"prev pos: {self.pos}")
        newPos = (self.pos[0] + dx, self.pos[1] + dy)
        self.model.grid.move_agent(self, newPos)

        if prevDistLeft >= 0 and self.distLeft < 0:
            self.model.servicedCars += 1

        if self.distLeft < -17:
            if self.direction == [0, 1]:    # up
                self.distLeft = self.TFL.pos[1] - self.pos[1]
            elif self.direction == [0, -1]: # down
                self.distLeft = self.pos[1] - self.TFL.pos[1]
            elif self.direction == [-1, 0]: # left
                self.distLeft = self.pos[0] - self.TFL.pos[0]
            else:                           # right
                self.distLeft = self.TFL.pos[0] - self.pos[0]      

            # and change velocity
            self.velocity = choice([1, 2, 3, 4])          

        # print(f"distLeft: {self.distLeft}")
        

    def stage_one(self):
        # check for crashes
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        carList = [obj for obj in cellmates if isinstance(obj, CarAgent) and obj != self]
        # print(f"len: {len(carList)}")
        if len(carList) > 0:
            for car in carList:
                car.reposition()
            self.model.reportedCrashes += 1
            self.reposition()
        pass
    def stage_two(self):
        #print("stage_two")
        pass
    def stage_three(self):
        #print("stage_three")
        
        #print(f"id: {self.TFL.unique_id},\tlight: {self.TFL.light},\tagent_position: {self.pos}")
        self.move()