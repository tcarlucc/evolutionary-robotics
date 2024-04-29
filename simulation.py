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
        self.totalDisplacement = 0
        self.angularDisplacement = 0

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think(i)
            self.robot.Act(i)
            for linkIndex in range(p.getNumJoints(self.robot.robotId)):
                velocity_vector = self.Calculate_Drag(np.asarray(p.getLinkState(self.robot.robotId, linkIndex,
                                             computeLinkVelocity=1)[6]), linkIndex)
                local_coords = p.getLinkState(self.robot.robotId, linkIndex)[2]
                p.applyExternalForce(self.robot.robotId, linkIndex, velocity_vector, local_coords, p.LINK_FRAME)
            self.Calc_Displacement()
            self.Calc_Angular_Velocity_Displacement()
            if i % 5 == 0:
                #for j in range(len(pyrosim.linkNamesToIndices) - 1):
                for j in range(p.getNumJoints(self.robot.robotId)):
                    p.applyExternalForce(self.robot.robotId, j, (0, 0.65, 0), (0, 0, 0), p.WORLD_FRAME)  # 'Stream'
            if self.directOrGUI == "GUI":
                time.sleep(1 / 60)


    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness(self.totalDisplacement, self.angularDisplacement)

    def Calculate_Drag(self, velocity_vector, linkIndex):
        # Drag calculation from: F. Corucci et al. (2018) "Evolving Soft Locomotion"
        if linkIndex == 0:
            # 1.0 is Area of the torso
            return 0.5 * c.fluidDensity * 0.47 * c.dragCoefficient * velocity_vector ** 2
        else:
            # 0.2 is Area of each link
            return 0.5 * c.fluidDensity * 0.2 * c.dragCoefficient * velocity_vector ** 2

    def Calc_Displacement(self):
        linkState = p.getLinkState(self.robot.robotId, 0, computeLinkVelocity=1)
        # Calculate distance from spawnpoint (0, 0, 3) over time
        self.totalDisplacement += np.sqrt(linkState[0][0] ** 2 + linkState[0][1] ** 2 + (3 - linkState[0][2]) ** 2)

    def Calc_Angular_Velocity_Displacement(self):
        linkState = p.getLinkState(self.robot.robotId, 0, computeLinkVelocity=1)
        self.angularDisplacement += np.sqrt(linkState[7][0] ** 2 + linkState[7][1] ** 2 + linkState[7][2] ** 2)