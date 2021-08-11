import deepmechanics.materialmodel as mm
import unittest


class TestLinearElasticPlaneStressMaterialModel(unittest.TestCase):

    def setUp(self):
        self.youngs_modulus = 10
        self.poissons_ratio = 0.3
        self.thickness = 0.1
        self.material_model = mm.LinearElasticPlaneStressMaterialModel(self.youngs_modulus, self.poissons_ratio, self.thickness)

    def test_compute_stresses(self):
        ex = 1.5
        ey = 2.5
        gamma_xy = 0.5

        nx, ny, nxy = self.material_model.compute_stresses(ex, ey, gamma_xy)

        self.assertAlmostEqual(nx, 2.472527472527472)
        self.assertAlmostEqual(ny, 3.241758241758242)
        self.assertAlmostEqual(nxy, 0.19230769230769226)


class TestLinearElasticPlaneStrainMaterialModel(unittest.TestCase):

    def setUp(self):
        self.youngs_modulus = 10
        self.poissons_ratio = 0.3
        self.thickness = 0.1
        self.material_model = mm.LinearElasticPlaneStrainMaterialModel(self.youngs_modulus, self.poissons_ratio, self.thickness)

    def test_compute_stresses(self):
        ex = 1.5
        ey = 2.5
        gamma_xy = 0.5

        nx, ny, nxy = self.material_model.compute_stresses(ex, ey, gamma_xy)

        self.assertAlmostEqual(nx, 3.461538461538461)
        self.assertAlmostEqual(ny, 4.230769230769231)
        self.assertAlmostEqual(nxy, 0.19230769230769226)
