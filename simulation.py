import constants as c
from world import WORLD
from robot import ROBOT
import numpy as np
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time


class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        self.robot = ROBOT()

        self.backLegTargetValues = c.backLegAmplitude * np.sin(
            c.backLegFrequency * np.linspace(0, 2 * np.pi, c.ITERATIONS) + c.backLegPhaseOffset)

        self.frontLegTargetValues = c.frontLegAmplitude * np.sin(
            c.frontLegFrequency * np.linspace(0, 2 * np.pi, c.ITERATIONS) + c.frontLegPhaseOffset)

        p.setGravity(0, 0, -9.8)
        pyrosim.Prepare_To_Simulate(self.world.robotId)

    def run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()

            pyrosim.Set_Motor_For_Joint(bodyIndex=self.world.robotId, jointName=b"Torso_BackLeg",
                                        controlMode=p.POSITION_CONTROL,
                                        targetPosition=self.backLegTargetValues[i], maxForce=50)

            pyrosim.Set_Motor_For_Joint(bodyIndex=self.world.robotId, jointName=b"Torso_FrontLeg",
                                        controlMode=p.POSITION_CONTROL,
                                        targetPosition=self.frontLegTargetValues[i], maxForce=50)

            time.sleep(1 / 60)
            # print(i)   Removed for the sensor statement above
