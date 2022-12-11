class Cell:
    def __init__(self, spatial_dimensions):
        self.spatial_dimensions = spatial_dimensions


class QuadCell(Cell):
    def __init__(self, x_start, y_start, x_end, y_end):
        super().__init__(spatial_dimensions=2)
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.children = []  # [child_sw, child_se, child_nw, child_ne]
        self._is_active = True
        self.integration_points = [-0.5773502691896257, 0.5773502691896257]
        self.integration_weights = [1.0, 1.0]

    @property
    def x_mid(self):
        return (self.x_start + self.x_end) / 2

    @property
    def y_mid(self):
        return (self.y_start + self.y_end) / 2

    @property
    def length_x(self):
        return self.x_end - self.x_start

    @property
    def length_y(self):
        return self.y_end - self.y_start

    @property
    def jacobian_det(self):
        return self.length_x * self.length_y / 4

    @property
    def jacobian_det_top_edge(self):
        return self.length_x / 2

    @property
    def top_edge_jacobian_det(self):
        return self.length_x / 2

    @property
    def bottom_edge_jacobian_det(self):
        return self.length_x / 2

    @property
    def right_edge_jacobian_det(self):
        return self.length_y / 2

    @property
    def left_edge_jacobian_det(self):
        return self.length_y / 2

    @property
    def corner_coords(self):
        xs = []
        ys = []
        if self.is_active:
            xs = [self.x_start, self.x_end, self.x_start, self.x_end]
            ys = [self.y_start, self.y_start, self.y_end, self.y_end]
        return xs, ys

    @property
    def number_of_integration_points_in_xi(self):
        if self.is_active:
            return len(self.integration_points)

    @property
    def number_of_integration_points_in_eta(self):
        if self.is_active:
            return len(self.integration_points)

    @property
    def integration_point_coords(self):
        xs = []
        ys = []
        if self.is_active:
            for xi in self.integration_points:
                for eta in self.integration_points:
                    x, y = self.map_local_to_global(xi, eta)
                    xs.append(x)
                    ys.append(y)
        return xs, ys

    @property
    def integration_point_weights(self):
        weights = []
        if self.is_active:
            for w_xi in self.integration_weights:
                for w_eta in self.integration_weights:
                    weights.append(w_xi * w_eta)
        return weights

    @property
    def integration_point_jacobian_dets(self):
        jacobian_dets = []
        if self.is_active:
            jacobian_dets += [self.jacobian_det] * 4
        return jacobian_dets

    @property
    def top_edge_integration_point_coords(self):
        xs = []
        ys = []
        for cell in self.top_active_leaves:
            for xi in cell.integration_points:
                x, y = cell.map_local_to_global(xi, 1)
                xs.append(x)
                ys.append(y)
        return xs, ys

    @property
    def top_edge_integration_point_weights(self):
        weights = []
        for cell in self.top_active_leaves:
            for w_xi in self.integration_weights:
                weights.append(w_xi)
        return weights

    @property
    def top_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.top_active_leaves:
            jacobian_dets += [
                cell.top_edge_jacobian_det
            ] * self.number_of_integration_points_in_xi
        return jacobian_dets

    @property
    def bottom_edge_integration_point_coords(self):
        xs = []
        ys = []
        for cell in self.bottom_active_leaves:
            for xi in cell.integration_points:
                x, y = cell.map_local_to_global(xi, -1)
                xs.append(x)
                ys.append(y)
        return xs, ys

    @property
    def bottom_edge_integration_point_weights(self):
        weights = []
        for cell in self.bottom_active_leaves:
            for w_xi in self.integration_weights:
                weights.append(w_xi)
        return weights

    @property
    def bottom_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.bottom_active_leaves:
            jacobian_dets += [
                cell.bottom_edge_jacobian_det
            ] * self.number_of_integration_points_in_xi
        return jacobian_dets

    @property
    def right_edge_integration_point_coords(self):
        xs = []
        ys = []
        for cell in self.right_active_leaves:
            for eta in cell.integration_points:
                x, y = cell.map_local_to_global(1, eta)
                xs.append(x)
                ys.append(y)
        return xs, ys

    @property
    def right_edge_integration_point_weights(self):
        weights = []
        for cell in self.right_active_leaves:
            for w_eta in self.integration_weights:
                weights.append(w_eta)
        return weights

    @property
    def right_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.right_active_leaves:
            jacobian_dets += [
                cell.right_edge_jacobian_det
            ] * self.number_of_integration_points_in_eta
        return jacobian_dets

    @property
    def left_edge_integration_point_coords(self):
        xs = []
        ys = []
        for cell in self.left_active_leaves:
            for eta in cell.integration_points:
                x, y = cell.map_local_to_global(-1, eta)
                xs.append(x)
                ys.append(y)
        return xs, ys

    @property
    def left_edge_integration_point_weights(self):
        weights = []
        for cell in self.left_active_leaves:
            for w_eta in self.integration_weights:
                weights.append(w_eta)
        return weights

    @property
    def left_edge_integration_point_jacobian_dets(self):
        jacobian_dets = []
        for cell in self.left_active_leaves:
            jacobian_dets += [
                cell.left_edge_jacobian_det
            ] * self.number_of_integration_points_in_eta
        return jacobian_dets

    @property
    def top_coords(self):
        xs = [self.x_start, self.x_end]
        ys = [self.y_end, self.y_end]
        return xs, ys

    @property
    def bottom_coords(self):
        xs = [self.x_start, self.x_end]
        ys = [self.y_start, self.y_start]
        return xs, ys

    @property
    def right_coords(self):
        xs = [self.x_end, self.x_end]
        ys = [self.y_start, self.y_end]
        return xs, ys

    @property
    def left_coords(self):
        xs = [self.x_start, self.x_start]
        ys = [self.y_start, self.y_end]
        return xs, ys

    def map_local_to_global(self, xi, eta):
        x = self.x_mid + self.length_x * xi / 2
        y = self.y_mid + self.length_y * eta / 2
        return x, y

    def refine(self):
        child_sw = QuadCell(self.x_start, self.y_start, self.x_mid, self.y_mid)
        child_se = QuadCell(self.x_mid, self.y_start, self.x_end, self.y_mid)
        child_nw = QuadCell(self.x_start, self.y_mid, self.x_mid, self.y_end)
        child_ne = QuadCell(self.x_mid, self.y_mid, self.x_end, self.y_end)
        self.children = [child_sw, child_se, child_nw, child_ne]
        self.is_active = False

    def delete_all_children(self):
        self.delete_all_children_recursive(self.children)

    def delete_all_children_recursive(self, children):
        if not children:
            self.is_active = True
        else:
            temp = children
            children.clear()
            for child in temp:
                self.delete_all_children_recursive(child.children)

    @property
    def is_leaf(self):
        return not self.children

    @property
    def is_refined(self):
        return not self.is_leaf

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def is_active_leaf(self):
        return self.is_active and self.is_leaf

    def _count_inside_seeds(self, filter, seeds_per_side=10):
        inside_seeds_count = 0
        dx = self.length_x / (seeds_per_side - 1)
        dy = self.length_y / (seeds_per_side - 1)
        for i in range(seeds_per_side):
            x = self.x_start + i * dx
            for j in range(seeds_per_side):
                y = self.y_start + j * dy

                if filter(x, y):
                    inside_seeds_count += 1
        return inside_seeds_count

    def is_cut(self, filter, seeds_per_side=10):
        inside_seeds_count = self._count_inside_seeds(filter, seeds_per_side)
        return 0 < inside_seeds_count < seeds_per_side**self.spatial_dimensions

    def is_inside(self, filter, seeds_per_side=10):
        inside_seeds_count = self._count_inside_seeds(filter, seeds_per_side)
        return inside_seeds_count == seeds_per_side**self.spatial_dimensions

    @property
    def leaves(self):
        leaves = []
        self._get_leaves_recursive(leaves)
        return leaves

    def _get_leaves_recursive(self, leaves):
        if self.is_leaf:
            leaves.append(self)
        else:
            for child in self.children:
                child._get_leaves_recursive(leaves)

    @property
    def active_leaves(self):
        leaves = []
        self._get_active_leaves_recursive(leaves)
        return leaves

    def _get_active_leaves_recursive(self, leaves):
        if self.is_active_leaf:
            leaves.append(self)
        else:
            for child in self.children:
                child._get_leaves_recursive(leaves)

    @property
    def top_leaves(self):
        leaves = []
        self._get_top_leaves_recursive(leaves)
        return leaves

    def _get_top_leaves_recursive(self, leaves):
        if self.is_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[2]._get_top_leaves_recursive(leaves)
            self.children[3]._get_top_leaves_recursive(leaves)

    @property
    def top_active_leaves(self):
        leaves = []
        self._get_top_active_leaves_recursive(leaves)
        return leaves

    def _get_top_active_leaves_recursive(self, leaves):
        if self.is_active_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[2]._get_top_active_leaves_recursive(leaves)
            self.children[3]._get_top_active_leaves_recursive(leaves)

    @property
    def bottom_leaves(self):
        leaves = []
        self._get_bottom_leaves_recursive(leaves)
        return leaves

    def _get_bottom_leaves_recursive(self, leaves):
        if self.is_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[0]._get_bottom_leaves_recursive(leaves)
            self.children[1]._get_bottom_leaves_recursive(leaves)

    @property
    def bottom_active_leaves(self):
        leaves = []
        self._get_bottom_active_leaves_recursive(leaves)
        return leaves

    def _get_bottom_active_leaves_recursive(self, leaves):
        if self.is_active_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[0]._get_bottom_active_leaves_recursive(leaves)
            self.children[1]._get_bottom_active_leaves_recursive(leaves)

    @property
    def right_leaves(self):
        leaves = []
        self._get_right_leaves_recursive(leaves)
        return leaves

    def _get_right_leaves_recursive(self, leaves):
        if self.is_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[1]._get_right_leaves_recursive(leaves)
            self.children[3]._get_right_leaves_recursive(leaves)

    @property
    def right_active_leaves(self):
        leaves = []
        self._get_right_active_leaves_recursive(leaves)
        return leaves

    def _get_right_active_leaves_recursive(self, leaves):
        if self.is_active_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[1]._get_right_active_leaves_recursive(leaves)
            self.children[3]._get_right_active_leaves_recursive(leaves)

    @property
    def left_leaves(self):
        leaves = []
        self._get_left_leaves_recursive(leaves)
        return leaves

    def _get_left_leaves_recursive(self, leaves):
        if self.is_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[0]._get_left_leaves_recursive(leaves)
            self.children[2]._get_left_leaves_recursive(leaves)

    @property
    def left_active_leaves(self):
        leaves = []
        self._get_left_active_leaves_recursive(leaves)
        return leaves

    def _get_left_active_leaves_recursive(self, leaves):
        if self.is_active_leaf:
            leaves.append(self)
        else:
            # [child_sw, child_se, child_nw, child_ne]
            self.children[0]._get_left_active_leaves_recursive(leaves)
            self.children[2]._get_left_active_leaves_recursive(leaves)
