from flask import Flask, request, jsonify
import os

# Flask code
app	= Flask("CrossRoadSimulation", static_url_path="")
port	= int(os.getenv("PORT", 8000))

# JSON car position structure
getCarPosition	= lambda carObject	: {"carId"	: str(  carObject.carId),
					   "x"		: float(carObject.x),
					   "y"		: float(carObject.y),
					   "z"		: float(carObject.z)}

getCarPositions	= lambda carObjects : jsonify({"positions":[getCarPosition(obj) for obj in carObjects]})

# Example car class
class TheCar:
	def __init__(self, carId_t, x_t, y_t, z_t):
		self.carId	= carId_t
		self.x		= x_t
		self.y		= y_t
		self.z		= z_t

# Method for initializing the simulation
@app.route("/init", methods=["POST", "GET"])
def startingConfiguration():
	cobs = []
	if request.method == "GET":
		# Initialize the simulation and send initial positions
		for i in range(0, 10):
			cobs.append(TheCar(i, i, i, i))
		cars = getCarPositions(cobs)
		return cars
	elif request.method == "POST":
		return "Use get method"
		

# Server start
if __name__=='__main__':
	app.run(host="0.0.0.0", port=port, debug=True)
