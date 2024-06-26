import constants as c
from sensor import SENSOR
from motor import MOTOR
import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import random


class ROBOT:
    def __init__(self, solutionID):
        self.sensors = {}
        self.motors = {}
        self.solutionID = solutionID
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf", self.robotId)
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system(f"del brain{solutionID}.nndf")
        self.angularDisplacement = 0

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for linkName in self.sensors:
            self.sensors[linkName].Set_Value(t, 1)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.neurons[neuronName].Get_Joint_Name().encode('ASCII')
                desiredAngle = self.nn.neurons[neuronName].Get_Value() * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Think(self, t):
        # self.nn.Print()
        self.nn.Update(t)

    def Get_Fitness(self, displacement, angularDisplacement):
        """ Old Fitness Code. Calculates displacement at end of simulation
        stateOfLinkZero = p.getLinkState(self.robotId, 0, computeLinkVelocity=1)
        # Minimize distance from C.O.M. spawnpoint (0, 0, 2) over time
        dist_from_origin = np.sqrt(stateOfLinkZero[0][0] ** 2 +
                                   stateOfLinkZero[0][1] ** 2 +
                                   (2 - stateOfLinkZero[0][2]) ** 2)
       """
        file = open(f"tmp{self.solutionID}.txt", "w")
        print(f"Displacement: {displacement}")
        print(f"angularDisplacement: {angularDisplacement}")
        # file.write(str((displacement + angularDisplacement) / c.ITERATIONS))
        file.write(str(1/(displacement / c.ITERATIONS)))
        file.close()
        os.rename(f"tmp{self.solutionID}.txt", f"fitness{self.solutionID}.txt")
