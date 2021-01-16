# polarization-simulation

These are small programs to simulate the state-of-polarization (SOP) of 

1. an optical plane wave (*polarization_sim.py*),

<img border="0" src="http://1.bp.blogspot.com/-pzUbg6zqN7Y/Vdj_j5v-8RI/AAAAAAAAAeo/xHlwX_fLyDA/s1600/ellipse.png" height="320" />

2. the SOP of light passing through a polarization maintaining (PM) optical fiber patchcord
(*per_sim.py*), and

<img border="0" src="http://1.bp.blogspot.com/-Jw_bIrsF8MI/VdkDoXaF-CI/AAAAAAAAAe4/_EwGZFg9pRg/s1600/psphere2.png" height="220" />

3. the SOP of light passing through a PM optical fiber (*pmfiber_sim.py*)

<img border="0" src="https://3.bp.blogspot.com/-7x2zjKGo2g4/WNa4PHkrf9I/AAAAAAAAAws/VIccZBFyRFwnbgCU5j3co1O71H8LxeZ4gCLcB/s320/poincare-sphere.png" height="320" />

For details on what these are all about, please see
my blog posts [part 1](http://morethanfootnotes.blogspot.com/2015/08/notes-on-measuring-polarization.html?view=sidebar)
and 
[part 2](http://morethanfootnotes.blogspot.com/2017/03/the-state-of-polarization-trajectory-of.html?view=sidebar)
at [http://morethanfootnotes.blogspot.com](http://morethanfootnotes.blogspot.com/).

The programs are Python scripts, and require [numpy](http://www.numpy.org), 
[matplotlib](http://matplotlib.org/) and
[mayavi](http://docs.enthought.com/mayavi/mayavi/). The programs have
been tested in Python 2.7.12 and Python 3.5.2, 3.6.7, and 3.7.3.


## JavaScript Version
(*Update: 2021-01-15*)

A port of the two Poincare Sphere simulations has been ported to an
interactive web page, using the [three.js](https://threejs.org) JavaScript
library. The GitHub page is at

	http://sid5432.github.io/polarization-simulation/index.html
    
click [here](http://sid5432.github.io/polarization-simulation/index.html) to 
go to the page. The entire simulation is included in the single file **index.html**;
everything (including the JavaScript code) is contained in this single file. 
However, it depend on the three.js library. 
The JavaScript code is "hot linked" to the library at threejs.org;
i.e., it pulls several JavaScript modules from the threejs.org website.

If you want to run it without internet access, you will need to get a copy of 
the three.js library and modify the script to pull from your local copy. 
But you may need to run/host the page with a web server; 
usually you will get some warning (if you look at the web console of the browser) 
that the browser is blocking the import of the JavaScript libraries because of 
"Cross-Origin Request".

If you have python installed on your computer, you should be able to start 
(on the command line) a simple web server 
(in the folder where the *.html file is saved) with the commands

    python -m http.server 

This will start a simple web server on your local computer on port 8000. 
Point your browser to https://localhost:8000/ and you should see the *.html file.
    


## Notes on Installing Matplotlib, Mayavi and Friends on Linux

> *Update: 2020-07-15*
>
> *With the new Ubuntu 20.04 and Python 3.8.3, most of the problems mentioned here 
have gone away. Nowadays I use pyenv almost exclusively; installing wxPython with pyenv 
works, and Qt5 does not cause any problem with incorrect rendering in Mayavi now. 
However, installing Mayavi with pip may fail to compile. See 
[this post at stackoverflow](https://stackoverflow.com/questions/27682120/installing-mayavi-with-pip-building-tvtk-classes-assertion-failed)
for a solution. This problem might already be fixed by the time you read this.*


The program for showing the SOP of a plane wave (the first program, *polarization_sim.py*)
uses [matplotlib](http://matplotlib.org/). This one should be easy to install. 
If you are using any of the [Ubuntu](https://www.ubuntu.com/) derivatives
(such as [Linux Mint](https://linuxmint.com/)), and assuming your are using Python3,
you should be able to just use *apt-get* to install the package:

	sudo apt-get install python3-matplotlib

(*Python2 is headed towards
obsolescence, so you might as well start migrating towards Python3. For the rest of this
discussion I will focus on Python3.*)

The other two programs for displaying the SOP on Poincaré Spheres are more problematic. They
rely on the [mayavi](http://docs.enthought.com/mayavi/mayavi/)
package, which is a little more difficult to install. for Python2,
the package is "mayavi2" (version 4.4.3-2.1 as of this writing):

	sudo apt-get install mayavi2
    
For Python3, this is a little trickier, since the package (as of this writing) is not
available throught *apt-get*; you have to use *pip* in order to install it. 
This requires first getting a few things installed through *apt-get*, including:

* python3-pip
* build-essential

The *pip* program will be installed as *pip3* (to distinguish it from *pip* for Python2). Once you
have *pip3* installed, it's a good idea to upgrade it:

	sudo pip3 install -U pip
    
which will install a new *pip* as */usr/local/bin/pip* (whereas the old Python2 pip -- if you installed
it --- will be in */usr/bin/pip* (it's confusing, I know). Make sure you invoke the right one
afterwards. 

The *sudo* part is important: if you do not run the upgrade with *sudo* (installing
it as root), the new *pip* will be installed in the (for Python3.6) 

	$HOME/.local/lib/python3.6/site-packages/
    
directory in your home directory,
and this will cause all sorts of trouble. In particular, you may find that *pip* no
longer works and report an error message about "*module has no attribute main*", 
or something similar.
If that happens, it is likely that you installed the upgrade into *$HOME/.local/lib/python3.6/site-packages*. You will find
that even running

	apt-get purge python3-pip
    
(trying to uninstall *pip3*) and then installing it again with

	apt-get install python3-pip
    
won't fix the problem --- because the new one is already stuck in the *.local* location. What you
have to do is remove the *.local* files first.

Once you have *pip3* installed and upgraded, you are ready to install the rest of the pieces.
You should be able to just run

	sudo pip3 install mayavi
    
This will build mayavi from source, and assuming you have all the necessary libraries and headers
installed already (pay attention to any warning messages), it should build successfully.
The build will pull in several other Python modules along the way, the major ones being:

* numpy (*this should have been installed along with matplotlib already*)
* traits
* traitsui
* envisage
* vtk
* pyface

You may need one more module to run the programs, even if *mayavi* and friends were
installed successfully.
If you were to run the programs requiring mayavi, you may find that it still doesn't run,
with an error message about *no pyface.toolkits plugin*. 

What that means is that you need a "GUI
component" that *pyface* calls to display the result. The easiest (as of this writing) is to use
the Qt4 module: install this with

	sudo apt-get install python3-pyqt4

This should be sufficient to have the programs run.

But the Qt4 *toolkit* isn't the only choice. The *pyface* module can actually also work with
the [wxPython](https://wxpython.org/) toolkit --- except that it is also not yet available for Python3 through *apt-get*
(as of this writing); you will need to install it through *pip3* as well:

	sudo pip3 install wxPython

But it may not work. I have run into trouble with this on Mint Linux 18.3, and my suggestion
is to stick with Qt4 for now.

The selection of using the *wx* or *Qt4* toolkit can be controlled through the environment 
variable **ETS_TOOLKIT**, although you can also force the selection in your Python script.
Set this variable to either **wx** or **qt4** to force a selection of the toolkit to use.

But what about *Qt5*? Support for *Qt5* has been out for a while, and in fact there are *four*
options for the Qt toolkit (even though the *ETS_TOOLKIT* environment variable is set to *qt4*). 
This option is set by another environment variable **QT_API**, and the options are

* pyqt (*using the older Qt4 library*)
* pyqt5 (*using the Qt5 library*)
* pyside (*another Python library/module for Qt*)
* pyside2 (*the new version of pyside that is to replace the old pyside library*)

For completeness, here is how you install these other modules and components:

	sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.opengl
    sudo apt-get install python3-pyside
    sudo pip3 install PySide2
    
(*PySide2* is not currently available through *apt-get*, and installing it through *pip3* 
will require some additional libraries and headers).

However, at this time I advise against using *pyqt5* or *pyside2*, 
simply because they don't quite work. As of this writing, if you use these two, you
may find that the depth order is incorrect (i.e, things that should be hidden behind
one object is showing up in front instead). An example is shown in the figures below:

<img border="0" 
src="https://2.bp.blogspot.com/-Xoym9SQa4Pc/XLztBWNMqmI/AAAAAAAAGOM/udOyY5Kkl_cJ-vDbF5OKFoEMk_UN6vOZACLcBGAs/s1600/shading-not-ok.png"
height="250" />
&nbsp;
<img border="0" src="https://2.bp.blogspot.com/-dIJd9lrC5Rc/XLztBdNLBZI/AAAAAAAAGOI/-JtWLKqSvzU-58PegEhEoW1xso0AJqkSgCLcBGAs/s1600/shading-ok.png"
height="250"/>

The left figure is rendered with the *pyqt5* or *pyside2* toolkits; the right figure is rendered
with the *pyqt* or *pyside* toolkits. Notice on the left figure that the golden ring and the 
character *H* appear to be behind the globe; they should be in front. The effects of the
error in depth order becomes even more bizarre for more complicated objects.

There are discussions on various forums about the cause of this. Some suspect that the problem
lies with the VTK library, while others point to problems with the Qt5 library. However, the
problem seems to be a combination of several factors. In particular, there are cases where the
problem does *not* show up with the *Qt5* library. The issue appears to involve the
OpenGL library and drivers; see the discussions 
(and [my comments](https://github.com/enthought/mayavi/issues/656#issuecomment-483550024)) 
on GitHub,
and [Nicolas Granger](https://github.com/nlgranger)'s
comment pointing to discussions at [VTK Dev](http://vtk.1045678.n5.nabble.com/VTK-master-Qt-5-and-Intel-i915-driver-on-Ubuntu-Linux-tt5727112.html).
In particular, when used with the NVIDIA OpenGL driver, the problem seems to go away.

A now a few words about using [pyenv](https://github.com/pyenv/pyenv), for those of you
who want to experiment with the latest cutting edge Python3. My experience and experiments have
been with Python 3.7.3, under Linux Mint 18.3 and 19.1. In either case, you should be able
to install mayavi and friends (through *pip*) without any problem (if you have first
installed all the necessary libraries and headers). 

But for the toolkits: for Qt you only have the choice
of [Qt5](https://wiki.python.org/moin/PyQt) or [PySide2](https://wiki.qt.io/Qt_for_Python):

	sudo pip install PySide2 pyqt5
    
(It seems that Qt4 and the older pyside are no longer available for Python3 via pip). 
Neither of them work for me (on computers with the Linux SGI OpenGL/GLX driver), 
as far as the depth order is concerned (although it *does* work for me
on computers with the NVIDIA OpenGL driver). 

For the other (wx) toolkit: installing [wxPython](https://wxpython.org/) with *pip3* turns out
to be a challenge. Under the *pyenv* setup, the pre-built Linux binary wheels are not currently available beyond
Python 3.4 (although it is available from *apt-get* for Python 3.5/3.6), 
so you will need to dig a little deeper: go to the [extras page](https://extras.wxpython.org/wxPython4/extras/linux/)
and pick the version appropriate for your version.

However, this is somewhat of a moot point: although wxPython will install, it does not run. It just 
quietly exits with a few warning messages about a call to a deprecated item. I have also
tried to compile wxPython from source. It was not easy, and although it seems to have
compiled and installed correctly (although it *did* fail to compile all the tests), 
that didn't work either (similar symptoms; the program failed to start up at all).

The bottom line is, if you are using *pyenv*, you may be out of luck unless you happen to
have the NVIDIA driver.

## Notes on Installing Matplotlib, Mayavi and Friends on Windows 10

I have had people ask me about running the programs in Windows (specifically, Windows 10).
The easiest way is probably to install the [Enthought Canopy](https://store.enthought.com/downloads/) 
distribution. I have had better experience with the 64-bit 3.5 distribution (I ran into
some problems with the 2.7 distribution).

By default the 3.5 distribution includes all the necessary modules to run mayavi, except
the Python Qt module. After installing the Canopy program, run the updates, then go
to the "available" section and search for *pyqt*. (You will need 
the *matplotlib* module also if you want to run the first polarization state simulation
program). I have not experimented extensively with the *wxPython* and *PySide* modules, but my
advice is to stick with the *pyqt* module for now.

One quirk with the Canopy package is that the Python program itself is installed per user, and
it is buried inside

	C:\Users\USERNAME\AppData\Local\Enthought\Canopy\edm\envs\User\python.exe
    
(where *USERNAME* is the name of the actual name of the user).
    
If you want to associate the *\*.py* programs with the Python program instead of the canopy program,
you will have to change the properties of the *\*.py* file to point to the Python executable
instead.

For Window users, one last option is to run the program in a Virtual Machine. I have tried
both [VirtualBox](https://www.virtualbox.org/) and [VMWare](https://www.vmware.com/). While both
perform similarly (and adequately) as a VM in a Linux host, the rendering in VMware seems to
be much better in a Windows 10 host. This was just a quick experiment with my particular 
computer hardware and setup, so your mileage may vary; take this with a grain of salt.

(*Last Revised 2021-01-15*)
