import numpy as np

from object_class import Object


class Sphere(Object):
    def __init__(self, amb_col, diff_col, spec_col, shine, refl_coef, centre, radius):
        super(Sphere, self).__init__(amb_col, diff_col, spec_col, shine, refl_coef)
        self.centre = centre
        self.radius = radius
        self.normal = lambda surface_pt: np.divide(surface_pt - self.centre, np.linalg.norm(surface_pt - self.centre))  # surface_pt - self.centre

    def __get_intersection_distance(self, ray_dir, ray_origin):
        # Calculate distance from origin of ray to intersection point with sphere
        # maths from: https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
        # Using numpy operations b/c they might be faster than standard python operations (+-*/)

        ray_dir = np.divide(ray_dir, np.linalg.norm(ray_dir))  # make sure ray_dir is a unit vector
        term1 = -(np.dot(ray_dir, np.subtract(ray_origin, self.centre)))
        discriminant = np.square(np.dot(ray_dir, np.subtract(ray_origin, self.centre))) - \
                       np.subtract(np.square(np.linalg.norm(np.subtract(ray_origin, self.centre))), self.radius ** 2)

        if discriminant > 0:  # if the ray intersects at 2 points
            plus = np.add(term1, np.sqrt(discriminant))
            minus = np.subtract(term1, np.sqrt(discriminant))
            if plus > 0 and minus > 0:
                return np.minimum(plus, minus)  # return closest intersection point

        return None  # if ray doesnt intersect, return nothing

    def get_intersection_data(self, ray_dir, ray_origin):
        dist = self.__get_intersection_distance(ray_dir, ray_origin)
        if dist:
            # return the intersection point and the distance
            return np.add(ray_origin, np.multiply(ray_dir, dist)), dist

        return None, np.inf
