import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np
import random

ITERATIONS = 1000

frontLegAmplitude = np.pi/3
frontLegFrequency = 20
frontLegPhaseOffset = np.pi/4

backLegAmplitude = np.pi/3
backLegFrequency = 10
backLegPhaseOffset = 0

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
robotId = p.loadURDF("body.urdf")
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(ITERATIONS)
frontLegSensorValues = np.zeros(ITERATIONS)

backLegTargetValues = backLegAmplitude * np.sin(backLegFrequency * np.linspace(0, 2*np.pi, ITERATIONS)
                                                + backLegPhaseOffset)
frontLegTargetValues = frontLegAmplitude * np.sin(frontLegFrequency * np.linspace(0, 2*np.pi, ITERATIONS)
                                                  + frontLegPhaseOffset)

for i in range(ITERATIONS):
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
