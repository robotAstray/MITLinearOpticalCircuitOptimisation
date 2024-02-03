# Numbering is based on the suggested timeline

import perceval as pcvl
import perceval.components.unitary_components as comp
from perceval.rendering.circuit import SymbSkin, PhysSkin
import numpy as np

##### STEP 1 #####
theta_0 = 54.74 * np.pi / 180
theta_1 = 17.63 * np.pi / 180

QPU = pcvl.Processor("SLOS", 4)

QPU.add(0, comp.PS(phi=np.pi))
QPU.add(1, comp.PS(phi=np.pi))

# The list commented after each line of code represents the current ordering of
# the cables at that point, i.e. 2, 0, 3, 1 means cable 2 is now in 1st position
# and cable 1 is in last.
QPU.add([0,2], comp.BS(theta=theta_0)) # 2, 0, 1, 3
QPU.add([2,3], comp.BS(theta=theta_0)) # 2, 0, 3, 1
QPU.add([1,3], comp.BS(theta=theta_0)) # 2, 1, 0, 3
QPU.add([0,3], comp.BS(theta=theta_0)) # 3, 2, 1, 0

QPU.with_input(pcvl.BasicState([0,0,1,1]))

pcvl.pdisplay(QPU, recursive=True, skin=PhysSkin())

##### STEP 2 #####

##### STEP 3 #####

##### STEP 4 #####

##### STEP 5 #####