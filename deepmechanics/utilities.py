import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from torch import device, float64, ones, tensor
from torch.autograd import grad


def make_array_unique(array):
    return list(set(array))


def get_derivative(y, x, n, device=device("cpu")):
    if n == 0:
        return y
    else:
        dy_dx = grad(
            y,
            x,
            ones(x.size()[0], 1, device=device),
            create_graph=True,
            retain_graph=True,
        )[0]
        return get_derivative(dy_dx, x, n - 1)


def tensorize_1d(x):
    if isinstance(x, (int, float)):
        return tensor([x], requires_grad=True, dtype=float64)
    elif isinstance(x, list):
        return tensor([x], requires_grad=True, dtype=float64).transpose(0, 1)
    else:
        raise TypeError("Values must be int, float or list")


def tensorize_2d(x, y):
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return tensor([x, y], requires_grad=True, dtype=float64)
    elif isinstance(x, list) and isinstance(y, list):
        return tensor([x, y], requires_grad=True, dtype=float64).transpose(0, 1)
    else:
        raise TypeError("Values must be int, float or list")


def tensorize_3d(x, y, z):
    if (
        isinstance(x, (int, float))
        and isinstance(y, (int, float))
        and isinstance(z, (int, float))
    ):
        return tensor([x, y, z], requires_grad=True, dtype=float64)
    elif isinstance(x, list) and isinstance(y, list) and isinstance(z, list):
        return tensor([x, y, z], requires_grad=True, dtype=float64).transpose(0, 1)
    else:
        raise TypeError("Values must be int, float or list")


def plot_grid(grid):
    fig, ax = plt.subplots()

    for cell in grid.leaf_cells:
        if cell.is_active:
            rect = Rectangle(
                (cell.x_start, cell.y_start),
                cell.length_x,
                cell.length_y,
                ec="r",
                fc="k",
            )

            ax.add_patch(rect)

    ax.set(xlim=(grid.x_start, grid.x_end), ylim=(grid.y_start, grid.y_end))
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


def plot_field(xs, ys, field, title, levels=12):
    # Make tensors 1D
    xs = xs.detach().flatten()
    ys = ys.detach().flatten()
    field = field.detach().flatten()

    # Set up plot
    fig, ax = plt.subplots(1, 1)
    plt.gca().set_aspect("equal", adjustable="box")
    ax.set_title(title)
    ax.axis("off")

    # Plot the field
    cp = ax.tricontourf(xs, ys, field, levels=levels, cmap=plt.cm.jet)

    # Add a colorbar to the plot
    fig.colorbar(cp)

    plt.show()
