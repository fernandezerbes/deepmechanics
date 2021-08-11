import deepmechanics.boundarycondition as bcond
from deepmechanics.grid import TensorizedPlanarCartesianGrid
import unittest


class TestFixedDisplacementsOnTopEdge(unittest.TestCase):

    def setUp(self):
        self.grid = TensorizedPlanarCartesianGrid(0, 0, 1, 1, 1, 1)
        self.grid.prepare_samples(number_of_samples_x=3, number_of_samples_y=3)
        self.bc = bcond.FixedDisplacementsOnTopEdge(self.grid)

    def test_get_constraint_on_integration_points(self):
        pass

    def test_get_constraint_on_samples(self):
        constraint = self.bc.get_constraint_on_samples()
        print(constraint(1, 1))

    def test_get_constraint_on_top_edge(self):
        pass

    def test_get_constraint_on_bottom_edge(self):
        pass

    def test_get_constraint_on_right_edge(self):
        pass

    def test_get_constraint_on_left_edge(self):
        pass
