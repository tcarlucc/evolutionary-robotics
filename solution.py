import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import sys
import time

class SOLUTION:
    def __init__(self):
        self.weights = (np.random.rand(3, 2) * 2) - 1
        self.fitness = None

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system(f'start /B py simulate.py {directOrGUI}')
        fitnessFile = open("fitness.txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])
        pyrosim.End()
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", position=[0.5, 0, 1],
                           type="revolute")
        pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", position=[-0.5, 0, 1],
                           type="revolute")
        pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.End()
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        while not os.path.exists("brain.nndf"):
            time.sleep(0.01)

        for currentRow in range(0, 3):
            for currentColumn in range(0, 2):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        row = random.randint(0, 2)
        col = random.randint(0, 1)
        self.weights[row, col] = (random.random() * 2) - 1
