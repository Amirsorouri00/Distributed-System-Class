from __future__ import division
import numpy as np
import matplotlib.pyplot as pl
 
trials = 3000000
counts = 0
for i in range(trials):
          x = np.random.random()
          y = np.random.random()
          x2 = x**2
          y2 = y**2
          x_y = x2 + y2
          dxy = np.sqrt(x_y)
          if dxy <= 1:
                    counts = counts + 1
 
print ("pi was approximated at ::",4*counts/trials)
