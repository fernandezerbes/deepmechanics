from deepmechanics.utilities import get_derivative


class LinearKinematicLaw:
    def compute_strains(self, ux, uy, coords):
        # Get first order derivatives of displacements w.r.t. x and y
        dux = get_derivative(ux, coords, 1)
        duy = get_derivative(uy, coords, 1)

        # Filter components out
        ex = dux[:, 0].view(-1, 1)
        exy = dux[:, 1].view(-1, 1)
        ey = duy[:, 1].view(-1, 1)
        eyx = duy[:, 0].view(-1, 1)

        gamma_xy = exy + eyx  # Voigt notation

        return ex, ey, gamma_xy
