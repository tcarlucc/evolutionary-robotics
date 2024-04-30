import constants
from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for parent in self.parents.keys():
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.keys():
            self.children[child].Mutate()

    def Select(self):
        for parent in self.parents.keys():
            if self.parents[parent].fitness > self.children[parent].fitness:
                self.parents[parent] = self.children[parent]

        try:
            fitnessTrend = np.load('data/BulkyFitnessTrend.npy')
            fitnessTrend = np.append(fitnessTrend, [self.parents[self.Find_Best_Parent()].fitness])
            np.save('data/BulkyFitnessTrend.npy', fitnessTrend)
            print(fitnessTrend)
        except FileNotFoundError:
            fitnessTrend = np.array([self.parents[self.Find_Best_Parent()].fitness])
            np.save('data/BulkyFitnessTrend.npy', fitnessTrend)
        np.save('data/bestSensorToHidden.npy', self.parents[self.Find_Best_Parent()].sensor_to_hidden_weights)
        np.save('data/bestHiddenToMotor.npy', self.parents[self.Find_Best_Parent()].hidden_to_motor_weights)

    def Print(self):
        for parent in self.parents.keys():
            print(f"Parent Fitness: {self.parents[parent].fitness}, Child Fitness: {self.children[parent].fitness}")

    def Show_Best(self):
        curr = float('inf')
        best_parent = self.Find_Best_Parent()
        self.parents[best_parent].Start_Simulation("GUI")
        np.save('data/bestSensorToHidden.npy', self.parents[best_parent].sensor_to_hidden_weights)
        np.save('data/bestHiddenToMotor.npy', self.parents[best_parent].hidden_to_motor_weights)


    def Evaluate(self, solutions):
        for solution in solutions.keys():
            solutions[solution].Start_Simulation("DIRECT")
        for solution in solutions.keys():
            solutions[solution].Wait_For_Simulation_To_End()

    def Find_Best_Parent(self):
        curr = float('inf')
        best_parent = self.parents[0]
        for parent in self.parents.keys():
            num = self.parents[parent].fitness
            if num < curr:
                curr = num
                best_parent = parent
        return best_parent
