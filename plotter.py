#!/usr/bin/env python3

# plotter.py

import matplotlib.pyplot as plt
import numpy as np

y = np.array([35, 25, 25, 15])
mylabels = ["Apples", "Bananas", "Cherries", "Dates"]

plt.pie(y, labels = mylabels)

output_filename = "my_pie_chart.png"
plt.savefig(output_filename)
# plt.show()     
