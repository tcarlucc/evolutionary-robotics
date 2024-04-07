import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p



class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.linkIndex = pyrosim.linkNamesToIndices[linkName]
        self.values = np.zeros(c.ITERATIONS)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Set_Value(self, t, value):
        self.values[t] = value

    def Save_Values(self):
        np.save("data/sensorValues.npy", self.values)