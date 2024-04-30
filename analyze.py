import numpy as np
import matplotlib.pyplot as plt


bulkyFitnessTrend = np.load('data/BulkyFitnessTrend.npy')
leanFitnessTrend = np.load('data/LeanFitnessTrend.npy')

"""def plot_bulky_values():
    plt.plot(bulkyFitnessTrend, label="'Bulky' Brain Fitness Trend")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()"""

def plot_values():
    plt.plot(bulkyFitnessTrend, label="'Bulky' Brain Fitness Trend")
    plt.plot(leanFitnessTrend, label="'Lean' Brain Fitness Trend")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()

plot_values()
