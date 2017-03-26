#!/usr/bin/python
import numpy as np
import vtk
import wx
from wx.combo import OwnerDrawnComboBox as ComboBox

from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item

from mayavi import mlab
from mayavi.core.ui.api import SceneEditor, MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

import poincare
import propagate
import version3

# --------------------------------------------------------------------------
class MayaviView(HasTraits):

    scene = Instance(MlabSceneModel, ())
    
    # The layout of the panel created by Traits
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene), 
                     resizable=True,
                     show_label=False))

    def __init__(self, parent):
        da = np.pi/50
        self.theta = np.arange(0, np.pi + da, da )
        self.cfactor = np.pi/180.0
        
        HasTraits.__init__(self)
        self.parent = parent
        mlab.clf(figure = self.scene.mayavi_scene)
        
    @on_trait_change('scene.activated')
    def activate_trajectory_scene(self):
        mlab.axes(self.pt_source,
                  x_axis_visibility=False, y_axis_visibility=False, z_axis_visibility=False)  
        
        self.cabs  = self.parent.control_panel.cabs_control.GetValue() * 0.01
        self.omega = self.parent.control_panel.omega_control.GetValue() * self.cfactor
        self.phi   = self.parent.control_panel.phi_control.GetValue() * self.cfactor
        self.Delta = self.parent.control_panel.Delta_control.GetValue() * self.cfactor
        
        x,y,z = propagate.trajectory( 1.0, self.cabs, self.omega, self.phi, self.Delta, self.theta )
        self.plot = self.scene.mlab.plot3d(x, y, z, tube_radius=None, color=poincare.orange)
        
        ex,ey,ez = propagate.ev(1.0, self.cabs, self.omega, self.phi, self.Delta)
        self.plot2 = self.scene.mlab.plot3d(ex, ey, ez, tube_radius=None, color=poincare.yellow)
        
        # self.text = mlab.text3d(1,1,1, str(self.parent.number_to_show), figure = self.scene.mayavi_scene)        
        poincare.plot_grid(Xmlab=mlab)
        poincare.land_marks(Xmlab=mlab, figure=self.scene.mayavi_scene)
        
        # mlab.view(distance='auto', figure = self.scene.mayavi_scene)
        self.scene.mlab.view( azimuth=45, elevation=54, distance=5.5 )
        # self.scene.reset_zoom()
        # self.update_scene()
        
    def initialize_scene(self,n):
        self.scene.disable_render = True
        
        self.pt_source = mlab.pipeline.scalar_scatter(1, 1, 1, 1, figure = self.scene.mayavi_scene)
         
        # Every object has been created, we can reenable the rendering.
        self.scene.disable_render = False
        return
        
    def update_scene(self):
        
        self.cabs  = self.parent.control_panel.cabs_control.GetValue() * 0.01
        self.omega = self.parent.control_panel.omega_control.GetValue() * self.cfactor
        self.phi   = self.parent.control_panel.phi_control.GetValue() * self.cfactor
        self.Delta = self.parent.control_panel.Delta_control.GetValue() * self.cfactor
        
        x,y,z = propagate.trajectory(1.0, self.cabs, self.omega, self.phi, self.Delta, self.theta)
        self.plot.mlab_source.set(x=x, y=y, z=z)
        
        ex,ey,ez = propagate.ev(1.0, self.cabs, self.omega, self.phi, self.Delta)
        self.plot2.mlab_source.set(x=ex, y=ey, z=ez)
        
        return

################################################################################
class ControlPanel(wx.Panel):
    
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        
        # Add sliders
        text_width = 40
        slide_width = 500
        space1 = 40
        
        ypos1 = 20
        xpos1 = 10
        ypos2 = ypos1 - 20
        xpos2 = xpos1 + text_width + 10
        
        wx.StaticText(self, -1, "|C|:", size=(text_width,-1), pos=(xpos1,ypos1) )
        self.cabs_control = wx.Slider(self, id=wx.ID_ANY, value=20, minValue=1, maxValue=100,
                                    size=(slide_width,-1), name="cabs", pos=(xpos2,ypos2),
                                    style=wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SL_TICKS|wx.SL_BOTH|wx.EXPAND)
        
        ypos1 += space1
        ypos2 += space1
        wx.StaticText(self, -1, "arg C:", size=(text_width,-1), pos=(xpos1,ypos1) )
        self.omega_control = wx.Slider(self, id=wx.ID_ANY, value=63, minValue=-90., maxValue=90,
                                       size=(slide_width,-1), name="omega",pos=(xpos2,ypos2),
                                       style=wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SL_TICKS|wx.SL_BOTH)
        
        ypos1 += space1
        ypos2 += space1
        wx.StaticText(self, -1, "phi:", size=(text_width,-1), pos=(xpos1,ypos1) )
        self.phi_control = wx.Slider(self, id=wx.ID_ANY, value=0, minValue=-90, maxValue=90,
                                     size=(slide_width,-1), name="phi",pos=(xpos2,ypos2),
                                     style=wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SL_TICKS|wx.SL_BOTH)

        ypos1 += space1
        ypos2 += space1
        wx.StaticText(self, -1, "Delta:", size=(text_width,-1), pos=(xpos1,ypos1) )
        self.Delta_control = wx.Slider(self, id=wx.ID_ANY, value=0, minValue=-90, maxValue=90,
                                     size=(slide_width,-1), name="Delta",pos=(xpos2,ypos2),
                                     style=wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SL_TICKS|wx.SL_BOTH)

        self.Layout()
        self.Show(True)
        return
    
# ----------------------------------------------------------------
class MainWindow(wx.Frame):

    def __init__(self, parent, id, size=(600,600)):
        title = "PM Fiber PER Simulation (Mayavi/Wx "+version3.version+")"
        wx.Frame.__init__(self, parent, id, title, size=size)
        
        self.control_panel = ControlPanel(self)
        
        self.number_to_show = 33
        print 'Currently selected number: %d' % self.number_to_show
        
        # Define events
        wx.EVT_SLIDER(self.control_panel.cabs_control, -1, self.param_change)
        wx.EVT_SLIDER(self.control_panel.omega_control, -1, self.param_change)
        wx.EVT_SLIDER(self.control_panel.phi_control, -1, self.param_change)
        wx.EVT_SLIDER(self.control_panel.Delta_control, -1, self.param_change)
        
        self.mayavi_view = MayaviView(self)
        self.mayavi_view.text = None
        self.mayavi_view.initialize_scene(self.number_to_show)            
        
        self.figure_panel = self.mayavi_view.edit_traits(
                        parent=self,
                        kind='subpanel').control
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.figure_panel, 1, wx.EXPAND)        
        sizer.Add(self.control_panel, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)        
        
        self.Show(True)

    def param_change(self, event=None):
        self.mayavi_view.update_scene()
        
        return

# ===================================================
if __name__ == '__main__':
    output = vtk.vtkFileOutputWindow()
    output.SetFileName("log3.txt")
    vtk.vtkOutputWindow().SetInstance(output)

    app = wx.PySimpleApp()
    frame = MainWindow(None, wx.ID_ANY)
    app.MainLoop()

