import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


bulkyFitnessTrend = np.load('data/analyze/BulkyFitnessTrend.npy')
bulkyFitnessTrend2 = np.load('data/analyze/BulkyFitnessTrend2.npy')
bulkyFitnessTrend3 = np.load('data/analyze/BulkyFitnessTrend3.npy')
bulkyFitnessTrend4 = np.load('data/analyze/BulkyFitnessTrend4.npy')
bulkyFitnessTrend5 = np.load('data/analyze/BulkyFitnessTrend5.npy')

leanFitnessTrend = np.load('data/analyze/LeanFitnessTrend.npy')
leanFitnessTrend2 = np.load('data/analyze/LeanFitnessTrend2.npy')
leanFitnessTrend3 = np.load('data/analyze/LeanFitnessTrend3.npy')
leanFitnessTrend4 = np.load('data/analyze/LeanFitnessTrend4.npy')
leanFitnessTrend5 = np.load('data/analyze/LeanFitnessTrendBest.npy')

A_Average = (leanFitnessTrend + leanFitnessTrend2 + leanFitnessTrend3 + leanFitnessTrend4 + leanFitnessTrend5) / 5
B_Average = (bulkyFitnessTrend + bulkyFitnessTrend2 + bulkyFitnessTrend3 + bulkyFitnessTrend4 + bulkyFitnessTrend5) / 5

"""def plot_bulky_values():
    plt.plot(bulkyFitnessTrend, label="'Bulky' Brain Fitness Trend")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()"""

def plot_all():
    plt.plot(bulkyFitnessTrend, label="B1", color='red')
    plt.plot(bulkyFitnessTrend2, label="B2", color='red')
    plt.plot(bulkyFitnessTrend3, label="B3", color='red')
    plt.plot(bulkyFitnessTrend4, label="B4", color='red')
    plt.plot(bulkyFitnessTrend5, label="B5", color='red')

    plt.plot(leanFitnessTrend, label="A1", color='blue')
    plt.plot(leanFitnessTrend2, label="A2", color='blue')
    plt.plot(leanFitnessTrend3, label="A3", color='blue')
    plt.plot(leanFitnessTrend4, label="A4", color='blue')
    plt.plot(leanFitnessTrend5, label="A5", color='blue')

    blue_patch = mpatches.Patch(color='blue', label='A Variants')
    red_patch = mpatches.Patch(color='red', label='B Variants')

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.ylim(0, 1.5)
    plt.legend(handles=[blue_patch, red_patch])
    plt.show()

def plot_avg():
    plt.plot(A_Average, label="A Average", color='blue')
    plt.plot(B_Average, label="B Average", color='red')
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.ylim(0, 1.25)
    plt.legend()
    plt.show()

print(bulkyFitnessTrend4)