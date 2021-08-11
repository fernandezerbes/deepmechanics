
class LinearElasticMaterialModel:

    def __init__(self, youngs_modulus, poissons_ratio):
        self.young_modulus = youngs_modulus
        self.poissons_ratio = poissons_ratio


class LinearElasticPlaneMaterialModel(LinearElasticMaterialModel):

    def __init__(self, youngs_modulus, poissons_ratio, thickness):
        super().__init__(youngs_modulus, poissons_ratio)
        self.thickness = thickness


class LinearElasticPlaneStressMaterialModel(LinearElasticPlaneMaterialModel):

    def compute_stresses(self, ex, ey, gamma_xy):
        factor = self.young_modulus * self.thickness / (1 - self.poissons_ratio**2) 

        sx = factor * (ex + self.poissons_ratio * ey)
        sy = factor * (self.poissons_ratio * ex + ey)
        tau_xy = factor * (1 - self.poissons_ratio) * gamma_xy / 2

        return sx, sy, tau_xy


class LinearElasticPlaneStrainMaterialModel(LinearElasticPlaneMaterialModel):

    def compute_stresses(self, ex, ey, gamma_xy):
        factor = self.young_modulus * self.thickness / ((1 + self.poissons_ratio) * (1 - 2 * self.poissons_ratio))

        sx = factor * ((1 - self.poissons_ratio) * ex + self.poissons_ratio * ey)
        sy = factor * (self.poissons_ratio * ex + (1 - self.poissons_ratio) * ey)
        tau_xy = factor * (1 - 2 * self.poissons_ratio) * gamma_xy / 2

        return sx, sy, tau_xy
