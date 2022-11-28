import mesa as ms
from Models import *
from Agents import *
import matplotlib.pyplot as plt

def agent_PT(agent):
	if type(agent) == GrassAgent:
		PT = {"Shape": "rect","Color": "green","Filled": "true","Layer": 0,"w": 1,"h":1}
	elif type(agent) == TrafficLightAgent or isinstance(agent, ScheduledTrafficLightAgent):
		if agent.light == 0:
			PT = {"Shape": "circle","Color": "red","Filled": "true","Layer": 1,"r" : 0.5}
		elif agent.light == 1:
			PT = {"Shape": "circle","Color": "yellow","Filled": "true","Layer": 1,"r" : 0.5}
		else:
			PT = {"Shape": "circle","Color": "white","Filled": "true","Layer": 1,"r" : 0.5}
	else:
		PT = {"Shape": "rect", "Color": "red", "Filled": "true", "Layer": 1, "w": 1, "h":1}
		
	return PT

grid = ms.visualization.CanvasGrid(agent_PT, 32, 32, 700, 700)

chartRC = ms.visualization.ChartModule(
	[
		{
			"Label": "ReportedCrashes",
			"Color": "Red"
		}
	],
	canvas_height=200,
	data_collector_name="datacollector"
)

chartSC = ms.visualization.ChartModule(
	[
		{
			"Label": "ServicedCars",
			"Color": "Blue"
		}
	],
	canvas_height=200,
	data_collector_name="datacollector"
)

chartCSIT = ms.visualization.ChartModule(
	[
		{
			"Label": "CarsStuckInTraffic",
			"Color": "Orange"
		}
	],
	canvas_height=200,
	data_collector_name="datacollector"
)

server = ms.visualization.ModularServer(RoomModel, [grid, chartRC, chartSC, chartCSIT], "Vacuum Room Model", {"nCars":4, "t2":0.25, "smartTLs":False})
server.port = 8521
server.launch()

