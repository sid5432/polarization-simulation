#!/usr/bin/env python
import numpy as np
import logging
import sys

import vtk
import mayavi.mlab as mlab

from traits.api import HasTraits, Range, Instance, on_trait_change
from traitsui.api import View, Item, HGroup, VGroup

from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

import version
import transform
import poincare
import input_stage

# phase perturbation on cable
delta_pt = np.arange( -np.pi, np.pi+0.05, 0.05 )
cvtfactor = np.pi/180.0

def calc(a1,a2,delta=0,theta=0,phi=0):
    # convert deg to radians
    delta *= cvtfactor
    theta *= cvtfactor
    phi   *= cvtfactor
    
    Ey = a2 * np.exp( 1.0j * delta_pt )
    Ex = a1 * np.ones_like( Ey )
    
    Ex, Ey = transform.unitary( Ex, Ey, th_rot=theta, phi_dl=phi, delta=delta )
    chi2, psi2 = transform.poincare(Ex, Ey)
    s1, s2, s3 = poincare.sphere_coord( chi2, psi2 )
    
    return s1,s2,s3

class Visualization(HasTraits):
    # sliders for adjustable parameters
    # alternative: mode='spinner'
    
    theta_1 = Range(-90, 90, 8, label='I/P theta', desc='Input stage rotation angle', mode='slider')
    delta   = Range(-90, 90, 4, label='I/P delta', desc='Input stage phase delay', mode='slider')
    
    beta    = Range(-90, 90, 12, label='I/P rot', desc='Input stage lin pol rot angle', mode='slider')
    
    a1, a2 =  0, 1
    
    theta = Range(-90, 90,  0, label='O/P theta', desc='Output stage rotation angle', mode='slider')
    phi   = Range(-90, 90, 0, label='O/P phi', desc='Output stage phase delay', mode='slider')
    scene = Instance(MlabSceneModel, ())
    
    def __init__(self):
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self)
        
        # initialize scene?
        self.scene.disable_render = True
        self.pt_source = mlab.pipeline.scalar_scatter(1, 1, 1, 1, figure = self.scene.mayavi_scene)
        self.scene.disable_render = False
        
        # self.scene.mlab.cfg(figure = self.scene.mayavi_scene)
        return
    
    @on_trait_change('scene.activated')
    def activate_trajectory_scene(self):
        self.scene.mlab.axes(self.pt_source,
                             x_axis_visibility=False, y_axis_visibility=False, z_axis_visibility=False)
        # self.scene.mlab.orientation_axes(xlabel='S1',ylabel='S2',zlabel='S3')
        xbeta  = self.beta * cvtfactor
        xdelta = self.delta * cvtfactor
        xtheta = self.theta_1 * cvtfactor
        self.a1, self.a2 = input_stage.amplitudes( xbeta, xdelta, xtheta )
        
        x,y,z = calc(self.a1, self.a2, theta=self.theta, phi=self.phi)
        self.plot = self.scene.mlab.plot3d(x, y, z, tube_radius=0.01, color=poincare.orange)
        
        poincare.plot_grid(Xmlab=self.scene.mlab)
        poincare.land_marks(Xmlab=self.scene.mlab, figure=self.scene.mayavi_scene)
        
        self.scene.mlab.view( azimuth=45, elevation=54, distance=5.5 )
        # self.scene.reset_zoom()
        
        return
        
    @on_trait_change('theta_1,delta,beta,theta,phi')
    def update_plot(self):
        xbeta  = self.beta * cvtfactor
        xdelta = self.delta * cvtfactor
        xtheta = self.theta_1 * cvtfactor
        self.a1, self.a2 = input_stage.amplitudes( xbeta, xdelta, xtheta )
        
        x, y, z = calc(self.a1, self.a2, theta=self.theta, phi=self.phi)
        self.plot.mlab_source.set(x=x, y=y, z=z)
        return
    
    # the layout of the dialog created
    title = "PER Simulation ("+version.version+")"
    
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=350, width=400, resizable=True, show_label=False),
                VGroup(
                       Item('_'),
                       Item('theta_1'), # IP rot angle
                       Item('delta'),   # IP phase delay
                       Item('beta'),    # IP linpol orient
                       Item('theta'),   # OP rot angle
                       Item('phi') ),   # OP phase
                title=title,
                resizable=True,
                scrollable=True
               )

# =======================================================================
# logging: ref: https://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
#
class StreamToLogger(object):
       """
       Fake file-like stream object that redirects writes to a logger instance.
       """
       def __init__(self, logger, log_level=logging.INFO):
           self.logger = logger
           self.log_level = log_level
           self.linebuf = ''
           
           def write(self, buf):
               for line in buf.rstrip().splitlines():
                   self.logger.log(self.log_level, line.rstrip())
                   
logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                    filename="log_per_sim.log",
                    # filemode='a'
                   )

# =======================================================================
# main
if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '-h':
        print("HINT: set environment variables ETS_TOOLKIT to 'qt4' or 'wx'")
        print("      for 'qt4', try setting QT_API to 'pyqt', 'pyqt5', 'pyside', or 'pyside2'")
        
    # redirect output to log file
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl
     
    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl
    
    visualization = Visualization()
    visualization.configure_traits()
