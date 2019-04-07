#!/usr/bin/python
import numpy as np

def poincare(Ex, Ey, debug=False):
    """
    Ex, Ey are in fields in X and Y, in complex numbers;
    a1 is the amplitude of Ex, a2 is the amplitude of Ey, and
    delta is the phase difference between Ey and Ex
    """
    a1 = np.abs(Ex)
    a2 = np.abs(Ey)
    
    # handle Ex=0
    idx = np.where( a1 != 0 )
    delta = np.zeros_like( Ex )
    delta[idx] = np.angle(Ey[idx]/Ex[idx])
    
    if debug:
        print( "a1 = %.3f, a2 = %.3f, delta = %.3f " % ( a1,a2,delta ) )
    # NOTE: delta is between -pi and +pi
    
    alpha2 = 2.0*np.arctan2( a2, a1 )
    chi2 = np.arcsin( np.sin(alpha2) * np.sin(delta) )
    psi2 = np.arctan( np.tan(alpha2) * np.cos(delta) )
    
    # adjustments: case 1: a1 < a2 and |delta| < pi/2
    idx = np.where( np.logical_and(a1 < a2, np.abs(delta)<=np.pi/2.0 ) )
    psi2[idx] += np.pi
    
    idx = np.where( np.logical_and(a1 < a2, np.abs(delta)>np.pi/2.0 ) )
    psi2[idx] -= np.pi
    
    # the imaginary part should theoretically be zero
    return chi2.real, psi2.real

# -------------------------------------------------
# delta: phase delay (T1)
# th_rot: rotation angle (T2)
# phi_dl: another phase delay (T3)
def unitary( Ex, Ey, th_rot=0.26, phi_dl=0.15, delta=0  ):
    Ex1 = Ex * np.exp( 1.0j* delta )
    Ey1 = Ey * np.exp( -1.0j* delta )
    
    cs = np.cos(th_rot)
    sn = np.sin(th_rot)
    
    Ex2 =  Ex1*cs + Ey1*sn
    Ey2 = -Ex1*sn + Ey1*cs
    
    Ex_new = Ex2 * np.exp( 1.0j* phi_dl )
    Ey_new = Ey2 * np.exp( -1.0j* phi_dl )
    
    return Ex_new, Ey_new

# ==============================================================
if __name__ == '__main__':
    # print "TEST: scalar"
    # Ex = 1.0 + 0.2j
    # Ey = 1.0 - 0.2j
    
    # a1,a2, delta = f1(Ex, Ey)
    # print "TEST: got a1 = ",a1," a2 = ",a2," delta = ", (delta*180.0/np.pi)

    print( "TEST: array" )
    Ex = np.array([ 1.0 + 0.2j, 1.0 - 0.2j, 1.0 + 0.2j, 0.0 ])
    Ey = np.array([ 1.0 - 0.2j, 1.0 + 0.2j, 1.0 - 0.2j, 1.0 ])
    
    chi2, psi2 = poincare(Ex, Ey)
    
    print( "TEST: ellipticity    chi ", chi2/2.0 )
    print( "TEST: azimuth (tilt) psi ", psi2/2.0 )

    

