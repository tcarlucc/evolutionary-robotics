import constants as c
from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
import numpy as np
import pyrosim.pyrosim as pyrosim


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, 0)  # z = -9.8 to enable gravity
        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            for linkIndex in range(p.getNumJoints(self.robot.robotId)):
                velocity_vector = self.Calculate_Drag(np.asarray(p.getLinkState(self.robot.robotId, linkIndex,
                                             computeLinkVelocity=1)[6]), linkIndex)
                local_coords = p.getLinkState(self.robot.robotId, linkIndex)[2]
                p.applyExternalForce(self.robot.robotId, linkIndex, velocity_vector, local_coords, p.LINK_FRAME)
            if i % 5 == 0:
                pass
                #p.applyExternalForce(self.robot.robotId, 0, (0, 5, 0), (0, 0.5, 0), p.WORLD_FRAME)  # 'Stream' of air
            if self.directOrGUI == "GUI":
                time.sleep(1 / 60)


    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def Calculate_Drag(self, velocity_vector, linkIndex):
        # Drag calculation from: F. Corucci et al. (2018) "Evolving Soft Locomotion"
        if linkIndex == 0:
            # 1.0 is Area of the torso
            return 0.5 * c.fluidDensity * 1.0 * c.dragCoefficient * velocity_vector ** 2
        else:
            # 0.2 is Area of each link
            return 0.5 * c.fluidDensity * 0.2 * c.dragCoefficient * velocity_vector ** 2

