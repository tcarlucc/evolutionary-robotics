import constants as c
from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim


class ROBOT:
    def __init__(self):
        self.sensors = {}
        self.motors = {}
        self.values = []
        self.Prepare_To_Sense()


    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)


    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)
            self.values = self.sensors[sensor].values
            if(t == c.ITERATIONS-1):
                print(self.values)

