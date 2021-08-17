"""Read .STL files or accept user input to define spheres"""

from triangle_class import Triangle
from sphere_class import Sphere
import random

filename = input("Enter STL file name from meshes dir or type /s for spheres: ")
""" ↓ you can manually add spheres/triangles into this list ↓ """
objects = []    # list to store all objects to render

spec_col = [.8] * 3
shine = 100     # large number = less exposure/brightness
refl_coef = .3
random_colours = False  # randomly assign colours to triangles
default_col = [.1, .6, .6]


def read_stl(file):
    path = file + ".stl" if file[-4:] != ".stl" else file  # add .stl file extension if not already added
    try:
        stl = open(f"meshes/{path}", "r")
        if stl.readline().startswith("solid"):
            lines = stl.readlines()
            for i in range(len(lines)):
                line = lines[i].strip()
                if line == "endsolid":  # end of file
                    break
                if line.startswith("facet normal"):
                    normal = list(map(float, line.split()[-3:]))
                    vertices = []
                    for j in range(3):
                        vertices.append(list(map(float, lines[i + j + 2].split()[-3:])))

                    col = [random.random(), random.random(), random.random()] if random_colours else default_col
                    diff_col = [col[0]/2, col[1]/2, col[2]/2]
                    objects.append(Triangle(col, diff_col, spec_col, shine, refl_coef, *vertices, normal))
        else:
            print(f"ERROR: {path} is in an incorrect format. Make sure the STL file is in ASCII, not binary.")
        stl.close()

    except FileNotFoundError:
        print(f"ERROR: {path} not found in the meshes directory.")


if filename.lower() == "/s":
    num = int(input("Number of spheres = "))
    for i in range(num):
        rad = float(input(f"Radius of sphere {i+1} = "))
        centre = eval(input(f"Coordinate of centre of sphere {i+1} (as list) = "))
        col = [random.random(), random.random(), random.random()]
        diff_col = [col[0] / 3, col[1] / 3, col[2] / 3]
        objects.append(Sphere(col, diff_col, spec_col, 100, 1, centre, rad))

else:
    read_stl(filename)
