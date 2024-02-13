import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")

plt.plot(backLegSensorValues, label="Back Leg", linewidth=2.0)
plt.plot(frontLegSensorValues, label="Front Leg")
plt.xlabel("Time")
plt.ylabel("Sensor Value")
plt.legend()

plt.show()
