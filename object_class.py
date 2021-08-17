import numpy as np


class Object:
    def __init__(self, amb_col, diff_col, spec_col, shininess, rf):
        # using the Blinn-Phong reflection model (https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model)
        self.ambient_colour = amb_col
        self.diffuse_colour = diff_col
        self.specular_colour = spec_col
        self.shininess = shininess
        self.refl_coef = rf

    def calc_col(self, light, L, N, V):
        illumination = np.zeros(3)
        illumination += self.ambient_colour * light.ambient
        illumination += self.diffuse_colour * light.diffuse * np.dot(L, N)
        camera_to_intersection = (L + V) / np.linalg.norm(L + V)
        illumination += self.specular_colour * light.specular * np.dot(N, camera_to_intersection) ** (self.shininess / 4)

        return np.clip(illumination, 0, 1)
