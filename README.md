PylabUtils
==========

Collection of pylab utilites I use for mobile robotics research and prototyping

Some important conventions for coordinate frames:
* Rotation about x axis: "roll"
* Rotation about y axis: "pitch"
* Rotation about z axis: "heading"

* The Euler sequence for the relative-pose $x_{ij}$ from frame $i$ to frame $j$ is
  rotation about the heading, pitch, and roll axes (in that order)
  
Instructions
============

Make sure PylabUtils is in the PYTHONPATH environment variable either from the shell or
sys.path

Import using `import PylabUtils` (I would recommend using `import PylabUtils as pylabu`)
