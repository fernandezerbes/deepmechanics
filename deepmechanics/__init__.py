import sys

import deepmechanics.boundarycondition
import deepmechanics.cell
import deepmechanics.grid
import deepmechanics.implicitgeometry
import deepmechanics.kinematics
import deepmechanics.materialmodel
import deepmechanics.model
import deepmechanics.neuralnetwork
import deepmechanics.refinement
import deepmechanics.utilities

sys.path.append("..")

print("\n")
print(
    "██████╗ ███████╗███████╗██████╗ ███╗   ███╗███████╗ ██████╗██╗  ██╗ █████╗ ███╗   ██╗██╗ ██████╗███████╗"
)
print(
    "██╔══██╗██╔════╝██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝██║  ██║██╔══██╗████╗  ██║██║██╔════╝██╔════╝"
)
print(
    "██║  ██║█████╗  █████╗  ██████╔╝██╔████╔██║█████╗  ██║     ███████║███████║██╔██╗ ██║██║██║     ███████╗"
)
print(
    "██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██║╚██╔╝██║██╔══╝  ██║     ██╔══██║██╔══██║██║╚██╗██║██║██║     ╚════██║"
)
print(
    "██████╔╝███████╗███████╗██║     ██║ ╚═╝ ██║███████╗╚██████╗██║  ██║██║  ██║██║ ╚████║██║╚██████╗███████║"
)
print(
    "╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝     ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝╚══════╝"
)
print("\n                               Created by Federico Fernández Erbes")
print("                                   All results without warranty\n")
