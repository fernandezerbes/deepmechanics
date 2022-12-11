from deepmechanics.boundarycondition import (
    AggregatedDirichletBoundaryCondition,
    FixedDisplacementsOnLeftEdge,
    FixedDisplacementsOnRightEdge,
    NeumannBoundaryCondition,
)
from deepmechanics.functional import PotentialEnergyFunctional
from deepmechanics.grid import TensorizedPlanarCartesianGrid
from deepmechanics.kinematics import LinearKinematicLaw
from deepmechanics.materialmodel import LinearElasticPlaneStressMaterialModel
from deepmechanics.model import MechanicalModel
from deepmechanics.neuralnetwork import NeuralNetwork
from deepmechanics.utilities import plot_field

# Define the computational grid
x_start = 0.0
y_start = 0.0
x_end = 10
y_end = 1
resolution_x = 20
resolution_y = 10

grid = TensorizedPlanarCartesianGrid(
    x_start, y_start, x_end, y_end, resolution_x, resolution_y
)
grid.prepare_samples(number_of_samples_x=100, number_of_samples_y=100)

# Neural network
nodes_per_hidden_layer = [50, 50]
nn = NeuralNetwork(
    grid.spatial_dimensions, nodes_per_hidden_layer, grid.spatial_dimensions
)

# Dirichlet boundary conditions
dirichlet_bc1 = FixedDisplacementsOnLeftEdge(grid)
dirichlet_bc2 = FixedDisplacementsOnRightEdge(grid)
dirichlet_bcs = AggregatedDirichletBoundaryCondition(dirichlet_bc1, dirichlet_bc2)

# Neumann boundary conditions
edge_load = lambda coords: (0, -1)  # [force / length^2]
edge_data = grid.top_edge_integration_points_data
edge_displacement_constraint = dirichlet_bcs.get_constraint_on_top_edge()
edge_load_on_top_bc = NeumannBoundaryCondition(
    edge_load, edge_data, edge_displacement_constraint
)

# Kinematics
kinematic_law = LinearKinematicLaw()

# Material model
youngs_modulus = 100
poissons_ratio = 0.3
thickness = 0.1
material_model = LinearElasticPlaneStressMaterialModel(
    youngs_modulus, poissons_ratio, thickness
)

# Functional
functional = PotentialEnergyFunctional(neumann_bcs=edge_load_on_top_bc)

# Model
model = MechanicalModel(
    nn, grid, dirichlet_bcs, functional, kinematic_law, material_model
)

# Solution
model.solve(epochs=1000, lr=1e-2)

# Plot results
constraint_on_samples = dirichlet_bcs.get_constraint_on_samples()
ux, uy = model.get_displacements(grid.samples_coords, constraint_on_samples)
nx, ny, nxy = model.get_stresses(grid.samples_coords, constraint_on_samples)

plot_field(grid.samples_xs, grid.samples_ys, ux, "$u_x$", 12)
plot_field(grid.samples_xs, grid.samples_ys, uy, "$u_y$", 12)
