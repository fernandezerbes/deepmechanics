class Refinement:
    def __init__(self, depth):
        self.depth = depth


class RefineBoundaries(Refinement):
    def __init__(self, depth, domain):
        super().__init__(depth)
        self.domain = domain

    def refine(self, grid, seeds_per_side=10):
        for cell in grid.base_cells:
            self.refine_recursive(cell, self.domain, self.depth, seeds_per_side)

    def refine_recursive(self, cell, domain, depth, seeds_per_side=10):
        if depth != 0 and cell.is_cut(domain, seeds_per_side):
            cell.refine()
            for child in cell.children:
                if child.is_cut(domain, seeds_per_side):
                    self.refine_recursive(child, domain, depth - 1, seeds_per_side)


class AgregatedRefinementStrategy:
    def __init__(self, *strategies):
        self.strategies = [strategy for strategy in strategies]

    def refine(self, grid, seeds_per_side=10):
        for strategy in self.strategies:
            for cell in grid.base_cells:
                self.refine_recursive(cell, self.domain, self.depth, seeds_per_side)
