import constants as c
from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
import numpy as np
import pyrosim.pyrosim as pyrosim

DRAG_COEF = 3.8


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
        #print(p.getLinkState(self.robot.robotId, 2, 1))  # << use in drag calculation

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            for linkIndex in range(p.getNumJoints(self.robot.robotId)):
                velocity_vector = self.Calculate_Drag(np.asarray(p.getLinkState(self.robot.robotId, linkIndex,
                                             computeLinkVelocity=1)[6]))
                local_coords = p.getLinkState(self.robot.robotId, linkIndex)[2]
                p.applyExternalForce(self.robot.robotId, linkIndex, velocity_vector, local_coords, p.LINK_FRAME)

            # p.applyExternalForce(self.robot.robotId, -1, self.Calculate_Drag(), [1, 1, 1], p.LINK_FRAME)  # Reference
            if self.directOrGUI == "GUI":
                time.sleep(1 / 60)


    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def Calculate_Drag(self, velocity_vector):
        velocity = np.linalg.norm(velocity_vector)
        drag = 0.5 * c.fluidDensity * 0.2 * c.dragCoefficient * velocity ** 2
        return drag
