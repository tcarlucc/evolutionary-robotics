import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import sys
import time
import constants as c

class SOLUTION:
    def __init__(self, myID):
        self.sensor_to_hidden_weights = (np.random.rand(c.numSensorNeurons, c.numHiddenNeurons) * 2) - 1
        self.hidden_to_motor_weights = (np.random.rand(c.numHiddenNeurons, c.numMotorNeurons) * 2) - 1
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
        # pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])  # Artifact from intro to pybullet
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 2], size=[1, 1, 1])

        # Back Legs
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", position=[0, -0.5, 2],
                           type="revolute", jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", position=[0, -1, 0],
                           type="revolute", jointAxis="1 0 0")

        # Front Legs
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", position=[0, 0.5, 2],
                           type="revolute", jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg",
                           position=[0, 1, 0], type="revolute", jointAxis="1 0 0")

        # Left Legs
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", position=[-0.5, 0, 2],
                           type="revolute", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", position=[-1, 0, 0],
                           type="revolute", jointAxis="0 1 0")

        # Right Legs
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", position=[0.5, 0, 2],
                           type="revolute", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", position=[1, 0, 0],
                           type="revolute", jointAxis="0 1 0")

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        for i in range(0, c.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name=i)

        for i in range(c.numSensorNeurons, c.numSensorNeurons + c.numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=i)

        jointNames = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", "BackLeg_BackLowerLeg",
                      "FrontLeg_FrontLowerLeg", "LeftLeg_LeftLowerLeg", "RightLeg_RightLowerLeg"]

        for i in range(c.numSensorNeurons+c.numHiddenNeurons, c.numSensorNeurons+c.numHiddenNeurons+c.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name=i, jointName=jointNames[i-(c.numSensorNeurons+c.numHiddenNeurons)])

        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0, c.numHiddenNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight=self.sensor_to_hidden_weights[currentRow][currentColumn])

        for currentRow in range(0, c.numHiddenNeurons):
            for currentColumn in range(0, c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow+c.numSensorNeurons,
                                     targetNeuronName=currentColumn+c.numSensorNeurons+c.numHiddenNeurons,
                                     weight=self.hidden_to_motor_weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        """row = random.randint(0, c.numSensorNeurons - 1)
        col = random.randint(0, c.numHiddenNeurons - 1)
        self.sensor_to_hidden_weights[row, col] = (random.random() * 2) - 1

        row = random.randint(0, c.numHiddenNeurons - 1)
        col = random.randint(0, c.numMotorNeurons - 1)
        self.hidden_to_motor_weights[row, col] = (random.random() * 2) - 1
        """
        ih_synapses_to_mutate = random.randint(0, (c.numSensorNeurons * c.numHiddenNeurons))
        for i in range(ih_synapses_to_mutate):
            row = random.randint(0, c.numSensorNeurons - 1)
            col = random.randint(0, c.numHiddenNeurons - 1)
            self.sensor_to_hidden_weights[row, col] = (random.random() * 2) - 1

        hm_synapses_to_mutate = random.randint(0, (c.numHiddenNeurons * c.numMotorNeurons))
        for i in range(hm_synapses_to_mutate):
            row = random.randint(0, c.numHiddenNeurons - 1)
            col = random.randint(0, c.numMotorNeurons - 1)
            self.hidden_to_motor_weights[row, col] = (random.random() * 2) - 1


    def Set_ID(self, myID):
        self.myID = myID
