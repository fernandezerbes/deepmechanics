import unittest

import torch

from deepmechanics.grid import TensorizedPlanarCartesianGrid
from deepmechanics.integration import gauss_legendre_integration


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.grid = TensorizedPlanarCartesianGrid(0.0, 0.0, 4.0, 16.0, 1, 1)

    def test_gauss_legendre_integration(self):
        integrand = torch.Tensor([2.0])
        weights = self.grid.integration_point_weights
        jacobian_dets = self.grid.integration_point_jacobian_dets
        result = (
            gauss_legendre_integration(integrand, weights, jacobian_dets)
            .detach()
            .numpy()
        )

        self.assertAlmostEqual(result, 16.0 * 4.0 * 2.0)
