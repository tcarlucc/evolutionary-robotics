import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
robotId = p.loadURDF("body.urdf")
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(10000)
for i in range(1000):
    p.stepSimulation()

    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")

    time.sleep(1/60)
    # print(i)   Removed for the sensor statement above

p.disconnect()
print(backLegSensorValues)
