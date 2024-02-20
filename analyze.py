import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")
targetAngles = np.load("data/targetAngles.npy")

def plot_sensor_values():
    plt.plot(backLegSensorValues, label="Back Leg", linewidth=2.0)
    plt.plot(frontLegSensorValues, label="Front Leg")
    plt.xlabel("Time")
    plt.ylabel("Sensor Value")
    plt.legend()
    plt.show()

def plot_target_angles():
    plt.plot(targetAngles)
    plt.xlabel("Time")
    plt.ylabel("Target Angle")
    plt.show()

plot_target_angles()
