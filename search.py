import os
from hillclimber import HILL_CLIMBER

hc = HILL_CLIMBER()
hc.Evolve()
hc.Show_Best()

"""for i in range(5):
    os.system("py generate.py")
    os.system("py simulate.py")"""