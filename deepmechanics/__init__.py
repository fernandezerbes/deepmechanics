import deepmechanics.cell
import deepmechanics.grid
import deepmechanics.implicitgeometry
import deepmechanics.refinement
import deepmechanics.neuralnetwork
import deepmechanics.utilities
import deepmechanics.model
import deepmechanics.materialmodel
import deepmechanics.kinematics
import deepmechanics.boundarycondition
import sys
sys.path.append('..')

print("\n")
print("██████╗ ███████╗███████╗██████╗ ███╗   ███╗███████╗ ██████╗██╗  ██╗ █████╗ ███╗   ██╗██╗ ██████╗███████╗")
print("██╔══██╗██╔════╝██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝██║  ██║██╔══██╗████╗  ██║██║██╔════╝██╔════╝")
print("██║  ██║█████╗  █████╗  ██████╔╝██╔████╔██║█████╗  ██║     ███████║███████║██╔██╗ ██║██║██║     ███████╗")
print("██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██║╚██╔╝██║██╔══╝  ██║     ██╔══██║██╔══██║██║╚██╗██║██║██║     ╚════██║")
print("██████╔╝███████╗███████╗██║     ██║ ╚═╝ ██║███████╗╚██████╗██║  ██║██║  ██║██║ ╚████║██║╚██████╗███████║")
print("╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝     ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝╚══════╝")
print("\n                               Created by Federico Fernández Erbes")
print("                                   All results without warranty\n")