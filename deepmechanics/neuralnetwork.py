import torch.nn as nn


class NeuralNetwork(nn.Sequential):
    def __init__(
        self,
        input_dimension,
        nodes_count_in_hidden_layers,
        output_dimension,
        activation=nn.Tanh,
    ):
        super().__init__()

        # Input layer
        self.add_module(
            "input", nn.Linear(input_dimension, nodes_count_in_hidden_layers[0])
        )
        self.add_module("activation_0", activation())

        # Hidden layers
        for i in range(len(nodes_count_in_hidden_layers) - 1):
            self.add_module(
                "linear_" + str(i + 1),
                nn.Linear(
                    nodes_count_in_hidden_layers[i], nodes_count_in_hidden_layers[i + 1]
                ),
            )
            self.add_module("activation_" + str(i + 1), activation())

        # Output layer
        self.add_module(
            "output", nn.Linear(nodes_count_in_hidden_layers[-1], output_dimension)
        )

        self.double()  # Use dtype=float64
