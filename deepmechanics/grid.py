from deepmechanics.cell import QuadCell
from deepmechanics.utilities import make_array_unique, tensorize_1d, tensorize_2d


class Grid:
    def __init__(self, spatial_dimensions):
        self.spatial_dimensions = spatial_dimensions
        self.base_cells = []
        self._leaf_cells = []
        self._active_leaf_cells = []
        self._refinement_strategy = None

    def generate(self):
        pass

    @property
    def refinement_strategy(self):
        if self._refinement_strategy is None:
            raise ValueError("Refinement strategy is not initialized")

        return self._refinement_strategy

    @refinement_strategy.setter
    def refinement_strategy(self, value):
        self._refinement_strategy = value

    @property
    def leaf_cells(self):
        self._leaf_cells.clear()
        for cell in self.base_cells:
            self._leaf_cells += cell.leaves

        return self._leaf_cells

    @property
    def active_leaf_cells(self):
        self._active_leaf_cells.clear()
        for cell in self.base_cells:
            self._active_leaf_cells += cell.active_leaves

        return self._active_leaf_cells

    def refine(self):
        self.refinement_strategy.refine(self)


class PlanarCartesianGrid(Grid):
    def __init__(self, x_start, y_start, x_end, y_end, resolution_x, resolution_y):
        super().__init__(2)
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.generate()

    def generate(self):
        if self.base_cells:
            raise ValueError("Grid already generated!")

        dx = self.length_x / self.resolution_x
        dy = self.length_y / self.resolution_y

        for j in range(self.resolution_y):
            for i in range(self.resolution_x):
                x_start_cell = self.x_start + dx * i
                x_end_cell = x_start_cell + dx
                y_start_cell = self.y_start + dy * j
                y_end_cell = y_start_cell + dy
                self.base_cells.append(
                    QuadCell(x_start_cell, y_start_cell, x_end_cell, y_end_cell)
                )

    def triangulate(self):
        triangles = []
        for i in range(len(self.active_leaf_cells)):
            triangles.append([4 * i, 4 * i + 1, 4 * i + 3])
            triangles.append([4 * i, 4 * i + 3, 4 * i + 2])
        return triangles

    @property
    def top_base_cells(self):
        return self.base_cells[-self.resolution_x :]

    @property
    def top_leaf_cells(self):
        leaf_cells = []
        for cell in self.top_base_cells:
            leaf_cells += cell.top_leaves

        return leaf_cells

    @property
    def bottom_base_cells(self):
        return self.base_cells[: self.resolution_x]

    @property
    def bottom_leaf_cells(self):
        leaf_cells = []
        for cell in self.bottom_base_cells:
            leaf_cells += cell.bottom_leaves

        return leaf_cells

    @property
    def right_base_cells(self):
        return self.base_cells[self.i_end :: self.resolution_x]

    @property
    def right_leaf_cells(self):
        leaf_cells = []
        for cell in self.right_base_cells:
            leaf_cells += cell.right_leaves

        return leaf_cells

    @property
    def left_base_cells(self):
        return self.base_cells[:: self.resolution_x]

    @property
    def left_leaf_cells(self):
        leaf_cells = []
        for cell in self.left_base_cells:
            leaf_cells += cell.left_leaves

        return leaf_cells

    @property
    def length_x(self):
        return self.x_end - self.x_start

    @property
    def length_y(self):
        return self.y_end - self.y_start

    @property
    def i_end(self):
        return self.resolution_x - 1

    @property
    def j_end(self):
        return self.resolution_y - 1

    @property
    def integration_point_coords(self):
        all_xs = []
        all_ys = []
        for cell in self.active_leaf_cells:
            xs, ys = cell.integration_point_coords
            all_xs += xs
            all_ys += ys
        return all_xs, all_ys

    @property
    def integration_point_weights(self):
        weights = []
        for cell in self.active_leaf_cells:
            weights += cell.integration_point_weights
        return weights

    @property
    def integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.active_leaf_cells:
            jacobian_dets += cell.integration_point_jacobian_dets
        return jacobian_dets

    @property
    def top_edge_integration_point_coords(self):
        all_xs = []
        all_ys = []
        for cell in self.top_base_cells:
            xs, ys = cell.top_edge_integration_point_coords
            all_xs += xs
            all_ys += ys
        return all_xs, all_ys

    @property
    def top_edge_integration_point_weights(self):
        weights = []
        for cell in self.top_base_cells:
            weights += cell.top_edge_integration_point_weights
        return weights

    @property
    def top_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.top_base_cells:
            jacobian_dets += cell.top_edge_integration_point_jacobian_dets
        return jacobian_dets

    @property
    def bottom_edge_integration_point_coords(self):
        all_xs = []
        all_ys = []
        for cell in self.bottom_base_cells:
            xs, ys = cell.bottom_edge_integration_point_coords
            all_xs += xs
            all_ys += ys
        return all_xs, all_ys

    @property
    def bottom_edge_integration_point_weights(self):
        weights = []
        for cell in self.bottom_base_cells:
            weights += cell.bottom_edge_integration_point_weights
        return weights

    @property
    def bottom_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.bottom_base_cells:
            jacobian_dets += cell.bottom_edge_integration_point_jacobian_dets
        return jacobian_dets

    @property
    def right_edge_integration_point_coords(self):
        all_xs = []
        all_ys = []
        for cell in self.right_base_cells:
            xs, ys = cell.right_edge_integration_point_coords
            all_xs += xs
            all_ys += ys
        return all_xs, all_ys

    @property
    def right_edge_integration_point_weights(self):
        weights = []
        for cell in self.right_base_cells:
            weights += cell.right_edge_integration_point_weights
        return weights

    @property
    def right_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.right_base_cells:
            jacobian_dets += cell.right_edge_integration_point_jacobian_dets
        return jacobian_dets

    @property
    def left_edge_integration_point_coords(self):
        all_xs = []
        all_ys = []
        for cell in self.left_base_cells:
            xs, ys = cell.left_edge_integration_point_coords
            all_xs += xs
            all_ys += ys
        return all_xs, all_ys

    @property
    def left_edge_integration_point_weights(self):
        weights = []
        for cell in self.left_base_cells:
            weights += cell.left_edge_integration_point_weights
        return weights

    @property
    def left_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.left_base_cells:
            jacobian_dets += cell.left_edge_integration_point_jacobian_dets
        return jacobian_dets

    @property
    def top_coords(self):
        all_xs = []
        all_ys = []
        for i in range(self.resolution_x):
            cell = self.get_cell_at_indices(i, self.j_end)
            for leaf in cell.leaves:
                xs, ys = leaf.top_coords
                if self.y_end in ys:
                    all_xs += xs
        all_xs = make_array_unique(all_xs)
        all_xs.sort()
        all_ys = [self.y_end] * len(all_xs)
        return all_xs, all_ys

    @property
    def bottom_coords(self):
        all_xs = []
        all_ys = []
        for i in range(self.resolution_x):
            cell = self.get_cell_at_indices(i, 0)
            for leaf in cell.leaves:
                xs, ys = leaf.bottom_coords
                if self.y_start in ys:
                    all_xs += xs
        all_xs = make_array_unique(all_xs)
        all_xs.sort()
        all_ys = [self.y_start] * len(all_xs)
        return all_xs, all_ys

    @property
    def right_coords(self):
        all_xs = []
        all_ys = []
        for j in range(self.resolution_y):
            cell = self.get_cell_at_indices(self.i_end, j)
            for leaf in cell.leaves:
                xs, ys = leaf.right_coords
                if self.x_end in xs:
                    all_ys += ys
        all_ys = make_array_unique(all_ys)
        all_ys.sort()
        all_xs = [self.x_end] * len(all_ys)
        return all_xs, all_ys

    @property
    def left_coords(self):
        all_xs = []
        all_ys = []
        for j in range(self.resolution_y):
            cell = self.get_cell_at_indices(0, j)
            for leaf in cell.leaves:
                xs, ys = leaf.left_coords
                if self.x_start in xs:
                    all_ys += ys
        all_ys = make_array_unique(all_ys)
        all_ys.sort()
        all_xs = [self.x_start] * len(all_ys)
        return all_xs, all_ys

    @property
    def corner_coords(self):
        all_xs = []
        all_ys = []
        for cell in self.active_leaf_cells:
            xs, ys = cell.corner_coords
            all_xs += xs
            all_ys += ys
        return all_xs, all_ys

    def get_samples(
        self, filter=None, number_of_samples_x=100, number_of_samples_y=100
    ):
        all_xs = []
        all_ys = []
        dx = self.length_x / (number_of_samples_x - 1)
        dy = self.length_y / (number_of_samples_y - 1)
        for i in range(number_of_samples_x):
            x = self.x_start + i * dx
            for j in range(number_of_samples_y):
                y = self.y_start + j * dy
                if filter is None:
                    all_xs.append(x)
                    all_ys.append(y)
                elif filter(x, y):
                    all_xs.append(x)
                    all_ys.append(y)
        return all_xs, all_ys

    def set_active_state_with_filter(self, filter, seeds_per_side=10):
        for cell in self.leaf_cells:
            cell.is_active = cell.is_inside(filter, seeds_per_side)

    def _index_exists(self, i, j):
        return 0 <= i <= self.i_end and 0 <= j <= self.j_end

    def get_cell_at_indices(self, i, j):
        if self._index_exists(i, j):
            return self.base_cells[j * self.resolution_x + i]

        raise ValueError("Indices ({},{}) are outside the grid".format(i, j))

    def _point_is_inside_grid(self, x, y):
        return self.x_start <= x <= self.x_end and self.y_start <= y <= self.y_end

    def get_cell_indices_from_coords(self, x, y):
        if self._point_is_inside_grid(x, y):
            i = int((x - self.x_start) / self.length_x)
            j = int((y - self.y_start) / self.length_y)

            return i, j

        raise ValueError("Point ({},{}) is outside the grid".format(x, y))

    def get_cell_from_coords(self, x, y):
        i, j = self.get_cell_indices_from_coords(x, y)
        return self.get_cell_at_indices(i, j)


class TensorizedPlanarCartesianGrid(PlanarCartesianGrid):
    def __init__(self, x_start, y_start, x_end, y_end, resolution_x, resolution_y):
        super().__init__(x_start, y_start, x_end, y_end, resolution_x, resolution_y)
        # Cashed values for efficiency
        self._integration_point_coords = None
        self._integration_point_weights = None
        self._integration_point_jacobian_dets = None
        self._integration_point_xs = None
        self._integration_point_ys = None
        self._top_edge_integration_point_coords = None
        self._top_edge_integration_point_weights = None
        self._top_edge_integration_point_jacobian_dets = None
        self._top_edge_integration_point_xs = None
        self._top_edge_integration_point_ys = None
        self._bottom_edge_integration_point_coords = None
        self._bottom_edge_integration_point_weights = None
        self._bottom_edge_integration_point_jacobian_dets = None
        self._bottom_edge_integration_point_xs = None
        self._bottom_edge_integration_point_ys = None
        self._right_edge_integration_point_coords = None
        self._right_edge_integration_point_weights = None
        self._right_edge_integration_point_jacobian_dets = None
        self._right_edge_integration_point_xs = None
        self._right_edge_integration_point_ys = None
        self._left_edge_integration_point_coords = None
        self._left_edge_integration_point_weights = None
        self._left_edge_integration_point_jacobian_dets = None
        self._left_edge_integration_point_xs = None
        self._left_edge_integration_point_ys = None
        self._samples_coords = None
        self._samples_xs = None
        self._samples_ys = None

    @property
    def integration_point_coords(self):
        if self._integration_point_coords is None:
            xs, ys = super().integration_point_coords
            self._integration_point_coords = tensorize_2d(xs, ys)

        return self._integration_point_coords

    @property
    def integration_point_weights(self):
        if self._integration_point_weights is None:
            weights = super().integration_point_weights
            self._integration_point_weights = tensorize_1d(weights)

        return self._integration_point_weights

    @property
    def integration_point_jacobian_dets(self):
        if self._integration_point_jacobian_dets is None:
            jacobian_dets = super().integration_point_jacobian_dets
            self._integration_point_jacobian_dets = tensorize_1d(jacobian_dets)

        return self._integration_point_jacobian_dets

    @property
    def integration_point_xs(self):
        if self._integration_point_xs is None:
            self._integration_point_xs = self.integration_point_coords[:, 0].view(-1, 1)

        return self._integration_point_xs

    @property
    def integration_point_ys(self):
        if self._integration_point_ys is None:
            self._integration_point_ys = self.integration_point_coords[:, 1].view(-1, 1)

        return self._integration_point_ys

    @property
    def integration_points_data(self):
        return (
            self.integration_point_coords,
            self.integration_point_weights,
            self.integration_point_jacobian_dets,
        )

    @property
    def top_edge_integration_point_coords(self):
        if self._top_edge_integration_point_coords is None:
            xs, ys = super().top_edge_integration_point_coords
            self._top_edge_integration_point_coords = tensorize_2d(xs, ys)
        return self._top_edge_integration_point_coords

    @property
    def top_edge_integration_point_weights(self):
        if self._top_edge_integration_point_weights is None:
            weights = super().top_edge_integration_point_weights
            self._top_edge_integration_point_weights = tensorize_1d(weights)

        return self._top_edge_integration_point_weights

    @property
    def top_edge_integration_point_jacobian_dets(self):
        if self._top_edge_integration_point_jacobian_dets is None:
            jacobian_dets = super().top_edge_integration_point_jacobian_dets
            self._top_edge_integration_point_jacobian_dets = tensorize_1d(jacobian_dets)

        return self._top_edge_integration_point_jacobian_dets

    @property
    def top_edge_integration_point_xs(self):
        if self._top_edge_integration_point_xs is None:
            self._top_edge_integration_point_xs = (
                self.top_edge_integration_point_coords[:, 0].view(-1, 1)
            )
        return self._top_edge_integration_point_xs

    @property
    def top_edge_integration_point_ys(self):
        if self._top_edge_integration_point_ys is None:
            self._top_edge_integration_point_ys = (
                self.top_edge_integration_point_coords[:, 1].view(-1, 1)
            )
        return self._top_edge_integration_point_ys

    @property
    def top_edge_integration_points_data(self):
        return (
            self.top_edge_integration_point_coords,
            self.top_edge_integration_point_weights,
            self.top_edge_integration_point_jacobian_dets,
        )

    @property
    def bottom_edge_integration_point_coords(self):
        if self._bottom_edge_integration_point_coords is None:
            xs, ys = super().bottom_edge_integration_point_coords
            self._bottom_edge_integration_point_coords = tensorize_2d(xs, ys)
        return self._bottom_edge_integration_point_coords

    @property
    def bottom_edge_integration_point_weights(self):
        if self._bottom_edge_integration_point_weights is None:
            weights = super().bottom_edge_integration_point_weights
            self._bottom_edge_integration_point_weights = tensorize_1d(weights)

        return self._bottom_edge_integration_point_weights

    @property
    def bottom_edge_integration_point_jacobian_dets(self):
        if self._bottom_edge_integration_point_jacobian_dets is None:
            jacobian_dets = super().bottom_edge_integration_point_jacobian_dets
            self._bottom_edge_integration_point_jacobian_dets = tensorize_1d(
                jacobian_dets
            )

        return self._bottom_edge_integration_point_jacobian_dets

    @property
    def bottom_edge_integration_point_xs(self):
        if self._bottom_edge_integration_point_xs is None:
            self._bottom_edge_integration_point_xs = (
                self.bottom_edge_integration_point_coords[:, 0].view(-1, 1)
            )
        return self._bottom_edge_integration_point_xs

    @property
    def bottom_edge_integration_point_ys(self):
        if self._bottom_edge_integration_point_ys is None:
            self._bottom_edge_integration_point_ys = (
                self.bottom_edge_integration_point_coords[:, 1].view(-1, 1)
            )
        return self._bottom_edge_integration_point_ys

    @property
    def bottom_edge_integration_points_data(self):
        return (
            self.bottom_edge_integration_point_coords,
            self.bottom_edge_integration_point_weights,
            self.bottom_edge_integration_point_jacobian_dets,
        )

    @property
    def right_edge_integration_point_coords(self):
        if self._right_edge_integration_point_coords is None:
            xs, ys = super().right_edge_integration_point_coords
            self._right_edge_integration_point_coords = tensorize_2d(xs, ys)
        return self._right_edge_integration_point_coords

    @property
    def right_edge_integration_point_weights(self):
        if self._right_edge_integration_point_weights is None:
            weights = super().right_edge_integration_point_weights
            self._right_edge_integration_point_weights = tensorize_1d(weights)

        return self._right_edge_integration_point_weights

    @property
    def right_edge_integration_point_jacobian_dets(self):
        if self._right_edge_integration_point_jacobian_dets is None:
            jacobian_dets = super().right_edge_integration_point_jacobian_dets
            self._right_edge_integration_point_jacobian_dets = tensorize_1d(
                jacobian_dets
            )

        return self._right_edge_integration_point_jacobian_dets

    @property
    def right_edge_integration_point_xs(self):
        if self._right_edge_integration_point_xs is None:
            self._right_edge_integration_point_xs = (
                self.right_edge_integration_point_coords[:, 0].view(-1, 1)
            )
        return self._right_edge_integration_point_xs

    @property
    def right_edge_integration_point_ys(self):
        if self._right_edge_integration_point_ys is None:
            self._right_edge_integration_point_ys = (
                self.right_edge_integration_point_coords[:, 1].view(-1, 1)
            )
        return self._right_edge_integration_point_ys

    @property
    def right_edge_integration_points_data(self):
        return (
            self.right_edge_integration_point_coords,
            self.right_edge_integration_point_weights,
            self.right_edge_integration_point_jacobian_dets,
        )

    @property
    def left_edge_integration_point_coords(self):
        if self._left_edge_integration_point_coords is None:
            xs, ys = super().left_edge_integration_point_coords
            self._left_edge_integration_point_coords = tensorize_2d(xs, ys)
        return self._left_edge_integration_point_coords

    @property
    def left_edge_integration_point_weights(self):
        if self._left_edge_integration_point_weights is None:
            weights = super().left_edge_integration_point_weights
            self._left_edge_integration_point_weights = tensorize_1d(weights)

        return self._left_edge_integration_point_weights

    @property
    def left_edge_integration_point_jacobian_dets(self):
        if self._left_edge_integration_point_jacobian_dets is None:
            jacobian_dets = super().left_edge_integration_point_jacobian_dets
            self._left_edge_integration_point_jacobian_dets = tensorize_1d(
                jacobian_dets
            )

        return self._left_edge_integration_point_jacobian_dets

    @property
    def left_edge_integration_point_xs(self):
        if self._left_edge_integration_point_xs is None:
            self._left_edge_integration_point_xs = (
                self.left_edge_integration_point_coords[:, 0].view(-1, 1)
            )
        return self._left_edge_integration_point_xs

    @property
    def left_edge_integration_point_ys(self):
        if self._left_edge_integration_point_ys is None:
            self._left_edge_integration_point_ys = (
                self.left_edge_integration_point_coords[:, 1].view(-1, 1)
            )
        return self._left_edge_integration_point_ys

    @property
    def left_edge_integration_points_data(self):
        return (
            self.left_edge_integration_point_coords,
            self.left_edge_integration_point_weights,
            self.left_edge_integration_point_jacobian_dets,
        )

    def prepare_samples(
        self, implicit_geometry=None, number_of_samples_x=100, number_of_samples_y=100
    ):
        xs, ys = super().get_samples(
            implicit_geometry, number_of_samples_x, number_of_samples_y
        )
        self._samples_coords = tensorize_2d(xs, ys)

    @property
    def samples_coords(self):
        if self._samples_coords is None:
            raise ValueError("Samples are not prepared")
        else:
            return self._samples_coords

    @property
    def samples_xs(self):
        if self._samples_coords is None:
            raise ValueError("Samples are not prepared")
        else:
            return self._samples_coords[:, 0].view(-1, 1)

    @property
    def samples_ys(self):
        if self._samples_coords is None:
            raise ValueError("Samples are not prepared")
        else:
            return self._samples_coords[:, 1].view(-1, 1)
