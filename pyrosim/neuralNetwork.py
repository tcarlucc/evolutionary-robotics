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

        f = open(nndfFileName,"r")

        for line in f.readlines():

            self.Digest(line)

        f.close()

    def Print(self):

        self.Print_Sensor_Neuron_Values()

        self.Print_Hidden_Neuron_Values()

        self.Print_Motor_Neuron_Values()

        print("")

    def Update(self):

        for neuronName in self.neurons.keys():

                if self.neurons[neuronName].Is_Sensor_Neuron():

                    # self.neurons[neuronName].Update_Sensor_Neuron()

                    if p.getJointState(self.robotId, int(neuronName))[1] == 0:

                        self.neurons[neuronName].Set_Value(1)

                    else:

                        self.neurons[neuronName].Set_Value(p.getJointState(self.robotId, int(neuronName))[1])

                    print(p.getJointState(self.robotId, int(neuronName))[1])

                else:

                        self.neurons[neuronName].Update_Hidden_Or_Motor_Neuron(self.neurons, self.synapses)

                        # self.prevMotorNeuronValues[int(neuronName)-c.numMotorNeurons] = self.neurons[neuronName].Get_Value()

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
