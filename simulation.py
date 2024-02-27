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

        self.backLegTargetValues = c.backLegAmplitude * np.sin(
            c.backLegFrequency * np.linspace(0, 2 * np.pi, c.ITERATIONS) + c.backLegPhaseOffset)

        self.frontLegTargetValues = c.frontLegAmplitude * np.sin(
            c.frontLegFrequency * np.linspace(0, 2 * np.pi, c.ITERATIONS) + c.frontLegPhaseOffset)

        p.setGravity(0, 0, -9.8)
        pyrosim.Prepare_To_Simulate(self.world.robotId)
        self.robot = ROBOT()

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)

            time.sleep(1 / 60)
            # print(i)   Removed for the sensor statement above

    def __del__(self):
        p.disconnect()
