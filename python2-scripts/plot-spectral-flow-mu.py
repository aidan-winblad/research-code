#!/usr/bin/python
#
# Created by: Aidan Winblad
#

import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt


# load in eigen- energy
edgeEnergies = np.loadtxt('../../data/bdg-spectral-flow-mu.txt')
n = np.shape(edgeEnergies)[1]-1

plt.figure(figsize=(2,4))
plt.xlabel('$\mu (t)$', fontsize=12)
plt.ylabel('$E (t)$', fontsize=12)
plt.xlim(edgeEnergies[0,0],edgeEnergies[-1,0])
plt.ylim(np.min(edgeEnergies[:,1:]),np.max(edgeEnergies[:,1:]))
for i in xrange(n):
  plt.plot(edgeEnergies[:,0],edgeEnergies[:,i+1], 'b', linewidth=0.25)
#plt.show()
plt.savefig('../data/fig-spectral-flow-mu.pdf')
