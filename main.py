import time
import numpy as np
import matplotlib.pyplot as plt

from light_class import Light
from camera_class import Camera
from stl_reader import objects

start_time = time.time()

resolution = 20
width, height = np.multiply([4, 3], resolution)
aspect_ratio = width / height   # also the width of screen

camera = Camera(np.array([0, 0, 0]), np.array([0, 1, 0]))

screen_width = aspect_ratio
screen_height = 1
FOV = 80    # in degrees
screen_dist = aspect_ratio / (2*np.tan(np.radians(FOV/2)))  # distance of screen from camera
screen_TL = np.array([-aspect_ratio / 2, screen_dist, screen_height / 2])  # Top-left corner of screen


def normalise(vector):
    # return unit vector of a vector
    return np.divide(vector, np.linalg.norm(vector))

# direction vector that is perpendicular to camera direction. Used to increment across the screen to find pixel coords
x_pixel_vector = normalise(np.cross(camera.direction, np.array([0, 0, 1])))
z_pixel_vector = normalise(np.cross(camera.direction, x_pixel_vector))


def translate(vector):
    global screen_TL, camera, x_pixel_vector, z_pixel_vector
    camera.position = np.add(camera.position, vector)
    screen_TL = np.add(screen_TL, vector)


def rotate_vector(vector, axis, angle, origin=np.array([0, 0, 0])):
    vector = np.subtract(vector, origin)
    matrix = axis * np.dot(axis, vector)
    matrix = np.add(matrix, np.cross(np.cos(angle) * np.cross(axis, vector), axis) + np.sin(angle) * np.cross(axis, vector))
    matrix = np.add(matrix, origin)

    return np.round_(matrix, 5)


def rotate(axis, angle):
    # rotations using radians
    c = rotate_vector(camera.direction, axis, angle)  # rotate direction of camera
    if list(np.cross(c, np.array([0, 0, 1]))) == [0, 0, 0]:     # avoid division by 0 errors if new cam dir is vertical
        c = rotate_vector(camera.direction, axis, angle+1e-5)

    global x_pixel_vector, z_pixel_vector, screen_TL
    camera.direction = c
    x_pixel_vector = normalise(np.cross(c, np.array([0, 0, 1])))    # re-calculate directions of pixels
    z_pixel_vector = normalise(np.cross(c, x_pixel_vector))
    screen_TL = rotate_vector(screen_TL, axis, angle, origin=camera.position)     # rotate top left coordinate of the screen


"""DEFINE COORDS OF CAM AND LIGHT"""
light_pos = [1.5, -4, 4]
light = Light(light_pos, np.array([1, 1, 1]), np.array([1, 1, 1]), np.array([1, 1, 1]))
translate([0, -1.5, 2])   # set camera position
rotate(np.array([1, 0, 0]), -np.pi/4)     # set camera rotation


def pixel_coords_generator():
    # find coords of each pixel on the screen
    for z in range(height):
        for x in range(width):
            pix_coords = screen_TL + x_pixel_vector * x * (screen_width/width) + z_pixel_vector * z * (screen_height/height)
            # return both absolute position (coord in 3D space) and position relative to the screen of each pixel
            yield {"abs": pix_coords, "rel": [x, z]}


image = np.zeros((height, width, 3))  # array to hold colours of each pixel


def get_reflected_ray(incident, normal):
    reflected = np.subtract(incident, np.multiply(np.multiply(2, (np.dot(incident, normal))), normal))
    return reflected


def get_closest_data(dir, origin):
    # return intersection point of closest object, the closest object and the distance to intersection point
    data = [obj.get_intersection_data(dir, origin) for obj in objects]
    min_dist = np.inf
    closest_pt = None
    closest_obj = None
    for index, i in enumerate(data):
        # if the distance to int_pt is positive and not infinity
        if 0 < i[1] < min_dist:
            min_dist = i[1]
            closest_pt = i[0]
            closest_obj = objects[index]
    return closest_pt, closest_obj, min_dist


def is_in_shadow(origin_pt, obj):
    normal_to_surface = obj.normal(origin_pt)
    shifted_pt = origin_pt + np.multiply(normal_to_surface, 1e-3)  # shift point away from sphere so that it doesn't re-detect the sphere as an object that blocks light

    intersection_to_light = normalise(np.subtract(light.pos, shifted_pt))  # ray that goes from intersection point towards the light source

    _, _, dist_to_object = get_closest_data(intersection_to_light, shifted_pt)

    dist_to_light = np.linalg.norm(np.subtract(light.pos, shifted_pt))

    return dist_to_object < dist_to_light


reflection_number = 3
loop_counter = 0
for pixel in pixel_coords_generator():  # get coord of every pixel in 3D space
    # show percentage complete:
    loop_counter += 1
    if loop_counter % 250 == 0:
        print(f"{np.round_(100 * loop_counter / (height * width), 1)}%")

    ray_dir = normalise(np.subtract(pixel["abs"], camera.position))
    int_pt, obj, _ = get_closest_data(ray_dir, camera.position)
    old_int_pt = camera.position
    old_obj_refl = 1
    total_illumination = 0
    reflections = 0

    while int_pt is not None and reflections <= reflection_number and not is_in_shadow(int_pt, obj):
        normal_to_surface = obj.normal(int_pt)
        total_illumination += np.multiply(old_obj_refl, obj.calc_col(light, normalise(np.subtract(light.pos, int_pt)), normal_to_surface, normalise(np.subtract(old_int_pt, int_pt))))
        old_int_pt = int_pt
        old_obj_refl = obj.refl_coef
        reflected_ray = get_reflected_ray(ray_dir, normal_to_surface) + np.multiply(normal_to_surface, 1e-5)
        int_pt, obj, _ = get_closest_data(reflected_ray, int_pt + np.multiply(obj.normal(int_pt), 1e-5))
        reflections += 1

    image[pixel["rel"][1], pixel["rel"][0]] = np.clip(total_illumination, 0, 1)


print(f"Rendering duration: {time.time() - start_time}s")

plt.imshow(image)
plt.show()
