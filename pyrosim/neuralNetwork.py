import constants
from pyrosim.neuron  import NEURON

from pyrosim.synapse import SYNAPSE

import pybullet as p

import constants as c

import numpy as np

import random

class NEURAL_NETWORK: 

    def __init__(self,nndfFileName, robotId):

        self.neurons = {}

        self.synapses = {}

        self.robotId = robotId

        self.prevMotorNeuronValues = {0: 1,
                                      1: 1,
                                      2: 1,
                                      3: 1,
                                      4: 0,
                                      5: 0,
                                      6: 0,
                                      7: 0}

        self.prevLinkState = p.getLinkState(self.robotId, 0, computeLinkVelocity=1)

        self.currentTimeStep = 0

        f = open(nndfFileName,"r")

        for line in f.readlines():

            self.Digest(line)

        f.close()

    def Print(self):

        self.Print_Sensor_Neuron_Values()

        self.Print_Hidden_Neuron_Values()

        self.Print_Motor_Neuron_Values()

        print("")

    def Update(self, timestep):

        """
        TODO: Implement Deltas and Acceleration
        Main idea will be to keep track of the previous timesteps link state and utilize that to calculate rate of
        change and just general change for the inputs below.
        """

        linkState = p.getLinkState(self.robotId, 0, computeLinkVelocity=1)

        """ Test A for sensor neurons
            When changing remember to update constants.py
        for neuronName in self.neurons.keys():

                if self.neurons[neuronName].Is_Sensor_Neuron():

                    linkState = p.getLinkState(self.robotId, 0, computeLinkVelocity=1)

                    # Position of center of mass neurons
                    if int(neuronName) < 3:

                        self.neurons[neuronName].Set_Value(linkState[0][int(neuronName)])

                    # Orientation of center of mass neurons
                    elif int(neuronName) < 7:

                        self.neurons[neuronName].Set_Value(linkState[1][int(neuronName)-3])

                    # Linear velocity of torso neurons
                    elif int(neuronName) < 10:

                        self.neurons[neuronName].Set_Value(linkState[6][int(neuronName)-7])

                    # Angular velocity of torso neurons
                    elif int(neuronName) < 13:

                        self.neurons[neuronName].Set_Value(linkState[7][int(neuronName)-10])

                else:

                        self.neurons[neuronName].Update_Hidden_Or_Motor_Neuron(self.neurons, self.synapses)"""

        """ 
        Test B for sensor neurons
        """
        for neuronName in self.neurons.keys():


            # Handle all non-time dependent sensor neurons
            if self.neurons[neuronName].Is_Sensor_Neuron():

                # Position of center of mass neurons
                if int(neuronName) < 3:
                    self.neurons[neuronName].Set_Value(linkState[0][int(neuronName)])

                # Orientation of center of mass neurons
                elif int(neuronName) < 7:
                    self.neurons[neuronName].Set_Value(linkState[1][int(neuronName) - 3])

                # Linear velocity of torso neurons
                elif int(neuronName) < 10:
                    self.neurons[neuronName].Set_Value(linkState[6][int(neuronName) - 7])

                # Angular velocity of torso neurons
                elif int(neuronName) < 13:
                    self.neurons[neuronName].Set_Value(linkState[7][int(neuronName) - 10])

                elif timestep == 0 and int(neuronName) > 12:
                    self.neurons[neuronName].Set_Value(0)

                elif timestep > 0:
                    # Acceleration neurons
                    if int(neuronName) < 16:
                        self.neurons[neuronName].Set_Value((linkState[6][int(neuronName) - 13] -
                                                           self.prevLinkState[6][int(neuronName) - 13]))

                    # Angular acceleration neurons
                    elif int(neuronName) < 19:
                        self.neurons[neuronName].Set_Value((linkState[7][int(neuronName) - 16] -
                                                           self.prevLinkState[7][int(neuronName) - 16]))

                    # Delta of position neurons
                    elif int(neuronName) < 22:
                        self.neurons[neuronName].Set_Value((linkState[0][int(neuronName) - 19] -
                                                           self.prevLinkState[0][int(neuronName) - 19]))

                    # Delta of orientation neurons
                    elif int(neuronName) < 25:
                        self.neurons[neuronName].Set_Value((linkState[1][int(neuronName) - 22] -
                                                           self.prevLinkState[1][int(neuronName) - 22]))

                    # Delta of linear velocity neurons
                    elif int(neuronName) < 28:
                        self.neurons[neuronName].Set_Value((linkState[6][int(neuronName) - 25] -
                                                           self.prevLinkState[6][int(neuronName) - 25]))
                    # Delta of angular velocity neurons
                    elif int(neuronName) < 31:
                        self.neurons[neuronName].Set_Value((linkState[7][int(neuronName) - 28] -
                                                           self.prevLinkState[7][int(neuronName) - 28]))

            else:
                self.neurons[neuronName].Update_Hidden_Or_Motor_Neuron(self.neurons, self.synapses)

        self.prevLinkState = linkState

    def Get_Neuron_Names(self):

        return self.neurons.keys()

    def Is_Motor_Neuron(self, neuronName):

            return self.neurons[neuronName].Is_Motor_Neuron()

    def Get_Joint_Name(self, neuronName):

            return self.neurons[neuronName].Get_Joint_Name()

    def Get_Value(self, neuronName):

            return self.neurons[neuronName].Get_Value()

# ---------------- Private methods --------------------------------------

    def Add_Neuron_According_To(self,line):

        neuron = NEURON(line)

        self.neurons[ neuron.Get_Name() ] = neuron

    def Add_Synapse_According_To(self,line):

        synapse = SYNAPSE(line)

        sourceNeuronName = synapse.Get_Source_Neuron_Name()

        targetNeuronName = synapse.Get_Target_Neuron_Name()

        self.synapses[sourceNeuronName , targetNeuronName] = synapse

    def Digest(self,line):

        if self.Line_Contains_Neuron_Definition(line):

            self.Add_Neuron_According_To(line)

        if self.Line_Contains_Synapse_Definition(line):

            self.Add_Synapse_According_To(line)

    def Line_Contains_Neuron_Definition(self,line):

        return "neuron" in line

    def Line_Contains_Synapse_Definition(self,line):

        return "synapse" in line

    def Print_Sensor_Neuron_Values(self):

        print("sensor neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Sensor_Neuron():

                self.neurons[neuronName].Print()

        print("")

    def Print_Hidden_Neuron_Values(self):

        print("hidden neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Hidden_Neuron():

                self.neurons[neuronName].Print()

        print("")

    def Print_Motor_Neuron_Values(self):

        print("motor neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Motor_Neuron():

                self.neurons[neuronName].Print()

        print("")
