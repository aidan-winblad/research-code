#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sp
np.set_printoptions(linewidth=np.inf, precision=4)


def hjjn(_n, _i, _j, _phi0, _kj):
  #cs = np.cos(_kj)
  cs = np.cos(_kj*2*np.pi)
  if _i == _j:
    #return -(sp.jv(_n,_phi0*cs)+sp.jv(_n,-_phi0*cs)) * np.exp(1.0j*_n*np.pi/2)
    return 2*cs
  elif _i+1 == _j:
    #print(-sp.jv(_n,_phi0))
    #return -sp.jv(_n,_phi0)
    return 1
  elif _i-1 == _j:
    #print(-(-1)**_n*sp.jv(_n,_phi0))
    #return -(-1)**_n*sp.jv(_n,_phi0)
    return 1
  else:
    return 0

rc = 10
Ns = 2*rc+1

mc = 0
Nm = 2*mc+1

ka = 0.1
hw = 0*0.1
nphi = 500
phimax = 100
#phi0 = np.linspace(-phimax,phimax,nphi)
phi0 = np.linspace(0,phimax,nphi)
energy = np.zeros((Nm*Ns,nphi))

for k in range(nphi):
  Hn = np.zeros([Nm,Ns,Ns], "complex")

  for n in range(Nm):
    for i in range(Ns):
      for j in range(Ns):
        #kj = (j%Ns)*ka
        kj = (j-rc)*ka
        Hn[n,i,j] = hjjn(0, i, j, phi0[k], kj)
#        if k==0:
#          print(Hn[n,i,j])

  #print(Hn[0])
  #print()

  Qmn = np.zeros([Nm*Ns, Nm*Ns],"complex")

  for i in range(Nm):
    for j in range(Nm-i):
      midx = mc-j
      r1 = (i+j)*Ns
      r2 = (i+j+1)*Ns
      c1 = j*Ns
      c2 = (j+1)*Ns
      if i == 0:
        Qmn[r1:r2,r1:r2] = Hn[i,:,:] - midx*hw*np.eye(Ns)
      else:
        Qmn[r1:r2,c1:c2] = Hn[i,:,:]

  #print(Qmn[0:Ns,0:Ns], '\n')
  #print(Qmn[0*Ns:3*Ns,0*Ns:3*Ns])

  energy[:,k] = np.linalg.eigvalsh(Qmn)

xaxis = np.array([-1, 1])
plt.figure(figsize=(10,10))
plt.tick_params(
    axis='x',
    which='both',
    bottom='on',
    top='off',
    labelbottom='on')
plt.ylabel('$E(\phi_0)$', fontsize=12)
plt.xlabel('$\phi_0$', fontsize=12)
#plt.xlim(phi0[0], phi0[-1])
plt.xlim(phi0[0], phi0[-1])
#plt.ylim(np.min(energy),np.max(energy))
#plt.ylim(-2, 0)


for i in range(Nm*Ns):
  plt.plot(phi0, energy[i,:], '.', color = 'r', markersize = 1.5)
#  plt.plot(phi0, energy[i,:], color = 'b', markersize = .1)

#for i in range(Nm*Ns):
#  plt.plot(xaxis,[energy[i],energy[i]], 'g')

plt.tight_layout()

#plt.savefig('../../data/fig-spectral-flow.pdf')
plt.show()
plt.close()

Emax = np.max(energy)
Emin = np.min(energy)
nE = 300
dE = (Emax-Emin)/(nE-1)
E = np.array([i*dE+Emin for i in range(nE)])
gE = np.zeros((nphi,nE))
for i in range(nphi):
  for j in range(nE-1):
    idx = np.where(np.logical_and(energy[:,i]>E[j],energy[:,i]<E[j+1]))[0]
    gE[i,j+1] = np.size(idx)

#print(gE)
plt.figure(figsize=(10,10))
Extent = [-phimax, phimax, 0.25*Emin, 0.25*Emax]
#plt.colorbar()

# include cmap='some_color' into the imshow function
#'viridis', aspect=3/5, RdGy, alpha=0.5
#plt.imshow(gE, origin='lower', interpolation="none", extent=Extent, cmap= 'viridis', aspect=3/5)
#plt.savefig('../../data/fig-dos-spectral-flow.pdf')
#plt.axis(aspect='image')
#plt.show()
#plt.close()
