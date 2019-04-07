#!/usr/bin/python
import numpy as np
import mayavi.mlab as mlab

black = (0,0,0) # black
red   = (1,0,0)
green = (0,1,0)
blue  = (0,0,1)
cyan  = (0,1,1)
orange = (1, 0.647, 0)
yellow = (1,1,0)

def sphere_coord(chi2, psi2):
    """
    tan(chi) = b/a: ellipticity
    tan(alpha) = a2/a1
    psi: tilt angle
    """
    # chi2 = chi*2
    # psi2 = psi*2
    tmp = np.cos(chi2) 
    s1 = tmp * np.cos(psi2)
    s2 = tmp * np.sin(psi2)
    s3 = np.sin(chi2)
    
    return s1,s2,s3

# ------------------------------------------------------------------
def plot_grid(Xmlab=mlab):
    
    # plot equator
    psi2 = np.arange( 0, 2.01*np.pi, 0.01 )
    chi2 = np.zeros_like(psi2)
    s1, s2, s3 = sphere_coord( chi2, psi2 )
    
    Xmlab.plot3d( s1, s2, s3, tube_radius=None, color=black )
    # Xmlab.points3d( s1, s2, s3, color=(0,0,1), mode='sphere', scale_factor=0.01, line_width=0.1 )

    # plot longitude 0 -------------------------------------
    chi2 = np.arange( 0, 2.01*np.pi, np.pi/50.0 )
    psi2 = np.zeros_like(chi2)
    s1, s2, s3 = sphere_coord( chi2, psi2 )
    
    # Xmlab.plot3d( s1, s2, s3, tube_radius=None, color=(0,0,1) )
    Xmlab.points3d( s1, s2, s3, color=black, mode='sphere', scale_factor=0.01, line_width=0.1 )
    
    # plot longitude 90 -------------------------------------
    chi2 = np.arange( 0, 2.01*np.pi, np.pi/50.0 )
    psi2 = np.ones_like(chi2) * np.pi * 0.5;
    s1, s2, s3 = sphere_coord( chi2, psi2 )
    
    # Xmlab.plot3d( s1, s2, s3, tube_radius=None, color=(0,0,1) )
    # Xmlab.points3d( s1, s2, s3, color=(0,0,1), mode='point', line_width=0.1 )
    Xmlab.points3d( s1, s2, s3, color=black, mode='sphere', scale_factor=0.01, line_width=0.1 )
    
    # xyz axes
    x = np.arange( -1.0, 1.2, 0.2 )
    z = np.zeros_like(x)
    
    Xmlab.plot3d(x,z,z, tube_radius=None, color=red)
    Xmlab.plot3d(z,x,z, tube_radius=None, color=green)
    Xmlab.plot3d(z,z,x, tube_radius=None, color=blue)
    
    # create a sphere
    r = 1.0
    psi, theta = np.mgrid[ 0:np.pi:101j, 0:2*np.pi:101j ]
    sp = r * np.sin(psi)
    x = sp * np.cos(theta)
    y = sp * np.sin(theta)
    z = r* np.cos(psi)
    s = np.abs(z)
    
    # Xmlab.mesh( x,y,z, scalars=s, colormap='jet', opacity=0.4 )
    Xmlab.mesh( x,y,z, scalars=s, colormap='Blues', opacity=0.4 )
    return

# ------------------------------------------------------------------
def p_trajectory( s1, s2, s3, color=orange ):
    # mlab.plot3d( s1, s2, s3, tube_radius=0.01 )
    mlab.plot3d( s1, s2, s3, tube_radius=None, color=color )
    return

# ------------------------------------------------------------------
def land_marks(Xmlab=mlab,figure=None):
    
    rad = 1.3
    x,y,z = rad, 0, 0
    if figure == None:
        t1 = Xmlab.text3d(x,y,z,'H',scale=0.1)
    else:
        t1 = Xmlab.text3d(x,y,z,'H',scale=0.1, figure=figure)
    
    t1.vector_text.update()
    
    x,y,z = -rad,0,0
    if figure == None:
        t2 = Xmlab.text3d(x,y,z,'V',scale=0.1)
    else:
        t2 = Xmlab.text3d(x,y,z,'V',scale=0.1, figure=figure)
    
    t2.vector_text.update()
    
    # R: clockwise (right-hand circular)
    x,y,z = 0, 0, rad
    if figure == None:
        t3 = Xmlab.text3d(x,y,z,'R',scale=0.1)
    else:
        t3 = Xmlab.text3d(x,y,z,'R',scale=0.1, figure=figure)
        
    t3.vector_text.update()
    
    # L: counter-clockwise (left-hand circular)
    x,y,z = 0, 0, -rad
    if figure == None:
        t4 = Xmlab.text3d(x,y,z,'L',scale=0.1) # orient_to_camera=True
    else:
        t4 = Xmlab.text3d(x,y,z,'L',scale=0.1, figure=figure) # orient_to_camera=True
    
    t4.vector_text.update()
    
    return

# ===========================================================
if __name__ == '__main__':
    print( "Test with tests/test_poincare.py")
    
