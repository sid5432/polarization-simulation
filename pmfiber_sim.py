#!/usr/bin/env python
import sys
import numpy as np
import logging

import vtk
from mayavi import mlab

from traits.api import HasTraits, Range, Instance, on_trait_change
from traitsui.api import View, Item, HGroup, VGroup

from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

import poincare
import propagate
import version3

# --------------------------------------------------------------------------
class Visualization(HasTraits):
    # sliders for adjustable parameters
    # alternative: mode='spinner'

    scene = Instance(MlabSceneModel, ())
    
    cabs    = Range(1, 100, 20, label='|C|', desc='coupling coefficient (C) magnitude', mode='slider')
    omega   = Range(-90, 90, 63, label='arg C', desc='coupling coefficient (C) angle', mode='slider')
    phi     = Range(-90, 90, 0, label='phi', desc='Input X (slow), Y (fast) axis component magnitude ratio is tan(phi)', mode='slider')
    Delta   = Range(-90, 90, 0, label='Delta', desc='Half phase difference of input X, Y components', mode='slider')

    # The layout of the panel created by Traits
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene), 
                     resizable=True,
                     show_label=False))

    def __init__(self):
        da = np.pi/50
        self.theta = np.arange(0, np.pi + da, da )
        self.cfactor = np.pi/180.0
        
        HasTraits.__init__(self)
        self.scene.disable_render = True
        self.pt_source = mlab.pipeline.scalar_scatter(1, 1, 1, 1, figure = self.scene.mayavi_scene)
        self.scene.disable_render = False
        
        return
        
    @on_trait_change('scene.activated')
    def activate_trajectory_scene(self):
        mlab.axes(self.pt_source,
                  x_axis_visibility=False, y_axis_visibility=False, z_axis_visibility=False)  
        
        xcabs  = self.cabs * 0.01
        xomega = self.omega * self.cfactor
        xphi   = self.phi * self.cfactor
        xDelta = self.Delta * self.cfactor
        
        x,y,z = propagate.trajectory( 1.0, xcabs, xomega, xphi, xDelta, self.theta )
        self.plot = self.scene.mlab.plot3d(x, y, z, tube_radius=0.01, color=poincare.orange)
        
        ex,ey,ez = propagate.ev(1.0, xcabs, xomega, xphi, xDelta)
        self.plot2 = self.scene.mlab.plot3d(ex, ey, ez, tube_radius=0.01, color=poincare.yellow)

        # self.text = mlab.text3d(1,1,1, str(self.parent.number_to_show), figure = self.scene.mayavi_scene)        
        poincare.plot_grid(Xmlab=self.scene.mlab)
        poincare.land_marks(Xmlab=self.scene.mlab, figure=self.scene.mayavi_scene)
        
        self.scene.mlab.view( azimuth=45, elevation=54, distance=5.5 )
        # self.scene.reset_zoom()
        # self.update_scene()
        
        return
        
    def initialize_scene(self,n):
        self.scene.disable_render = True
        
        self.pt_source = mlab.pipeline.scalar_scatter(1, 1, 1, 1, figure = self.scene.mayavi_scene)
         
        # Every object has been created, we can reenable the rendering.
        self.scene.disable_render = False
        return
        
    @on_trait_change('cabs,omega,phi,Delta')
    def update_scene(self):
        
        xcabs  = self.cabs * 0.01
        xomega = self.omega * self.cfactor
        xphi   = self.phi * self.cfactor
        xDelta = self.Delta * self.cfactor
        
        x,y,z = propagate.trajectory(1.0, xcabs, xomega, xphi, xDelta, self.theta)
        self.plot.mlab_source.set(x=x, y=y, z=z)
        
        return

    @on_trait_change('cabs,omega')
    def update_scene2(self):
        
        xcabs  = self.cabs * 0.01
        xomega = self.omega * self.cfactor
        xphi   = self.phi * self.cfactor
        xDelta = self.Delta * self.cfactor
        
        ex,ey,ez = propagate.ev(1.0, xcabs, xomega, xphi, xDelta)
        self.plot2.mlab_source.set(x=ex, y=ey, z=ez)
        
        return

    # the layout of the dialog created
    title = "PM Fiber PER Simulation ("+version3.version+")"
    
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=350, width=400, resizable=True, show_label=False),
                VGroup(
                       Item('_'),
                       Item('cabs'),   # |C|
                       Item('omega'),  # C angle
                       Item('phi'),    # phi
                       Item('Delta') ),  # Delta
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
                    filename="log_pmfiber.log",
                    # filemode='a'
                   )
    
# ===================================================
if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '-h':
        print("HINT: set environment variables ETS_TOOLKIT to 'qt4' or 'wx'")
        print("      for 'qt4', try setting QT_API to 'pyqt', 'pyqt5', 'pyside', or 'pyside2'")
    
    # redirect output to log file
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl
    
    # stderr_logger = logging.getLogger('STDERR')
    # sl = StreamToLogger(stderr_logger, logging.ERROR)
    # sys.stderr = sl
    
    visualization = Visualization()
    visualization.configure_traits()

