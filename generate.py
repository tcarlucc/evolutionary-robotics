import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

for i in range(10):
    for j in range(5):
        for k in range(5):
            s = 1 if i == 0 else 0.9 ** i  # Decay size of box 10% each iteration
            pyrosim.Send_Cube(name="Box", pos=[j, k, (.5 + i)], size=[s, s, s])

pyrosim.End()

