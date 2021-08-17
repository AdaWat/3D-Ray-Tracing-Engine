# 3D-Ray-Tracing-Engine
A 3D ray tracing engine in pure Python for STL files.

![Example of 3 spheres](https://github.com/AdaWat/3D-Ray-Tracing-Engine/blob/a95d99ce2aa37715e3cba55c952e12701bf38806/images/ray_tracing_8.png)
![Example render of Utah teapot](https://github.com/AdaWat/3D-Ray-Tracing-Engine/blob/7ef09248dd10679b8f39653bea1a0dfd728fca97/images/utah%20teapot.png)

## Description
This is a fun project I made at the end of year 11. It's not meant to be especially fast or high-tech, I just wanted it to render an STL with shadows and reflections 
using ray tracing.
The code can render perfect spheres or any STL file. The code uses matplotlib to display the final result.
I used OOP and split the classes into different files to improve readability.
The stl_reader.py file handles reading the STL and converting it to a format that uses Triangle classes that are used by main.py for rendering.
I used a python generator to find to coordinates of each pixel in the 3D space and convert that into 2D coordinates on the display screen. This is used in the main loop in main.py.

## Requirements
If you want to render a custom STL file, make sure it is in ASCII format (binary STLs won't work) and using the millimeter scale. Then save it to the meshes directory.


## Running
Run main.py to begin ray tracing. Then enter the file name of the STL file you want to render (you don't need to type the .stl file extension).
Alternatively, you can type /s to only render spheres. The coodinates of the centre of the spheres must be in python list format (eg: [.1, 3, -.1]).

## Changing coords of camera and light
The coordinate system uses x/y/z where z is up (this is unlike most other rendering programs).

The STLs are centered at the origin, so to change the viewing angle, you must set the coodinate of the camera and the light source.
To do that, translate or rotate the camera in main.py.

```
"""DEFINE COORDS OF CAM AND LIGHT"""
light_pos = [1.5, -4, 4]
light = Light(light_pos, np.array([1, 1, 1]), np.array([1, 1, 1]), np.array([1, 1, 1]))
translate([0, -1.5, 2])   # set camera position
rotate(np.array([1, 0, 0]), -np.pi/4)     # set camera rotation
```
The code in the repo is set up to render the utah.stl file (Utah teapot) so that is why the camera and light are at odd positions.


For example, to move the light to coord (0, -4, 0), simply edit line 62 to: ```light_pos = [0, -4, 0]```

To move the camera to coord (0, -2, 0), simple edit line 64 to ```translate([0, -2, 0])```

To rotate the camera, use this syntax: ```rotate(AXIS-OF-ROTATION, ROTATION-ANGLE-IN-RADIANS)```
The angle of rotation is in radians and a positive angle is an anti-clockwise rotation.

## Changing resolution
To improve resolution, make the ```resolution``` variable higher.
This will slow rendering times.

## Changine colours of objects
To assign random colours to each triangle in an STL, make the ```random_colours``` variable True.

Otherwise, to edit the colour of the STL, edit the ```default_col```. The colours use RGB and use a scale from 0 to 1.
You can also change other variables, like spec_col, shine and refl_coef. See https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model for more info on how the colouring
system works.

Make sure that the light is illuminating a side of the object that is visible to the camera. Otherwise, the image will just appear black becasue the camera is looking at an
object that is in shadow.
