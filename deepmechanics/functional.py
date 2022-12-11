import torch

from deepmechanics.integration import gauss_legendre_integration


class Functional:
    def __init__(
        self, integrator=gauss_legendre_integration, *neumann_bcs, source_function=None
    ):
        self.integrator = integrator

        self.neumann_bcs = neumann_bcs
        self.source_function = source_function


class PotentialEnergyFunctional(Functional):
    def __init__(
        self,
        integrator=gauss_legendre_integration,
        neumann_bcs=None,
        source_function=None,
    ):
        super().__init__(integrator, neumann_bcs, source_function)

    def internal_term(self, ex, ey, gamma_xy, nx, ny, nxy, weights, jacobian_dets):
        integrand = 0.5 * ((ex * nx) + (ey * ny) + (gamma_xy * nxy))

        return self.integrator(integrand, weights, jacobian_dets)

    def external_term(self, approximator):
        result = torch.tensor(0.0)

        for bc in self.neumann_bcs:
            if bc is not None:
                fx, fy = bc.load
                ux, uy = approximator(bc.boundary_coords, bc.constraint)
                integrand = -fx * ux - fy * uy  # Negative as potential is lost
                result += self.integrator(
                    integrand, bc.boundary_weights, bc.boundary_jacobian_dets
                )

        return result

    def source_term(self, ux, uy, coords, weights, jacobian_dets):
        result = torch.tensor(0.0)

        # Compute the external energy body load (if present)
        if self.source_function is not None:
            qx, qy = self.source_function(coords)
            integrand = -qx * ux - qy * uy  # Negative as potential is lost
            result += self.integrator(integrand, weights, jacobian_dets)

        return result
