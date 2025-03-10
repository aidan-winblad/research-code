#!/usr/bin/python3

import numpy as np
import scipy.special as sp

# Constants
hbar = 6.582E-16 # 6.582 * 10^-16 [eV*s]
c = 2.998E8 # 2.998 * 10^8 [m/s]
q = 1.602E-19 # [C]
m_e = 0.51E6 / c**2 # [MeV/c^2]
pi = np.pi

# System parameters
a = 0.56E-9 # GaAs/AlGaAs: a = 0.56nm
#a = 1e-9 # [m]
m = 0.067 * m_e # GaAs/AlGaAs: m = 0.067m_e
#m = 1.0 * m_e # [MeV/c^2]
h = hbar**2 / (2 * m * a**2) # hopping value for square lattice
print(h)
k = 0 # [m^-1] Momentum space wavenumber
ka = k*a

# Laser parameters
hw = 191e-3 # [meV]
Estrength = 2e8 # V/m
d = 100E-9 # [m] Spatial period of the electric field of laser in x direction, make sure d>>a and not necessarily integer multiple
K = 2*pi/d # Spatial wavenumber of laser light in x direction

# Matrix cutoffs
# Number of modes
mc = 5
Nm = 2*mc+1
nhw = np.arange(-mc,mc+1,1)

# Size of system in x direction
rc = 10
xm = rc*a
Nr = 2*rc+1
xj = np.linspace(-xm, xm, Nr)
Kxj = K*xj

phimin = 0
phimax = 1e9 # unitless
phimax = Estrength*a/hw # unitless
print('Phimax ', phimax)

nphi = 100
phi0 = np.linspace(phimin,phimax,nphi)
#energy = np.zeros( (Nm*Nr, nphi) )
energy = np.zeros( (Nr, nphi) )
H = np.zeros( (Nm,Nr,Nr) )

# For loop over the phi0 terms
for i, phi in enumerate(phi0):

  # Calculate individual block matrices for given phi0 and construct Q matrix
  # Clear the Q matrix since we will be adding to the matrix
  Q = np.zeros( (Nm*Nr,Nm*Nr) )
  for n in range(Nm):
    H[n] = -2*h*np.diag(sp.jv(n,phi*np.cos(Kxj)),k=0)*np.cos(ka-n*pi/2) - h*np.diag(sp.jv(n,phi*np.ones(Nr-1)),k=1) - h*(-1)**n * np.diag(sp.jv(n,phi*np.ones(Nr-1)),k=-1)
    if(n != 0):
      Q += np.kron(np.diag(np.ones(Nm-n),k=-n),H[n])
    else:
      Q += np.kron(np.eye(Nm),H[0]) + np.kron(np.diag(nhw,k=0),np.eye(Nr))

  eng = np.linalg.eigvalsh(Q, UPLO = 'L')
  energy[:,i] = eng[mc*Nr:(mc+1)*Nr]


np.savetxt('./data/eng-matrix.txt', energy, fmt='%1.8f')


