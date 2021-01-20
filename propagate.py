#!/usr/bin/env python
import numpy as np
import pylab as plt

def ev( dbeta, Cabs, om, phi, Delta):
    C = Cabs * np.exp( 1j* om )
    # gamma
    # gm = np.sqrt( dbeta**2 + np.abs(C)**2 )
    gm = np.sqrt( dbeta**2 + Cabs**2 )
    D = gm - dbeta
    
    eps = D/Cabs
    eps2 = eps**2
    s10 = (1-eps2)/(1+eps2)
    ff = 2*eps/(1+eps2)
    s20 = ff * np.sin(om)
    s30 = ff * np.cos(om)
    
    t = np.arange( -1.0, 1.2, 0.5 )
    ex = s10 * t
    ey = s20 * t
    ez = s30 * t
    
    return (ex, ey, ez)

    
def trajectory( dbeta, Cabs, om, phi, Delta, theta):
    """
    dbeta: \delta\beta
    Cabs: |C|
    om: \omega; C = |C| exp(j * om)
    phi and Delta: 
       X_1(0) = exp( -i Delta/2 ) * cos( phi )
       X_2(0) = exp( +i Delta/2 ) * sin( phi )
    
    theta: gamma z / 2
    
    calculate trajectory on Poincare sphere
    """
    C = Cabs * np.exp( 1j* om )
    # gamma
    # gm = np.sqrt( dbeta**2 + np.abs(C)**2 )
    gm = np.sqrt( dbeta**2 + Cabs**2 )
    D = gm - dbeta
    
    ff = 1.0/np.sqrt( 2* gm * D )
    iD = 1j * D
    Cs = np.conjugate(C)
    
    T = ff * np.matrix( [ [C, iD], [ iD, Cs ]] )
    Tinv = ff * np.matrix( [[Cs, -iD],[-iD,C]] )
    
    # check
    # S = np.dot( T, Tinv )
    # print S
    
    lmda = np.exp( 1j*theta )
    
    LL = np.matrix( [[lmda, 0],[0, np.conjugate(lmda)]] )
    
    # V = T . LL . T^{-1}
    tmp = np.dot( T, LL )
    V = np.dot( tmp, Tinv )
    
    iDelta2 = 1j*Delta/2.0
    X10 = np.cos(phi) * np.exp( -iDelta2 )
    X20 = np.sin(phi) * np.exp( iDelta2 )
    
    X = np.matrix( [[X10], [X20]] )
    
    Xz = np.dot( V, X )
    
    # print Xz
    (X1z,X2z) = (Xz[0,0], Xz[1,0])
    
    # s0 = np.abs(X1z)**2 + np.abs(X2z)**2
    # print s0
    s1 = np.abs(X1z)**2 - np.abs(X2z)**2
    # print s1
    s1 = s1.flatten()
    
    stmp = 2 * np.conjugate(X1z) * X2z
    # print stmp
    
    (s2,s3) = (stmp.real.flatten(), stmp.imag.flatten())
    
    return (s1,s2,s3)

# ===================================================
if __name__ == '__main__':
    
    fig = plt.figure()
    ax = fig.add_subplot(111,  aspect='equal' )
    
    # normalized \delta\beta to 1
    dbeta = 1.0
    om = 0.35 * np.pi
    Cabs = 0.2
    
    phi = 0.25 * np.pi
    Delta = 1.3 * np.pi
    
    da = np.pi/100
    theta = np.arange(0, np.pi + da, da )
    
    (s1,s2,s3) = trajectory( dbeta, Cabs, om, phi, Delta, theta)
    ax.plot( s2, s3, '-' )
    
    plt.grid()
    plt.show()
    
