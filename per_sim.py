#!/usr/bin/python
import numpy as np
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
    # a2 is fixed
    a2    = 10.0
    
    # sliders for adjustable parameters
    # alternative: mode='spinner'
    a1    = Range(1, 100, 100, label='a1', desc='E_x amplitude (E_y=4.0)', mode='slider')
    theta = Range(-90, 90,  0, label='theta', desc='Rotation angle', mode='slider')
    phi   = Range(-90, 90, 0, label='phi', desc='Phase delay', mode='slider')
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
        
        x,y,z = calc(self.a1, self.a2, theta=self.theta, phi=self.phi)
        self.plot = self.scene.mlab.plot3d(x, y, z, tube_radius=None, color=poincare.orange)
        
        poincare.plot_grid(Xmlab=self.scene.mlab)
        poincare.land_marks(Xmlab=self.scene.mlab, figure=self.scene.mayavi_scene)
        
        self.scene.mlab.view( azimuth=45, elevation=54, distance=5.5 )
        # self.scene.reset_zoom()
        
        return
        
    @on_trait_change('a1,theta,phi')
    def update_plot(self):
        x, y, z = calc(self.a1, self.a2, theta=self.theta, phi=self.phi)
        self.plot.mlab_source.set(x=x, y=y, z=z)
        return
    
    # the layout of the dialog created
    title = "PER Simulation ("+version.version+")"
    
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=350, width=400, resizable=True, show_label=False),
                VGroup(
                       Item('_'),
                       Item('a1'),
                       Item('theta'),
                       Item('phi') ),
                title=title,
                resizable=True,
                scrollable=True
               )
    

# main
if __name__ == '__main__':
    # redirect output to log file
    output = vtk.vtkFileOutputWindow()
    output.SetFileName("log.txt")
    # vtk.vtkOutputWindow().SetInstance(output)
    output.SetInstance(output)
    
    visualization = Visualization()
    visualization.configure_traits()
