class DirichletBoundaryCondition:
    def __init__(self, grid):
        self.grid = grid
        self._constraint_function = None
        self._integration_point_coords = None
        self._samples_coords = None
        self._top_edge_integration_point_coords = None
        self._bottom_edge_integration_point_coords = None
        self._right_edge_integration_point_coords = None
        self._left_edge_integration_point_coords = None

    def get_constraint_on_integration_points(self):
        def constraint(ux, uy):
            return self._constraint_function(self._integration_point_coords, ux, uy)

        return constraint

    def get_constraint_on_samples(self):
        def constraint(ux, uy):
            return self._constraint_function(self._samples_coords, ux, uy)

        return constraint

    def get_constraint_on_top_edge(self):
        def constraint(ux, uy):
            return self._constraint_function(
                self._top_edge_integration_point_coords, ux, uy
            )

        return constraint

    def get_constraint_on_bottom_edge(self):
        def constraint(ux, uy):
            return self._constraint_function(
                self._bottom_edge_integration_point_coords, ux, uy
            )

        return constraint

    def get_constraint_on_right_edge(self):
        def constraint(ux, uy):
            return self._constraint_function(
                self._right_edge_integration_point_coords, ux, uy
            )

        return constraint

    def get_constraint_on_left_edge(self):
        def constraint(ux, uy):
            return self._constraint_function(
                self._left_edge_integration_point_coords, ux, uy
            )

        return constraint


class FixedDisplacementsOnTopEdge(DirichletBoundaryCondition):
    def __init__(self, grid):
        super().__init__(grid)
        self._constraint_function = lambda ys, ux, uy: (
            ux * (grid.length_y - ys),
            uy * (grid.length_y - ys),
        )
        self._integration_point_coords = grid.integration_point_ys
        self._samples_coords = grid.samples_ys
        self._top_edge_integration_point_coords = grid.top_edge_integration_point_ys
        self._bottom_edge_integration_point_coords = (
            grid.bottom_edge_integration_point_ys
        )
        self._right_edge_integration_point_coords = grid.right_edge_integration_point_ys
        self._left_edge_integration_point_coords = grid.left_edge_integration_point_ys


class FixedDisplacementsOnBottomEdge(DirichletBoundaryCondition):
    def __init__(self, grid):
        super().__init__(grid)
        self._constraint_function = lambda ys, ux, uy: (ux * ys, uy * ys)
        self._integration_point_coords = grid.integration_point_ys
        self._samples_coords = grid.samples_ys
        self._top_edge_integration_point_coords = grid.top_edge_integration_point_ys
        self._bottom_edge_integration_point_coords = (
            grid.bottom_edge_integration_point_ys
        )
        self._right_edge_integration_point_coords = grid.right_edge_integration_point_ys
        self._left_edge_integration_point_coords = grid.left_edge_integration_point_ys


class FixedDisplacementsOnRightEdge(DirichletBoundaryCondition):
    def __init__(self, grid):
        super().__init__(grid)
        self._constraint_function = lambda xs, ux, uy: (
            ux * (grid.length_x - xs),
            uy * (grid.length_x - xs),
        )
        self._integration_point_coords = grid.integration_point_xs
        self._samples_coords = grid.samples_xs
        self._top_edge_integration_point_coords = grid.top_edge_integration_point_xs
        self._bottom_edge_integration_point_coords = (
            grid.bottom_edge_integration_point_xs
        )
        self._right_edge_integration_point_coords = grid.right_edge_integration_point_xs
        self._left_edge_integration_point_coords = grid.left_edge_integration_point_xs


class FixedDisplacementsOnLeftEdge(DirichletBoundaryCondition):
    def __init__(self, grid):
        super().__init__(grid)
        self._constraint_function = lambda xs, ux, uy: (ux * xs, uy * xs)
        self._integration_point_coords = grid.integration_point_xs
        self._samples_coords = grid.samples_xs
        self._top_edge_integration_point_coords = grid.top_edge_integration_point_xs
        self._bottom_edge_integration_point_coords = (
            grid.bottom_edge_integration_point_xs
        )
        self._right_edge_integration_point_coords = grid.right_edge_integration_point_xs
        self._left_edge_integration_point_coords = grid.left_edge_integration_point_xs


class AggregatedDirichletBoundaryCondition:
    def __init__(self, *dirichlet_bcs):
        self.dirichlet_bcs = [bc for bc in dirichlet_bcs]

    def get_constraint_on_integration_points(self):
        def constraint(ux, uy):
            for bc in self.dirichlet_bcs:
                constraint = bc.get_constraint_on_integration_points()
                ux, uy = constraint(ux, uy)
            return ux, uy

        return constraint

    def get_constraint_on_samples(self):
        def constraint(ux, uy):
            for bc in self.dirichlet_bcs:
                constraint = bc.get_constraint_on_samples()
                ux, uy = constraint(ux, uy)
            return ux, uy

        return constraint

    def get_constraint_on_top_edge(self):
        def constraint(ux, uy):
            for bc in self.dirichlet_bcs:
                constraint = bc.get_constraint_on_top_edge()
                ux, uy = constraint(ux, uy)
            return ux, uy

        return constraint

    def get_constraint_on_bottom_edge(self):
        def constraint(ux, uy):
            for bc in self.dirichlet_bcs:
                constraint = bc.get_constraint_on_bottom_edge()
                ux, uy = constraint(ux, uy)
            return ux, uy

        return constraint

    def get_constraint_on_right_edge(self):
        def constraint(ux, uy):
            for bc in self.dirichlet_bcs:
                constraint = bc.get_constraint_on_right_edge()
                ux, uy = constraint(ux, uy)
            return ux, uy

        return constraint

    def get_constraint_on_left_edge(self):
        def constraint(ux, uy):
            for bc in self.dirichlet_bcs:
                constraint = bc.get_constraint_on_left_edge()
                ux, uy = constraint(ux, uy)
            return ux, uy

        return constraint


class NeumannBoundaryCondition:
    def __init__(self, load_function, boundary_data, constraint):
        self.load_function = load_function
        (
            self.boundary_coords,
            self.boundary_weights,
            self.boundary_jacobian_dets,
        ) = boundary_data
        self.constraint = constraint
        self._fx = None
        self._fy = None

    @property
    def load(self):
        if not self._fx or not self._fy:
            self._fx, self._fy = self.load_function(self.boundary_coords)

        return self._fx, self._fy
