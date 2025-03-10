#!/usr/bin/python

import numpy as np

#np.set_printoptions(threshold='nan')

# Solve Tight-Binding Model for a Square Lattice System

#property values
t = 10.
mu = Vz+6*t
nr = 20
n = int(nr*(nr+1)/2)

# Create zero matrix for BdG
a = 1.
bdg = np.zeros((4*n,4*n),dtype='complex')
imax = np.array([int((i+1)*(i+2)/2)-1 for i in range(nr)])

# create the equilateral triangle lattice mesh
siteCoord = np.zeros((n,2))
latticeCtr = 0
for i in range(nr):
  for j in range(i+1):
    siteCoord[latticeCtr,0] = a*(j-i/2.)
    siteCoord[latticeCtr,1] = -i*a*np.sqrt(3)/2.
    latticeCtr+=1

np.savetxt(filename+'-coordinates.txt', siteCoord, fmt='%1.32f')

# fill in the bdg Hamiltonian without the pairing potential then add it's H.C.
alpha1 = alpha*1.0j*np.exp(-1.0j*np.pi/6.)
alpha2 = alpha*1.0j*np.exp( 1.0j*np.pi/6.)
row = 0
for i in range(n):
  # this is the current lattice site
  # I divide by 2 here because we will add the h.c. later which will double the diagonal values
  bdg[i,i]         =  (-mu+6*t+Vz)/2.
  bdg[i+n,i+n]     = -(-mu+6*t+Vz)/2.
  bdg[i+2*n,i+2*n] =  (-mu+6*t-Vz)/2.
  bdg[i+3*n,i+3*n] = -(-mu+6*t-Vz)/2.
  # pairing terms
  bdg[i,i+3*n]   =  delta
  bdg[i+2*n,i+n] = -delta
  # in-plane Zeeman terms
  bdg[i,i+2*n]   =  (Vx-1.0j*Vy)
  bdg[i+n,i+3*n] = -(Vx+1.0j*Vy)

  # determines how many nearest neighbors for the current lattice point there are
  # this looks to the right, down and right, and down and left
  # the h.c. will take care of the opposite directions of these three
  if row<nr-1:
    if i<imax[row]:
      # a lattice point either along the left edge or in the bulk
      nnidx = np.array([i+1,i+row+1,i+row+2])
    else: #i==imax
      # at the right most lattice point for the given row
      nnidx = np.array([i+row+1,i+row+2])
      row += 1
  else: #row==nr-1
    if i<imax[row]:
      # we are on the last row
      nnidx = np.array([i+1])
    else: #i==imax
      # at the last lattice site. Has no more nearest neighbors for the given directions
      nnidx = np.array([])
  nnn = np.size(nnidx)

  # this next part applies the hopping and rashba terms to the nearest neighbors
  for j in range(nnn):
    bdg[i,nnidx[j]]         = -t
    bdg[i+1*n,nnidx[j]+1*n] =  t
    bdg[i+2*n,nnidx[j]+2*n] = -t
    bdg[i+3*n,nnidx[j]+3*n] =  t
    if j==0 and (nnn==1 or nnn==3):
      # nearest neighbor along the x-direction
      bdg[i,nnidx[j]+2*n]   =  alpha
      bdg[i+2*n,nnidx[j]]   = -alpha
      bdg[nnidx[j]+3*n,i+n] = -alpha
      bdg[nnidx[j]+n,i+3*n] =  alpha
    elif (j==0 and nnn==2) or (j==1 and nnn==3):
      # nearest neighbor along +60 degree axis from x-axis
      bdg[i,nnidx[j]+2*n]   =  alpha2
      bdg[i+2*n,nnidx[j]]   =  alpha1
      bdg[nnidx[j]+3*n,i+n] = -alpha2
      bdg[nnidx[j]+n,i+3*n] = -alpha1
    elif (j==1 and nnn==2) or (j==2 and nnn==3):
      # nearest neighbor along -60 degree axis from x-axis
      bdg[i,nnidx[j]+2*n]   =  alpha1
      bdg[i+2*n,nnidx[j]]   =  alpha2
      bdg[nnidx[j]+3*n,i+n] = -alpha1
      bdg[nnidx[j]+n,i+3*n] = -alpha2

bdg += np.conj(np.transpose(bdg))
np.savetxt(filename+'-bdg.txt', bdg, fmt='%1.1f')
energy, tmp = np.linalg.eigh(bdg)
states = tmp[0:n,:]

idx = energy.argsort()[::-1]
energy = np.real(energy[idx])
states = states[:,idx]
np.savetxt(filename+'-energy.txt', energy, fmt='%1.8f')

# determine the edge energies and states
energyBandGap = np.loadtxt(filename+'-energy-band-gaps.txt')
idx = np.where(np.logical_and(energy>=energyBandGap[0],energy<=energyBandGap[1]))[0]
np.savetxt(filename+'-edge-state-energy.txt', energy[idx],     fmt='%1.8f')

states = np.real(np.multiply(states,np.conj(states)))
np.savetxt(filename+'-states.txt', states, fmt='%1.32f')
np.savetxt(filename+'-edge-state-states.txt', states[0:n,idx], fmt='%1.8f')
