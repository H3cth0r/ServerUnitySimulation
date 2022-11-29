import mesa as ms
from Models import *
from Agents import *
import pandas as pd
import matplotlib.pyplot as plt

params = {"nCars":4, "typesChance": 0.06, "smartTLs":True, "stepsToIncrement":30}
results = ms.batch_run(
    CrossroadModel,
    parameters=params,
    iterations=50,
    max_steps=300,
    number_processes=1,
    data_collection_period=1,
    display_progress=False)


# valor esperado o esperanza matemática
df = pd.DataFrame(results)
df.set_index("Step", inplace=True)

"""
df.groupby("iteration")["Deactivated Robots"].plot(legend=False, ylabel="Deactivated robots")
plt.show()
"""

"""
datacollector variables:
ServicedCars
CarsStuckInTraffic
ReportedCrashes
"""

served_df = pd.DataFrame()
traffic_df = pd.DataFrame()
crashes_df = pd.DataFrame()
for name, group in df.groupby('iteration'):
    served = group[["ServicedCars"]]
    served.rename({'ServicedCars':('SC' + str(name+1))})
    served_df = pd.concat([served_df, served], axis=1)

    traffic = group[["CarsStuckInTraffic"]]
    traffic.rename({'CarsStuckInTraffic':('CT' + str(name+1))})
    traffic_df = pd.concat([traffic_df, traffic], axis=1)
    
    crashes = group[["ReportedCrashes"]]
    crashes.rename({'ReportedCrashes':('RC' + str(name+1))})
    crashes_df = pd.concat([crashes_df, crashes], axis=1)

"""--- CARROS ATENDIDOS ---"""
df.groupby("iteration")["ServicedCars"].plot(legend=False, xlabel = "Pasos (Steps)", ylabel="Carros Atendidos")
plt.savefig('static/resources/batch/smart/ServicedCars.png')
plt.show()

# valor esperado
served_df.mean(axis=1).plot(ylabel="Carros Atendidos")
plt.savefig('static/resources/batch/smart/ServicedCars_mean.png')
plt.show()

served_mean = served_df.iloc[-1].mean()
print(f"Promedio de carros atendidos: {served_mean}")

"""--- CARROS PARADOS EN TRÁFICO ---"""
df.groupby("iteration")["CarsStuckInTraffic"].plot(legend=False, xlabel = "Pasos (Steps)", ylabel="Carros parados en tráfico")
plt.savefig('static/resources/batch/smart/CarsStuckInTraffic.png')
plt.show()

# valor esperado
traffic_df.mean(axis=1).plot(ylabel="Carros parados en tráfico")
plt.savefig('static/resources/batch/smart/CarsStuckInTraffic_mean.png')
plt.show()

traffic_mean = df.groupby("iteration")["CarsStuckInTraffic"].mean().mean()
print(f"Promedio de carros parados en tráfico: {traffic_mean}")

"""--- CHOQUES REPORTADOS ---"""
df.groupby("iteration")["ReportedCrashes"].plot(legend=False, xlabel = "Pasos (Steps)", ylabel="Choques reportados")
plt.savefig('static/resources/batch/smart/ReportedCrashes.png')
plt.show()

# valor esperado
crashes_df.mean(axis=1).plot(ylabel="Choques reportados")
plt.savefig('static/resources/batch/smart/ReportedCrashes_mean.png')
plt.show()

crashes_mean = df.groupby("iteration")["ReportedCrashes"].mean().mean()
print(f"Promedio de choques reportados: {crashes_mean}")

"""--- SCHEDULED TRAFFIC LIGHTS ---"""
params = {"nCars":4, "typesChance": 0.06, "smartTLs":False, "stepsToIncrement":30}
results = ms.batch_run(
    CrossroadModel,
    parameters=params,
    iterations=50,
    max_steps=300,
    number_processes=1,
    data_collection_period=1,
    display_progress=False)


# valor esperado o esperanza matemática
df = pd.DataFrame(results)
df.set_index("Step", inplace=True)

"""
df.groupby("iteration")["Deactivated Robots"].plot(legend=False, ylabel="Deactivated robots")
plt.show()
"""

"""
datacollector variables:
ServicedCars
CarsStuckInTraffic
ReportedCrashes
"""

served_df = pd.DataFrame()
traffic_df = pd.DataFrame()
crashes_df = pd.DataFrame()
for name, group in df.groupby('iteration'):
    served = group[["ServicedCars"]]
    served.rename({'ServicedCars':('SC' + str(name+1))})
    served_df = pd.concat([served_df, served], axis=1)

    traffic = group[["CarsStuckInTraffic"]]
    traffic.rename({'CarsStuckInTraffic':('CT' + str(name+1))})
    traffic_df = pd.concat([traffic_df, traffic], axis=1)
    
    crashes = group[["ReportedCrashes"]]
    crashes.rename({'ReportedCrashes':('RC' + str(name+1))})
    crashes_df = pd.concat([crashes_df, crashes], axis=1)

"""--- CARROS ATENDIDOS ---"""
df.groupby("iteration")["ServicedCars"].plot(legend=False, xlabel = "Pasos (Steps)", ylabel="Carros Atendidos")
plt.savefig('static/resources/batch/scheduled/ServicedCars.png')
plt.show()

# valor esperado
served_df.mean(axis=1).plot(ylabel="Carros Atendidos")
plt.savefig('static/resources/batch/scheduled/ServicedCars_mean.png')
plt.show()

served_mean = served_df.iloc[-1].mean()
print(f"Promedio de carros atendidos: {served_mean}")

"""--- CARROS PARADOS EN TRÁFICO ---"""
df.groupby("iteration")["CarsStuckInTraffic"].plot(legend=False, xlabel = "Pasos (Steps)", ylabel="Carros parados en tráfico")
plt.savefig('static/resources/batch/scheduled/CarsStuckInTraffic.png')
plt.show()

# valor esperado
traffic_df.mean(axis=1).plot(ylabel="Carros parados en tráfico")
plt.savefig('static/resources/batch/scheduled/CarsStuckInTraffic_mean.png')
plt.show()

traffic_mean = df.groupby("iteration")["CarsStuckInTraffic"].mean().mean()
print(f"Promedio de carros parados en tráfico: {traffic_mean}")

"""--- CHOQUES REPORTADOS ---"""
df.groupby("iteration")["ReportedCrashes"].plot(legend=False, xlabel = "Pasos (Steps)", ylabel="Choques reportados")
plt.savefig('static/resources/batch/scheduled/ReportedCrashes.png')
plt.show()

# valor esperado
crashes_df.mean(axis=1).plot(ylabel="Choques reportados")
plt.savefig('static/resources/batch/scheduled/ReportedCrashes_mean.png')
plt.show()

crashes_mean = df.groupby("iteration")["ReportedCrashes"].mean().mean()
print(f"Promedio de choques reportados: {crashes_mean}")