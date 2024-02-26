import pybullet as p
import pybullet_data


class WORLD:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")

