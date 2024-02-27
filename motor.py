import constants as c
import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.frontLegAmplitude
        self.frequency = c.frontLegFrequency
        self.offset = c.frontLegOffset
        self.targetAngles = None

        if self.jointName == b"Torso_BackLeg":
            self.targetAngles = c.backLegAmplitude * np.sin(c.backLegFrequency * np.linspace(0, 2 * np.pi, c.ITERATIONS)
                                                            + c.backLegPhaseOffset)
        else:
            self.targetAngles = c.frontLegAmplitude * np.sin(c.frontLegFrequency * np.linspace(0, 2 * np.pi, c.ITERATIONS)
                                                             + c.frontLegOffset)

    def Set_Value(self, t, robotId):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=self.jointName, controlMode=p.POSITION_CONTROL,
                                    targetPosition=self.targetAngles[t], maxForce=50)

    def Save_Values(self):
        np.save("data/targetAngles.npy", self.targetAngles)