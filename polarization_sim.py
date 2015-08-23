#!/usr/bin/python
import sys
import numpy as np
from matplotlib import patches
from matplotlib.widgets import Slider,Button
import pylab as plt
import time
# add this for windows pyinstaller
import FileDialog

version = "2015-06-03"

def ellipse(a1,a2,delta):
    tau = np.arange(0, np.pi*2.01, np.pi/200)
    x = a1 * np.cos( tau )
    y = a2 * np.cos( tau + delta )
    
    return x,y

def enclose_box(a1,a2):
    x = np.array([-a1,-a1, a1,  a1, -a1])
    y = np.array([-a2, a2, a2, -a2, -a2])
    return x, y    

def my_axes(psi, r):
    xm = r*np.cos(psi)
    ym = r*np.sin(psi)
    x = np.array( [ -xm, xm ] )
    y = np.array( [ -ym, ym ] )
    return x, y

def make_ellipse(a1,a2,delta, ax=None):
    # delta is given in degrees!
    
    if ax == None:
        print "make_ellipse(): ax not defined; cannot plot!"
        return
    
    if delta == 0 or abs(delta) == 180.0:
        polstate = "linear"
    elif delta > 0:
        polstate = "clockwise"
    else:
        polstate = "counter-clockwise"
    
    ax.cla()
    ax.set_title(r'$\delta$ = %.1f deg (%s)' % (delta,polstate) )
    ax.set_xlim([-12,12])
    ax.set_ylim([-6,6])
    
    delta = delta * np.pi/180.0 # convert to radians
    
    x, y = ellipse(a1,a2,delta)
    ax.plot( x,y, color='black')
    
    # box
    x,y = enclose_box(a1,a2)
    ax.plot( x,y, '-.', color='blue' )
    
    # tilt axes
    alpha = np.arctan(a2/a1)
    # print "MAIN: alpha = %.3f deg" % (alpha*180.0/np.pi)
    alpha2 = 2.0 * alpha
    
    chi = 0.5 * np.arcsin( np.sin(alpha2) * np.sin(delta) )
    # print "MAIN: ellipticity angle chi = %.3f deg" % (chi*180.0/np.pi)
    
    psi = 0.5 * np.arctan( np.tan(alpha2) * np.cos(delta) )
    
    if a2 > a1:
        if np.abs(delta)<np.pi/2.0:
            psi += np.pi/2.0
        else:
            psi -= np.pi/2.0
    
    # print "MAIN: tilt psi = %.3f deg" % (psi*180.0/np.pi)
    r = np.sqrt( a1**2 + a2**2 )
    a = r * np.cos(chi)
    b = r * np.sin(chi)
    # print "MAIN: a = %.3f, b = %.3f" % (a,b)
    
    # x,y axis
    x,y = my_axes( 0, 1.1*a1)
    ax.plot( x,y, color='blue')

    x,y = my_axes( np.pi/2.0, 1.1*a2)
    ax.plot( x,y, color='blue')
    
    x,y = my_axes( psi, 1.1*a)
    ax.plot( x,y, color='red')
    
    x,y = my_axes( psi+np.pi/2.0, 1.2*b)
    ax.plot( x,y, color='red')
    
    # drop lines
    x = np.array([ a*np.cos(psi), -b*np.sin(psi) ])
    y = np.array([ a*np.sin(psi),  b*np.cos(psi) ])
    ax.plot( x,y, color='green')
    
    x = np.array([ -a1, 0.0 ])
    y = np.array([ 0.0, -a2 ])
    ax.plot( x,y, color='orange')
    
    # annotation
    # ax.annotate(r'$x$', xy=(a1,0), xytext=(a1+0.1, 0.1), fontsize='x-large' )
    ax.annotate(r'$x$', xy=(a1,0), xytext=(a1+0.1, 0.1), fontsize=20 )
    ax.annotate(r'$y$', xy=(0,a2), xytext=(0.1, a2+0.2), fontsize=20 )
    
    # tilted axes labels
    xt, yt = 1.1*a*np.cos(psi), 1.1*a*np.sin(psi),
    ax.annotate(r'$\xi$', xy=(xt,yt), xytext=(xt+0.1, yt+0.2), fontsize=20 )
    xt, yt = -1.2*b*np.sin(psi), 1.2*b*np.cos(psi),
    ax.annotate(r'$\eta$', xy=(xt,yt), xytext=(xt-0.3, yt+0.3), fontsize=20 )
    
    # tilted axes length
    xt, yt = a*np.cos(psi), a*np.sin(psi),
    ax.annotate(r'$a$', xy=(xt,yt), xytext=(xt-0.1, yt+0.3), fontsize=20 )
    xt, yt = -b*np.sin(psi), b*np.cos(psi),
    ax.annotate(r'$b$', xy=(xt,yt), xytext=(xt-0.1, yt+0.3), fontsize=20 )
    
    # original axes length
    xt, yt = a1, -a2
    ax.annotate(r'$a_1$', xy=(xt,yt), xytext=(xt-0.2, yt-0.6), fontsize=20 )
    xt, yt = -a1, a2
    ax.annotate(r'$a_2$', xy=(xt,yt), xytext=(xt-0.7, yt-0.1), fontsize=20 )

    # angle arcs
    cent = [ 0, 0 ]
    theta1 = 0
    theta2 = psi*180.0/np.pi # deg!
    if theta2 < theta1:
        tmp = theta2
        theta2 = theta1
        theta1 = tmp
    
    arc1 = patches.Arc( cent, 2.0, 2.0, 0, theta1, theta2, linewidth=2, color='red', label=r'$\psi')
    ax.add_patch(arc1)
    xt, yt = 1.0, 0.0
    ax.annotate(r'$\psi$', xy=(xt,yt), xytext=(xt+0.1, yt+0.2), fontsize=20 )
    
    # chi angle
    cent = [ a*np.cos(psi), a*np.sin(psi) ]
    theta2 = (np.pi + psi)*180.0/np.pi # deg!
    theta1 = theta2 - chi*180.0/np.pi
    if theta1 > theta2:
        tmp = theta1
        theta1 = theta2
        theta2 = tmp
    
    arc1 = patches.Arc( cent, 2.0, 2.0, 0, theta1, theta2, linewidth=2, color='green', label=r'$\chi')
    ax.add_patch(arc1)
    xt, yt = cent
    ax.annotate(r'$\chi$', xy=(xt,yt), xytext=(xt-1.8, yt-0.6), fontsize=20 )

    cent = [ -a1, 0 ]
    theta2 = 0
    theta1 = -alpha*180.0/np.pi # deg!
    arc1 = patches.Arc( cent, 2.0, 2.0, 0, theta1, theta2, linewidth=2, color='orange', label=r'$\alpha')
    ax.add_patch(arc1)
    xt, yt = cent
    ax.annotate(r'$\alpha$', xy=(xt,yt), xytext=(xt+1.2, yt-0.5), fontsize=20 )
    
    # text
    ax.text(-12,-8,r'$\chi$ = %.3f $^\circ$' % (chi*180.0/np.pi) )
    ax.text(-5,-8,r'$\psi$ = %.3f $^\circ$' % (psi*180.0/np.pi) )
    ax.text( 5,-8,r'$\alpha$ = %.3f $^\circ$' % (alpha*180.0/np.pi) )
    
    ax.text(-12,-9.5,r'(major) $a$ = %.3f' % a )
    ax.text(-5,-9.5,r'(minor) $b$ = %.3f' % b )
    
    # finish
    ax.figure.canvas.draw()
    
    return

def quit(event):
    sys.exit()
    return

# -----------------------------------------------------------
class MySlider(Slider):
    """Slider with discrete steps (to integer)"""
    def __init__(self, *args, **kwargs):
        self.inc = kwargs.pop('increment', 1.0)
        self.param = kwargs.pop('param')
        self.item  = kwargs.pop('item')
        
        self.val = None
        Slider.__init__(self,*args, **kwargs)
        self.on_changed( self.replot )
        
        return
    
    def set_val(self,val):
        discrete_val = int( val/self.inc )* self.inc
        
        if self.val == None:
            # new value
            self.val = discrete_val
            # print "\tinit current: %.1f" % self.val
        else: # compare with current
            if discrete_val == self.val:
                # pass
                return
            else:
                self.val = discrete_val
        
        # print "\tcurrent: %.1f" % self.val
        
        # update Slider appearance
        xy = self.poly.xy
        xy[2] = discrete_val, 1
        xy[3] = discrete_val, 0
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % discrete_val)
        if self.drawon: 
            self.ax.figure.canvas.draw()
        if not self.eventson: 
            return
        for cid, func in self.observers.iteritems():
            func(discrete_val)
        
        return
    
    # -----------------------------------------------------------
    def replot(self,val):
        # update 
        self.param[self.item] = self.val
        # print "replot(from %s): a1 %.2f, a2 %.2f, delta %.2f" % \
        (self.item, self.param['a1'], self.param['a2'], self.param['delta'])
        
        make_ellipse(self.param['a1'], self.param['a2'], self.param['delta'], ax=ax)
        return
    

# ====================================================
if __name__ == '__main__':
    """
    This program simulates the polarzation 
    """
    
    a1,a2,delta = 5.0,4.0,60.0
    
    fig = plt.figure("Polarization Simulation (%s)" % version)
    ax  = fig.add_axes([0.10,0.25,0.75,0.75],aspect='equal')
    fig.suptitle("Polarization Simulation")
    
    ax_quit = fig.add_axes([0.05,0.05,0.12,0.06])
    quit_button = Button(ax_quit,'Quit',color='#FF0000',hovercolor='0.975')
    quit_button.on_clicked( quit )
    
    param = { "a1": a1, "a2": a2, "delta": delta }
    
    ax_slide1 = fig.add_axes([0.32,0.05,0.50,0.05])
    # slide1 = Slider(ax_slide1, r'$\delta$ (deg)', valfmt='%.0f',valmin=-180, valmax=180, valinit=0)
    slide1 = MySlider(ax_slide1, r'$\delta$ (deg)',
                      param=param, increment=2.0, item='delta',
                      valfmt='%.1f',valmin=-180, valmax=180, valinit=delta)
    
    ax_slide2 = fig.add_axes([0.32,0.12,0.50,0.05])
    # slide1 = Slider(ax_slide1, r'$\delta$ (deg)', valfmt='%.0f',valmin=-180, valmax=180, valinit=0)
    slide2 = MySlider(ax_slide2, r'$a_1$',
                      param=param, increment=0.1, item='a1',
                      valfmt='%.2f',valmin=1, valmax=10, valinit=a1)
    
    make_ellipse(a1,a2, delta, ax=ax)
    
    plt.show()
    
    
    
