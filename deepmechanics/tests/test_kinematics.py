import unittest

from deepmechanics.kinematics import LinearKinematicLaw
from deepmechanics.utilities import tensorize_2d


class TestKinematics(unittest.TestCase):
    def setUp(self):
        self.kinematic_law = LinearKinematicLaw()

    def test_compute_strains(self):
        samples = [0, 1, 2, 3, 4]
        coords = tensorize_2d(samples, samples)
        xs = coords[:, 0].view(-1, 1)
        ys = coords[:, 1].view(-1, 1)

        # Manufactured displacement field
        ux = xs**2 + ys**2
        uy = xs**3 + ys**3

        # Expected values
        ex_expected = 2 * xs
        ey_expected = 3 * ys**2
        gamma_xy_expected = 2 * ys + 3 * xs**2

        # Computed values
        ex, ey, gamma_xy = self.kinematic_law.compute_strains(ux, uy, coords)

        for i in range(len(samples)):
            self.assertAlmostEqual(ex.detach().numpy()[i][0], ex_expected[i][0])
            self.assertAlmostEqual(ey.detach().numpy()[i][0], ey_expected[i][0])
            self.assertAlmostEqual(
                gamma_xy.detach().numpy()[i][0], gamma_xy_expected[i][0]
            )
