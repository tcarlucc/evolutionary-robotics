import pyrosim.pyrosim as pyrosim

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", position=[0.5, 0, 1], type="revolute")
    pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", position=[-0.5, 0, 1], type="revolute")
    pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
    pyrosim.End()


def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.End()

Generate_Body()
Generate_Brain()
