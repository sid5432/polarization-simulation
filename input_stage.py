#!/usr/bin/python
import numpy as np

"""
calculate the amplitudes of Ex and Ey after a linearly polarized field
passes through a loss-less input stage.  The input field is tilted wrt
the x-y axes at an angle beta (radians).  The transformation is (th is theta)

Q = exp(-i varphi) [ exp(+i phi) 0           ][  cos(th)  sin(th) ][ exp(+i delta) 0             ]
                   [ 0           exp(-i phi) ][ -sin(th)  cos(th) ][ 0             exp(-i delta) ]
                   
we are only interested in the amplitudes (absolute value), so we only need to consider the effects of

Q_1 = [  cos(th)  sin(th) ][ exp(+i delta) 0             ]
      [ -sin(th)  cos(th) ][ 0             exp(-i delta) ]

(the other factors are just phase differences, which will be absorbed into the phase delay in the PM fiber
when perturbation is applied).

amplitudes() calculate the amplitudes |Ex|, |Ey| of the electric field upon exiting the
input stage (described by Q).

"""
def amplitudes(beta, delta, theta):
    t = np.exp( +1j * delta )
    x1 = np.cos(beta)*t # times np.exp( +1j * delta )
    x2 = np.sin(beta)/t # times np.exp( -1j * delta )
    
    cs = np.cos(theta)
    sn = np.sin(theta)
    a1 = np.abs(cs*x1 + sn*x2)
    a2 = np.abs(-sn*x1 + cs*x2)
        
    return a1,a2

# ====================================================
if __name__ == '__main__':
    import pylab as plt
    beta = np.arange( 0, np.pi, 0.01 )
    delta = np.pi/8.0;
    theta = np.pi/3.0;
    
    a1, a2 = amplitudes( beta, delta, theta)
    
    # plt.xkcd()
    plt.plot(beta/np.pi*180.0, a1, label='a1')
    plt.plot(beta/np.pi*180.0, a2, label='a2')
    
    # expected min and max
    cmin = 0.5 * ( 1.0 - np.sqrt( np.cos(2.0*theta)**2 + \
                                 np.sin(2.0*theta)**2 * np.cos(2.0*delta)**2 ) )
    cmax = 1.0 - cmin
    cmin = np.sqrt(cmin)
    cmax = np.sqrt(cmax)
    
    # plot
    plt.plot( [0,180], [cmin,cmin], '--', label='min' )
    plt.plot( [0,180], [cmax,cmax], '--', label='max' )
    plt.ylim( 0, 1.1 )
    plt.xlabel(r'$\theta$ (degrees)')
                    
    plt.legend()
    plt.draw()
    plt.show()
    
    
    
    
    
