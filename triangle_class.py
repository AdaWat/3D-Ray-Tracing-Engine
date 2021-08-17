import numpy as np

from object_class import Object


def normalise(vector):
    # return unit vector of a vector
    return np.divide(vector, np.linalg.norm(vector))


class Triangle(Object):
    def __init__(self, amb_col, diff_col, spec_col, shine, refl_coef, A, B, C, normal=None):
        super(Triangle, self).__init__(amb_col, diff_col, spec_col, shine, refl_coef)
        # A, B, C are vertices of the triangle. ALWAYS defined in anti-clockwise direction
        self.A = A  # used in the get_intersection_data method
        self.AB = np.subtract(B, A)
        self.AC = np.subtract(C, A)
        self.normal = lambda _: normal if normal is not None else normalise(np.cross(self.AB, self.AC))
        self.D = np.dot(self.normal(None), A)     # distance from origin to the plane of triangle (along the normal)

    """Möller–Trumbore algorithm (fast)"""
    def get_intersection_data(self, ray_dir, ray_origin):
        pVec = np.cross(ray_dir, self.AC)
        determinant = np.dot(self.AB, pVec)

        if determinant < 1e-5:
            return None, np.inf

        tVec = np.subtract(ray_origin, self.A)
        u = np.divide(np.dot(tVec, pVec), determinant)

        if u <= 0 or u >= 1:    # if u is 0, the ray hit the edge of the triangle (no intersect)
            return None, np.inf

        qVec = np.cross(tVec, self.AB)
        v = np.divide(np.dot(ray_dir, qVec), determinant)
        if v < 0 or u+v > 1:
            return None, np.inf

        t = np.divide(np.dot(self.AC, qVec), determinant)       # distance from ray_origin to intersection point

        p = ray_origin + t * normalise(ray_dir)     # intersection point

        # return the intersection point and the distance to intersection
        return p, t
