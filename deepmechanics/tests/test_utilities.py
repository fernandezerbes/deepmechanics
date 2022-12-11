import unittest

import torch
from torch.autograd import grad
from torch.functional import unique

from deepmechanics import utilities


class TestIntegration(unittest.TestCase):
    def test_make_array_unique(self):
        non_unique_array = [1, 2, 1, 2, 3, 4, 4, 2, 1]
        unique_array = [1, 2, 3, 4]

        self.assertEqual(utilities.make_array_unique(non_unique_array), unique_array)

    def test_get_derivative(self):
        xs = torch.linspace(0, 10, 11, requires_grad=True, dtype=torch.float64).view(
            -1, 1
        )
        ys = xs**3
        first_derivative = utilities.get_derivative(ys, xs, 1)
        second_derivative = utilities.get_derivative(ys, xs, 2)

        for x, dy, ddy in zip(xs, first_derivative, second_derivative):
            x = x.detach().numpy()[0]
            dy = dy.detach().numpy()[0]
            ddy = ddy.detach().numpy()[0]
            self.assertAlmostEqual(dy, 3 * x**2)
            self.assertAlmostEqual(ddy, 6 * x)

    def test_tensorize_1d(self):
        # scalar
        x = 12
        x = utilities.tensorize_1d(x)

        self.assertTrue(isinstance(x, torch.Tensor))
        self.assertEqual(list(x.size()), [1])
        self.assertAlmostEqual(x.detach().numpy()[0], x)

        # list
        x = [1, 2, 5, 9]
        x = utilities.tensorize_1d(x)

        self.assertTrue(isinstance(x, torch.Tensor))
        self.assertEqual(list(x.size()), [4, 1])
        self.assertAlmostEqual(x.detach().numpy()[0][0], x[0])
        self.assertAlmostEqual(x.detach().numpy()[1][0], x[1])
        self.assertAlmostEqual(x.detach().numpy()[2][0], x[2])
        self.assertAlmostEqual(x.detach().numpy()[3][0], x[3])

    def test_tensorize_2d(self):
        # scalar
        x = 12
        y = 24
        xy = utilities.tensorize_2d(x, y)

        self.assertTrue(isinstance(xy, torch.Tensor))
        self.assertEqual(list(xy.size()), [2])
        self.assertAlmostEqual(xy.detach().numpy()[0], x)
        self.assertAlmostEqual(xy.detach().numpy()[1], y)

        # list
        x = [1, 2, 5, 9]
        y = [11, 12, 15, 19]
        xy = utilities.tensorize_2d(x, y)

        self.assertTrue(isinstance(xy, torch.Tensor))
        self.assertEqual(list(xy.size()), [4, 2])
        self.assertAlmostEqual(xy.detach().numpy()[0][0], x[0])
        self.assertAlmostEqual(xy.detach().numpy()[1][0], x[1])
        self.assertAlmostEqual(xy.detach().numpy()[2][0], x[2])
        self.assertAlmostEqual(xy.detach().numpy()[3][0], x[3])
        self.assertAlmostEqual(xy.detach().numpy()[0][1], y[0])
        self.assertAlmostEqual(xy.detach().numpy()[1][1], y[1])
        self.assertAlmostEqual(xy.detach().numpy()[2][1], y[2])
        self.assertAlmostEqual(xy.detach().numpy()[3][1], y[3])

    def test_tensorize_3d(self):
        # scalar
        x = 12
        y = 24
        z = 36
        xyz = utilities.tensorize_3d(x, y, z)

        self.assertTrue(isinstance(xyz, torch.Tensor))
        self.assertEqual(list(xyz.size()), [3])
        self.assertAlmostEqual(xyz.detach().numpy()[0], x)
        self.assertAlmostEqual(xyz.detach().numpy()[1], y)
        self.assertAlmostEqual(xyz.detach().numpy()[2], z)

        # list
        x = [1, 2, 5, 9]
        y = [11, 12, 15, 19]
        z = [21, 22, 25, 29]
        xyz = utilities.tensorize_3d(x, y, z)

        self.assertTrue(isinstance(xyz, torch.Tensor))
        self.assertEqual(list(xyz.size()), [4, 3])
        self.assertAlmostEqual(xyz.detach().numpy()[0][0], x[0])
        self.assertAlmostEqual(xyz.detach().numpy()[1][0], x[1])
        self.assertAlmostEqual(xyz.detach().numpy()[2][0], x[2])
        self.assertAlmostEqual(xyz.detach().numpy()[3][0], x[3])
        self.assertAlmostEqual(xyz.detach().numpy()[0][1], y[0])
        self.assertAlmostEqual(xyz.detach().numpy()[1][1], y[1])
        self.assertAlmostEqual(xyz.detach().numpy()[2][1], y[2])
        self.assertAlmostEqual(xyz.detach().numpy()[3][1], y[3])
        self.assertAlmostEqual(xyz.detach().numpy()[0][2], z[0])
        self.assertAlmostEqual(xyz.detach().numpy()[1][2], z[1])
        self.assertAlmostEqual(xyz.detach().numpy()[2][2], z[2])
        self.assertAlmostEqual(xyz.detach().numpy()[3][2], z[3])
