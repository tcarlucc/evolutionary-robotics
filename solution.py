import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import sys
import time
import constants as c

class SOLUTION:
    def __init__(self, myID):
        self.weights = (np.random.rand(3, 2) * 2) - 1
        self.fitness = None
        self.myID = myID

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system(f'start /B py simulate.py {directOrGUI} {str(self.myID)}')
        fitnessFileName = f"fitness{str(self.myID)}"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        print(self.fitness)
        fitnessFile.close()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {str(self.myID)}")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        file = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(file.read())
        file.close()
        os.system(f"del fitness{self.myID}.txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", position=[0.5, 0, 1],
                           type="revolute")
        pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", position=[-0.5, 0, 1],
                           type="revolute")
        pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0, c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons - 1)
        col = random.randint(0, c.numMotorNeurons - 1)
        self.weights[row, col] = (random.random() * 2) - 1

    def Set_ID(self, myID):
        self.myID = myID