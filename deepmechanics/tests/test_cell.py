from deepmechanics.cell import Cell, QuadCell
from deepmechanics.implicitgeometry import make_rectangle
import unittest


class TestCell(unittest.TestCase):

    def setUp(self):
        self.cell = Cell(2)

    def test_spatial_dimensions(self):
        self.assertEqual(self.cell.spatial_dimensions, 2)

class TestQuadCell(unittest.TestCase):

    def setUp(self):
        self.cell = QuadCell(1.0, 1.0, 5.0, 3.0)

    def test_x_mid(self):
        self.assertAlmostEqual(self.cell.x_mid, 3)

    def test_y_mid(self):
        self.assertAlmostEqual(self.cell.y_mid, 2)

    def test_length_x(self):
        self.assertAlmostEqual(self.cell.length_x, 4)

    def test_length_y(self):
        self.assertAlmostEqual(self.cell.length_y, 2)

    def test_integration_point_coords(self):
        xs, ys = self.cell.integration_point_coords
        self.assertAlmostEqual(xs[0], 1.84529946162075)
        self.assertAlmostEqual(xs[1], 1.84529946162075)
        self.assertAlmostEqual(xs[2], 4.15470053837925)
        self.assertAlmostEqual(xs[3], 4.15470053837925)

        self.assertAlmostEqual(ys[0], 1.42264973081037)
        self.assertAlmostEqual(ys[1], 2.57735026918963)
        self.assertAlmostEqual(ys[2], 1.42264973081037)
        self.assertAlmostEqual(ys[3], 2.57735026918963)

    def test_top_edge_integration_point_coords(self):
        xs, ys = self.cell.top_edge_integration_point_coords
        self.assertAlmostEqual(xs[0], 1.84529946162075)
        self.assertAlmostEqual(xs[1], 4.15470053837925)

        self.assertAlmostEqual(ys[0], 3.0)
        self.assertAlmostEqual(ys[1], 3.0)

        # TODO Test refined case

    def test_bottom_edge_integration_point_coords(self):
        xs, ys = self.cell.bottom_edge_integration_point_coords
        self.assertAlmostEqual(xs[0], 1.84529946162075)
        self.assertAlmostEqual(xs[1], 4.15470053837925)

        self.assertAlmostEqual(ys[0], 1.0)
        self.assertAlmostEqual(ys[1], 1.0)

        # TODO Test refined case

    def test_right_edge_integration_point_coords(self):
        xs, ys = self.cell.right_edge_integration_point_coords
        self.assertAlmostEqual(xs[0], 5.0)
        self.assertAlmostEqual(xs[1], 5.0)

        self.assertAlmostEqual(ys[0], 1.42264973081037)
        self.assertAlmostEqual(ys[1], 2.57735026918963)

        # TODO Test refined case

    def test_left_edge_integration_point_coords(self):
        xs, ys = self.cell.left_edge_integration_point_coords
        self.assertAlmostEqual(xs[0], 1.0)
        self.assertAlmostEqual(xs[1], 1.0)

        self.assertAlmostEqual(ys[0], 1.42264973081037)
        self.assertAlmostEqual(ys[1], 2.57735026918963)

        # TODO Test refined case 

    def test_top_coords(self):
        xs, ys = self.cell.top_coords
        self.assertAlmostEqual(xs[0], 1.0)
        self.assertAlmostEqual(xs[1], 5.0)
        self.assertAlmostEqual(ys[0], 3.0)
        self.assertAlmostEqual(ys[1], 3.0)

    def test_bottom_coords(self):
        xs, ys = self.cell.bottom_coords
        self.assertAlmostEqual(xs[0], 1.0)
        self.assertAlmostEqual(xs[1], 5.0)
        self.assertAlmostEqual(ys[0], 1.0)
        self.assertAlmostEqual(ys[1], 1.0)

    def test_right_coords(self):
        xs, ys = self.cell.right_coords
        self.assertAlmostEqual(xs[0], 5.0)
        self.assertAlmostEqual(xs[1], 5.0)
        self.assertAlmostEqual(ys[0], 1.0)
        self.assertAlmostEqual(ys[1], 3.0)

    def test_left_coords(self):
        xs, ys = self.cell.left_coords
        self.assertAlmostEqual(xs[0], 1.0)
        self.assertAlmostEqual(xs[1], 1.0)
        self.assertAlmostEqual(ys[0], 1.0)
        self.assertAlmostEqual(ys[1], 3.0)

    def test_jacobian_det(self):
        self.assertAlmostEqual(self.cell.jacobian_det, 2.0)

    def test_map_local_to_global(self):
        x_mid, y_mid = self.cell.map_local_to_global(0.0, 0.0)
        self.assertAlmostEqual(x_mid, 3.0)
        self.assertAlmostEqual(y_mid, 2.0)

        x_sw, y_sw = self.cell.map_local_to_global(-1.0, -1.0)
        self.assertAlmostEqual(x_sw, 1.0)
        self.assertAlmostEqual(y_sw, 1.0)

        x_se, y_se = self.cell.map_local_to_global(1.0, -1.0)
        self.assertAlmostEqual(x_se, 5.0)
        self.assertAlmostEqual(y_se, 1.0)

        x_nw, y_nw = self.cell.map_local_to_global(1.0, 1.0)
        self.assertAlmostEqual(x_nw, 5.0)
        self.assertAlmostEqual(y_nw, 3.0)

        x_ne, y_ne = self.cell.map_local_to_global(-1.0, 1.0)
        self.assertAlmostEqual(x_ne, 1.0)
        self.assertAlmostEqual(y_ne, 3.0)

        x, y = self.cell.map_local_to_global(-0.5, -0.5)
        self.assertAlmostEqual(x, 2.0)
        self.assertAlmostEqual(y, 1.5)

    def test_refine(self):
        self.cell.refine()
        self.assertEqual(len(self.cell.children), 4)
        self.assertFalse(self.cell.is_active)

        child_sw = self.cell.children[0]
        self.assertEqual(child_sw.x_start, 1.0)
        self.assertEqual(child_sw.y_start, 1.0)
        self.assertEqual(child_sw.x_end, 3.0)
        self.assertEqual(child_sw.y_end, 2.0)
        self.assertTrue(child_sw.is_active)

        child_se = self.cell.children[1]
        self.assertEqual(child_se.x_start, 3.0)
        self.assertEqual(child_se.y_start, 1.0)
        self.assertEqual(child_se.x_end, 5.0)
        self.assertEqual(child_se.y_end, 2.0)
        self.assertTrue(child_se.is_active)

        child_nw = self.cell.children[2]
        self.assertEqual(child_nw.x_start, 1.0)
        self.assertEqual(child_nw.y_start, 2.0)
        self.assertEqual(child_nw.x_end, 3.0)
        self.assertEqual(child_nw.y_end, 3.0)
        self.assertTrue(child_nw.is_active)

        child_ne = self.cell.children[3]
        self.assertEqual(child_ne.x_start, 3.0)
        self.assertEqual(child_ne.y_start, 2.0)
        self.assertEqual(child_ne.x_end, 5.0)
        self.assertEqual(child_ne.y_end, 3.0)
        self.assertTrue(child_ne.is_active)

        self.cell.delete_all_children()

    def test_delete_all_children(self):
        self.cell.refine()
        self.assertTrue(self.cell.is_refined)
        self.cell.delete_all_children()
        self.assertFalse(self.cell.is_refined)
        self.assertEqual(len(self.cell.children), 0)

    def test_delete_all_childeren_recursive(self):
        self.cell.refine()
        self.assertTrue(self.cell.is_refined)
        self.cell.delete_all_children_recursive(self.cell.children)
        self.assertFalse(self.cell.is_refined)
        self.assertEqual(len(self.cell.children), 0)

    def test_is_leaf(self):
        self.cell.delete_all_children()
        self.assertTrue(self.cell.is_leaf)

    def test_is_refined(self):
        self.cell.delete_all_children()
        self.assertFalse(self.cell.is_refined)

        self.cell.refine()
        self.assertTrue(self.cell.is_refined)
        self.cell.delete_all_children()

    def test_is_active(self):
        self.cell.delete_all_children()
        self.assertTrue(self.cell.is_active)

        self.cell.refine()
        self.assertFalse(self.cell.is_active)

        self.cell.delete_all_children()

        # Test setter
        self.cell.is_active = False
        self.assertFalse(self.cell.is_active)

        self.cell.is_active = True
        self.assertTrue(self.cell.is_active)

    def test_is_active_leaf(self):
        self.cell.delete_all_children()
        self.assertTrue(self.cell.is_active)
        self.assertTrue(self.cell.is_leaf)

    def test_count_inside_seeds(self):
        domain_for_cell_outside = make_rectangle(10, 10, 11, 11)
        count_outside = self.cell._count_inside_seeds(domain_for_cell_outside, 10)
        self.assertEqual(count_outside, 0)

        domain_for_cell_inside = make_rectangle(0, 0, 10, 10)
        count_inside = self.cell._count_inside_seeds(domain_for_cell_inside, 10)
        self.assertEqual(count_inside, 100)

        domain_for_cell_half_outside = make_rectangle(0, 0, self.cell.x_mid, 11)
        count_half_outside = self.cell._count_inside_seeds(domain_for_cell_half_outside, 10)
        self.assertEqual(count_half_outside, 50)

    def test_is_cut(self):
        domain_for_cell_outside = make_rectangle(10, 10, 11, 11)
        self.assertFalse(self.cell.is_cut(domain_for_cell_outside))
        self.assertFalse(self.cell.is_cut(domain_for_cell_outside, 50))

        domain_for_cell_inside = make_rectangle(0, 0, 10, 10)
        self.assertFalse(self.cell.is_cut(domain_for_cell_inside))
        self.assertFalse(self.cell.is_cut(domain_for_cell_inside, 50))

        domain_for_cell_cut = make_rectangle(0, 0, 2, 2)
        self.assertTrue(self.cell.is_cut(domain_for_cell_cut))
        self.assertTrue(self.cell.is_cut(domain_for_cell_cut, 50))

    def test_is_inside(self):
        domain_outside = make_rectangle(10, 10, 11, 11)
        self.assertFalse(self.cell.is_inside(domain_outside))
        self.assertFalse(self.cell.is_inside(domain_outside, 50))

        domain_inside = make_rectangle(0, 0, 11, 11)
        self.assertTrue(self.cell.is_inside(domain_inside))
        self.assertTrue(self.cell.is_inside(domain_inside, 50))

    def test_leaves(self):
        self.cell.delete_all_children()
        self.cell.refine()
        self.assertEqual(len(self.cell.leaves), 4)

        self.cell.children[0].refine()
        self.assertEqual(len(self.cell.leaves), 7)
        self.cell.delete_all_children()

    def test_top_leaves(self):
        self.cell.delete_all_children()

        self.assertEqual(len(self.cell.top_leaves), 1)
        self.cell.refine()

        self.assertEqual(len(self.cell.top_leaves), 2)

        self.cell.children[2].refine()
        self.assertEqual(len(self.cell.top_leaves), 3)

        self.cell.delete_all_children()

    def test_bottom_leaves(self):
        self.cell.delete_all_children()

        self.assertEqual(len(self.cell.bottom_leaves), 1)
        self.cell.refine()

        self.assertEqual(len(self.cell.bottom_leaves), 2)

        self.cell.children[0].refine()
        self.assertEqual(len(self.cell.bottom_leaves), 3)
        
        self.cell.delete_all_children()

    def test_right_leaves(self):
        self.cell.delete_all_children()

        self.assertEqual(len(self.cell.right_leaves), 1)
        self.cell.refine()

        self.assertEqual(len(self.cell.right_leaves), 2)

        self.cell.children[1].refine()
        self.assertEqual(len(self.cell.right_leaves), 3)
        
        self.cell.delete_all_children()

    def test_left_leaves(self):
        self.cell.delete_all_children()

        self.assertEqual(len(self.cell.left_leaves), 1)
        self.cell.refine()

        self.assertEqual(len(self.cell.left_leaves), 2)

        self.cell.children[0].refine()
        self.assertEqual(len(self.cell.left_leaves), 3)
        
        self.cell.delete_all_children()
