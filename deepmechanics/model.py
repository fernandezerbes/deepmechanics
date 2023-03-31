import torch


class Model:
    def __init__(self, approximator, grid, dirichlet_bcs, functional):
        self.approximator = approximator
        self.grid = grid
        self.dirichlet_bcs = dirichlet_bcs
        self.functional = functional
        self.optimizer = None
        self.total_energy = None

    def solve(self):
        raise (NotImplementedError, "Solve method not overriden in derived class")

    def get_solution_at(self, coords):
        return self.approximator(coords)


class MechanicalModel(Model):
    def __init__(
        self,
        approximator,
        grid,
        dirichlet_bcs,
        functional,
        kinematic_law,
        material_model,
    ):
        super().__init__(approximator, grid, dirichlet_bcs, functional)
        self.kinematic_law = kinematic_law
        self.material_model = material_model

    def get_displacements(self, coords, constraint):
        displacements = self.approximator(coords)

        ux = displacements[:, 0].view(-1, 1)
        uy = displacements[:, 1].view(-1, 1)

        return constraint(ux, uy)

    def get_strains(self, coords, constraint):
        ux, uy = self.get_displacements(coords, constraint)
        return self.kinematic_law.compute_strains(ux, uy, coords)

    def get_stresses(self, coords, constraint):
        ex, ey, gamma_xy = self.get_strains(coords, constraint)
        return self.material_model.compute_stresses(ex, ey, gamma_xy)

    def closure(self):
        self.optimizer.zero_grad()
        self.total_energy.backward(retain_graph=True)

        return self.total_energy

    def solve(self, epochs=100, early_stopping=True, optimizer=None, **kwargs):
        if not optimizer:
            optimizer = torch.optim.Adam(self.approximator.parameters(), **kwargs)

        self.optimizer = optimizer

        # Get data for training
        coords, weights, jacobian_dets = self.grid.integration_points_data
        constraint = self.dirichlet_bcs.get_constraint_on_integration_points()

        print("\033[1mStarting neural network training...\033[0m")

        # Train
        for i in range(epochs + 1):
            # Predict field quantities
            ux, uy = self.get_displacements(coords, constraint)
            ex, ey, gamma_xy = self.kinematic_law.compute_strains(ux, uy, coords)
            nx, ny, nxy = self.material_model.compute_stresses(ex, ey, gamma_xy)

            # Get energy values
            internal_energy = self.functional.internal_term(
                ex, ey, gamma_xy, nx, ny, nxy, weights, jacobian_dets
            )

            external_energy = self.functional.external_term(self.get_displacements)

            source_energy = self.functional.source_term(
                ux, uy, coords, weights, jacobian_dets
            )

            print(
                "\033[1mEpoch\033[0m = {}\t \033[1mInternal energy\033[0m = {:.4e}\t \033[1mExternal energy\033[0m = {:.4e}\t \033[1mSource energy\033[0m = {:.4e}".format(
                    i,
                    internal_energy,
                    external_energy.detach().numpy(),
                    source_energy.detach().numpy(),
                )
            )

            self.total_energy = internal_energy + external_energy + source_energy

            optimizer.step(self.closure)

        print("\033[1mFinished training!\033[0m")
