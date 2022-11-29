from flask import Flask, request, jsonify, render_template
import os
import mesa as ms
from Models import *
from Agents import *
import pandas as pd
import matplotlib.pyplot as plt

# Flask code
app	= Flask("CrossRoadSimulation", static_url_path="")
port	= int(os.getenv("PORT", 8000))

# Mesa model
model = CrossroadModel(nCars = 4, typesChance = 0.06, smartTLs = True, stepsToIncrement = 30)

# JSON car position structure
getCarData = lambda carObject	: {"carId"	: str(carObject.unique_id),
					   "x"		: float(carObject.pos[0]),
					   "y"		: float(carObject.pos[1]),
					   "dir"	: carObject.getDirectionInt()}

getTFLData = lambda TFLObject	: {"tflId"	: str(TFLObject.unique_id),
					   "light"	: TFLObject.light}

getStepData	= lambda m : jsonify({
		"step":m.schedule.steps,
		"cars":[getCarData(agent) for agent in m.schedule.agents if isinstance(agent, CarAgent)],
		"tfls":[getTFLData(agent) for agent in m.schedule.agents if isinstance(agent, TrafficLightAgent) or isinstance(agent, ScheduledTrafficLightAgent)]})

# Method for initializing the simulation
@app.route("/init", methods=["POST", "GET"])
def startingConfiguration():
	model.step()
	if request.method == "GET":
		print([getTFLData(agent) for agent in model.schedule.agents if isinstance(agent, TrafficLightAgent)])
		return getStepData(model)
	elif request.method == "POST":
		return "Use get method"
	
# Method for getting a step
@app.route("/step", methods=["POST", "GET"])
def getStep():
	model.step()
	if request.method == "GET":
		return getStepData(model)
	elif request.method == "POST":
		return "Use get method"

# Showing the plot
@app.route("/charts", methods=["GET"])
def showCharts():
	df = model.datacollector.get_model_vars_dataframe()
	df[["ServicedCars"]].plot()
	plt.savefig('static/resources/ServicedCars.png')
	df[["CarsStuckInTraffic"]].plot()
	plt.savefig('static/resources/CarsStuckInTraffic.png')
	return render_template("charts.html")

# Server start
if __name__=='__main__':
	app.run(host="0.0.0.0", port=port, debug=True)
