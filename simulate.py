import constants as c
import numpy as np
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from simulation import SIMULATION
import time
import random

'''
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
robotId = p.loadURDF("body.urdf")
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(c.ITERATIONS)
frontLegSensorValues = np.zeros(c.ITERATIONS)

backLegTargetValues = c.backLegAmplitude * np.sin(c.backLegFrequency * np.linspace(0, 2*np.pi, c.ITERATIONS)
                                                + c.backLegPhaseOffset)
frontLegTargetValues = c.frontLegAmplitude * np.sin(c.frontLegFrequency * np.linspace(0, 2*np.pi, c.ITERATIONS)
                                                  + c.frontLegPhaseOffset)

for i in range(c.ITERATIONS):
    p.stepSimulation()

    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_BackLeg", controlMode=p.POSITION_CONTROL,
                                targetPosition=backLegTargetValues[i], maxForce=50)
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_FrontLeg", controlMode=p.POSITION_CONTROL,
                                targetPosition=frontLegTargetValues[i], maxForce=50)

    time.sleep(1/60)
    # print(i)   Removed for the sensor statement above

np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)
#np.save("data/targetAngles.npy", targetAngles)
p.disconnect()
'''
simulation = SIMULATION()