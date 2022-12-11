import unittest

from deepmechanics.grid import Grid, PlanarCartesianGrid
from deepmechanics.implicitgeometry import make_rectangle


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(2)

    def test_base_cells(self):
        # leaf_cells is empty
        self.assertFalse(self.grid.base_cells)

    def test_leaf_cells(self):
        # leaf_cells is empty
        self.assertFalse(self.grid.leaf_cells)


class TestPlanarCartesianGrid(unittest.TestCase):
    def setUp(self):
        self.grid = PlanarCartesianGrid(1.0, 1.0, 5.0, 3.0, 4, 2)

    def test_generate(self):
        self.grid.base_cells = []

        self.grid.generate()
        self.assertTrue(self.grid.base_cells)
        self.assertTrue(self.grid.leaf_cells)
        self.assertEqual(len(self.grid.base_cells), 8)

    def test_top_base_cells(self):
        self.assertEqual(len(self.grid.top_base_cells), 4)

        for cell in self.grid.top_base_cells:
            _, ys = cell.top_coords
            for y in ys:
                self.assertAlmostEqual(y, self.grid.y_end)

    def test_top_leaf_cells(self):
        self.grid.get_cell_at_indices(0, self.grid.j_end).refine()
        self.assertEqual(len(self.grid.top_leaf_cells), 5)

        for cell in self.grid.top_leaf_cells:
            _, ys = cell.top_coords
            for y in ys:
                self.assertAlmostEqual(y, self.grid.y_end)

        self.grid.get_cell_at_indices(0, self.grid.j_end).delete_all_children()

    def test_bottom_base_cells(self):
        self.assertEqual(len(self.grid.bottom_base_cells), 4)

        for cell in self.grid.bottom_base_cells:
            _, ys = cell.bottom_coords
            for y in ys:
                self.assertAlmostEqual(y, self.grid.y_start)

    def test_bottom_leaf_cells(self):
        self.grid.get_cell_at_indices(0, 0).refine()
        self.assertEqual(len(self.grid.bottom_leaf_cells), 5)

        for cell in self.grid.bottom_leaf_cells:
            _, ys = cell.bottom_coords
            for y in ys:
                self.assertAlmostEqual(y, self.grid.y_start)

        self.grid.get_cell_at_indices(0, 0).delete_all_children()

    def test_right_base_cells(self):
        self.assertEqual(len(self.grid.right_base_cells), 2)

        for cell in self.grid.right_base_cells:
            xs, _ = cell.right_coords
            for x in xs:
                self.assertAlmostEqual(x, self.grid.x_end)

    def test_right_leaf_cells(self):
        self.grid.get_cell_at_indices(self.grid.i_end, 0).refine()
        self.assertEqual(len(self.grid.right_leaf_cells), 3)

        for cell in self.grid.right_leaf_cells:
            xs, _ = cell.right_coords
            for x in xs:
                self.assertAlmostEqual(x, self.grid.x_end)

        self.grid.get_cell_at_indices(self.grid.i_end, 0).delete_all_children()

    def test_left_base_cells(self):
        self.assertEqual(len(self.grid.left_base_cells), 2)

        for cell in self.grid.left_base_cells:
            xs, _ = cell.left_coords
            for x in xs:
                self.assertAlmostEqual(x, self.grid.x_start)

    def test_left_leaf_cells(self):
        self.grid.get_cell_at_indices(0, 0).refine()
        self.assertEqual(len(self.grid.left_leaf_cells), 3)

        for cell in self.grid.left_leaf_cells:
            xs, _ = cell.left_coords
            for x in xs:
                self.assertAlmostEqual(x, self.grid.x_start)

        self.grid.get_cell_at_indices(0, 0).delete_all_children()

    def test_length_x(self):
        self.assertAlmostEqual(self.grid.length_x, 4)

    def test_length_y(self):
        self.assertAlmostEqual(self.grid.length_y, 2)

    def test_i_end(self):
        self.assertEqual(self.grid.i_end, 3)

    def test_j_end(self):
        self.assertEqual(self.grid.j_end, 1)

    def test_integration_point_coords(self):
        xs, ys = self.grid.integration_point_coords

        self.assertEqual(len(xs), 4 * 4 * 2)
        self.assertEqual(len(ys), 4 * 4 * 2)

    def test_top_edge_integration_point_coords(self):
        self.grid.get_cell_at_indices(0, self.grid.j_end).refine()

        _, ys = self.grid.top_edge_integration_point_coords

        for y in ys:
            self.assertAlmostEqual(y, self.grid.y_end)

        self.grid.get_cell_at_indices(0, self.grid.j_end).delete_all_children()

    def test_bottom_edge_integration_point_coords(self):
        self.grid.get_cell_at_indices(0, 0).refine()

        _, ys = self.grid.bottom_edge_integration_point_coords

        for y in ys:
            self.assertAlmostEqual(y, self.grid.y_start)

        self.grid.get_cell_at_indices(0, 0).delete_all_children()

    def test_right_edge_integration_point_coords(self):
        self.grid.get_cell_at_indices(self.grid.i_end, 0).refine()

        xs, _ = self.grid.right_edge_integration_point_coords

        for x in xs:
            self.assertAlmostEqual(x, self.grid.x_end)

        self.grid.get_cell_at_indices(self.grid.i_end, 0).delete_all_children()

    def test_left_edge_integration_point_coords(self):
        self.grid.get_cell_at_indices(0, 0).refine()

        xs, _ = self.grid.left_edge_integration_point_coords

        for x in xs:
            self.assertAlmostEqual(x, self.grid.x_start)

        self.grid.get_cell_at_indices(0, 0).delete_all_children()

    def test_top_coords(self):
        xs, ys = self.grid.top_coords

        xs_expected = [1.0, 2.0, 3.0, 4.0, 5.0]
        ys_expected = [3.0, 3.0, 3.0, 3.0, 3.0]

        for x_expected, x in zip(xs_expected, xs):
            self.assertAlmostEqual(x_expected, x)

        for y_expected, y in zip(ys_expected, ys):
            self.assertAlmostEqual(y_expected, y)

    def test_bottom_coords(self):
        xs, ys = self.grid.bottom_coords

        xs_expected = [1.0, 2.0, 3.0, 4.0, 5.0]
        ys_expected = [1.0, 1.0, 1.0, 1.0, 1.0]

        for x_expected, x in zip(xs_expected, xs):
            self.assertAlmostEqual(x_expected, x)

        for y_expected, y in zip(ys_expected, ys):
            self.assertAlmostEqual(y_expected, y)

    def test_right_coords(self):
        xs, ys = self.grid.right_coords

        xs_expected = [5.0, 5.0, 5.0]
        ys_expected = [1.0, 2.0, 3.0]

        for x_expected, x in zip(xs_expected, xs):
            self.assertAlmostEqual(x_expected, x)

        for y_expected, y in zip(ys_expected, ys):
            self.assertAlmostEqual(y_expected, y)

    def test_left_coords(self):
        xs, ys = self.grid.left_coords

        xs_expected = [1.0, 1.0, 1.0]
        ys_expected = [1.0, 2.0, 3.0]

        for x_expected, x in zip(xs_expected, xs):
            self.assertAlmostEqual(x_expected, x)

        for y_expected, y in zip(ys_expected, ys):
            self.assertAlmostEqual(y_expected, y)

    def test_set_active_state_with_domain(self):
        # Deactivate all
        for cell in self.grid.leaf_cells:
            cell.is_active = False

        # Rectangle enclosing cells of the bottom half
        rectangle = make_rectangle(0, 0, 10, 2.1)

        self.grid.set_active_state_with_filter(rectangle)

        for cell in self.grid.bottom_leaf_cells:
            self.assertTrue(cell.is_active)

        for cell in self.grid.top_leaf_cells:
            self.assertFalse(cell.is_active)

        # Activate all
        for cell in self.grid.leaf_cells:
            cell.is_active = True

    def test_index_exists(self):
        # Corners
        self.assertTrue(self.grid._index_exists(0, 0))
        self.assertTrue(self.grid._index_exists(self.grid.i_end, 0))
        self.assertTrue(self.grid._index_exists(0, self.grid.j_end))
        self.assertTrue(self.grid._index_exists(self.grid.i_end, self.grid.j_end))

        # Inside
        self.assertTrue(self.grid._index_exists(0, self.grid.j_end))

        # Outside
        self.assertFalse(self.grid._index_exists(1, 100))
        self.assertFalse(self.grid._index_exists(1, -100))
        self.assertFalse(self.grid._index_exists(100, 1))
        self.assertFalse(self.grid._index_exists(-100, 1))

    def test_get_cell_at_indices(self):
        self.assertEqual(self.grid.get_cell_at_indices(0, 0), self.grid.base_cells[0])
        self.assertEqual(
            self.grid.get_cell_at_indices(self.grid.i_end, self.grid.j_end),
            self.grid.base_cells[-1],
        )

    def test_point_is_inside_grid(self):
        # Inside
        self.assertTrue(self.grid._point_is_inside_grid(2.0, 2.0))

        # Outside
        self.assertFalse(self.grid._point_is_inside_grid(1, 100))
        self.assertFalse(self.grid._point_is_inside_grid(1, -100))
        self.assertFalse(self.grid._point_is_inside_grid(100, 1))
        self.assertFalse(self.grid._point_is_inside_grid(-100, 1))

    def test_get_cell_indices_from_coords(self):
        self.assertTrue(self.grid.get_cell_indices_from_coords(1.1, 1.1), (0, 0))
        self.assertTrue(
            self.grid.get_cell_indices_from_coords(4.9, 2.9),
            (self.grid.i_end, self.grid.j_end),
        )

    def test_get_cell_from_coords(self):
        self.assertTrue(
            self.grid.get_cell_from_coords(1.1, 1.1), self.grid.base_cells[0]
        )
        self.assertTrue(
            self.grid.get_cell_from_coords(4.9, 2.9), self.grid.base_cells[-1]
        )
