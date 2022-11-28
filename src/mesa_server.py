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

grid = ms.visualization.CanvasGrid(agent_PT, 34, 34, 700, 700)

chart_currents = ms.visualization.ChartModule(
	[

	],
	canvas_height=300,
	data_collector_name="datacollector"
)

server = ms.visualization.ModularServer(CrossroadModel, [grid, chart_currents], "Crossroad Model", {"nCars":4, "types": {"t2":0.34}, "smartTLs":True})
server.port = 8521
server.launch()

