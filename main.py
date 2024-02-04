#This is an example of the file you must have in your main git branch
import perceval as pcvl
from auto_grader import loss_function_prob_amplitudes
from scipy.optimize import minimize
import random

import perceval as pcvl
from perceval.components.unitary_components import PS, BS, PERM
from perceval.components import Circuit, Processor, PERM, BS, Port
import numpy as np
from perceval.utils import Encoding, PostSelect
from perceval.components import BS, Circuit, catalog
from scipy import optimize


def create_ccz_with_cnot_and_rx_and_hadamard(cnot="postprocessed cnot"):
    QPU = pcvl.Processor("SLOS", 6)

    QPU.add_port(0, Port(Encoding.DUAL_RAIL, 'ctrl0'))
    QPU.add_port(2, Port(Encoding.DUAL_RAIL, 'ctrl1'))
    QPU.add_port(4, Port(Encoding.DUAL_RAIL, 'data'))

    QPU.add([2, 3, 4, 5], catalog[cnot].build_processor())

    theta = np.pi / 4

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=-theta))
    QPU.add(4, BS.H())


    QPU.add([0, 1, 4, 5], catalog[cnot].build_processor())

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=theta))
    QPU.add(4, BS.H())

    QPU.add([2, 3, 4, 5], catalog[cnot].build_processor())

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=-theta))
    QPU.add(4, BS.H())

    QPU.add([0, 1, 4, 5], catalog[cnot].build_processor())

    QPU.add(2, BS.H())
    QPU.add(2, BS.Rx(theta=theta))
    QPU.add(2, BS.H())

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=theta))
    QPU.add(4, BS.H())

    QPU.add([0, 1, 2, 3], catalog[cnot].build_processor())

    QPU.add(0, BS.H())
    QPU.add(0, BS.Rx(theta=theta))
    QPU.add(0, BS.H())

    QPU.add(2, BS.H())
    QPU.add(2, BS.Rx(theta=-theta))
    QPU.add(2, BS.H())


    return QPU

    #return create_ansatz()

def VQE_optimise_params():
    #List of the parameters φ1,φ2,...,φ8
    List_Parameters=[] # to store the parameters used in the ansatz.
    # VQE is a 6 optical mode circuit
    VQE=pcvl.Circuit(9) # Circuit Initialization
    # add entry for mode 0

    List_Parameters.append(pcvl.Parameter("φ1"))
    VQE.add((1, 3),pcvl.PS(phi=List_Parameters[-1]))

    List_Parameters.append(pcvl.Parameter("φ2"))
    VQE.add((3, 5),pcvl.PS(phi=List_Parameters[-1]))

    List_Parameters.append(pcvl.Parameter("φ3"))
    VQE.add((5, ),pcvl.PS(phi=List_Parameters[-1]))

    List_Parameters.append(pcvl.Parameter("φ4"))
    VQE.add((5,),pcvl.PS(phi=List_Parameters[-1]))

    return VQE

def create_vqe_ansatz_old():
    List_Parameters = []
    VQE=pcvl.Circuit(6)

    VQE.add((1,2), pcvl.BS())
    VQE.add((3,4), pcvl.BS())
    List_Parameters.append(pcvl.Parameter("φ1"))
    VQE.add((2,),pcvl.PS(phi=List_Parameters[-1]))
    List_Parameters.append(pcvl.Parameter("φ3"))
    VQE.add((4,),pcvl.PS(phi=List_Parameters[-1]))
    VQE.add((1,2), pcvl.BS())
    VQE.add((3,4), pcvl.BS())
    List_Parameters.append(pcvl.Parameter("φ2"))
    VQE.add((2,),pcvl.PS(phi=List_Parameters[-1]))
    List_Parameters.append(pcvl.Parameter("φ4"))
    VQE.add((4,),pcvl.PS(phi=List_Parameters[-1]))


    # CNOT ( Post-selected with a success probability of 1/9)
    VQE.add([0,1,2,3,4,5], pcvl.PERM([0,1,2,3,4,5]))#Identity PERM (permutation) for the purpose of drawing a nice circuit
    VQE.add((3,4), pcvl.BS())
    VQE.add([0,1,2,3,4,5], pcvl.PERM([0,1,2,3,4,5]))#Identity PERM (permutation) for the same purpose
    VQE.add((0,1), pcvl.BS(pcvl.BS.r_to_theta(1/3)))
    VQE.add((2,3), pcvl.BS(pcvl.BS.r_to_theta(1/3)))
    VQE.add((4,5), pcvl.BS(pcvl.BS.r_to_theta(1/3)))
    VQE.add([0,1,2,3,4,5], pcvl.PERM([0,1,2,3,4,5]))#Identity PERM (permutation) for the same purpose
    VQE.add((3,4), pcvl.BS())
    VQE.add([0,1,2,3,4,5], pcvl.PERM([0,1,2,3,4,5]))#Identity PERM (permutation) for the same purpose

    List_Parameters.append(pcvl.Parameter("φ5"))
    VQE.add((2,),pcvl.PS(phi=List_Parameters[-1]))
    List_Parameters.append(pcvl.Parameter("φ7"))
    VQE.add((4,),pcvl.PS(phi=List_Parameters[-1]))
    VQE.add((1,2), pcvl.BS())
    VQE.add((3,4), pcvl.BS())
    List_Parameters.append(pcvl.Parameter("φ6"))
    VQE.add((2,),pcvl.PS(phi=List_Parameters[-1]))
    List_Parameters.append(pcvl.Parameter("φ8"))
    VQE.add((4,),pcvl.PS(phi=List_Parameters[-1]))
    VQE.add((1,2), pcvl.BS())
    VQE.add((3,4), pcvl.BS())

    return VQE


N = 9
def create_vqe_ansatz():
    #List of the parameters φ1,φ2,...,φ8
    List_Parameters=[] # to store the parameters used in the ansatz.
    # VQE is a 6 optical mode circuit
    VQE=pcvl.Processor("SLOS", N) # Circuit Initialization

    VQE.add_port(0, Port(Encoding.DUAL_RAIL, 'ctrl0'))
    VQE.add_port(2, Port(Encoding.DUAL_RAIL, 'ctrl1'))
    VQE.add_port(4, Port(Encoding.DUAL_RAIL, 'data'))


    # add Beam Splitter on mode 1, 3, 5
    List_Parameters.append(pcvl.Parameter("φ1"))
    VQE.add([1],pcvl.PS(phi=List_Parameters[-1]))

    List_Parameters.append(pcvl.Parameter("φ2"))
    VQE.add([3],pcvl.PS(phi=List_Parameters[-1]))

    List_Parameters.append(pcvl.Parameter("φ3"))
    VQE.add([5],pcvl.PS(phi=List_Parameters[-1]))


    VQE = VQE.add_herald(6,0).add_herald(7,0).add_herald(8,0)
    VQE.set_postselection(PostSelect("[0,1]==1 & [2,3]==1 & [4,5]==1"))

    return VQE

def create_ansatz():

    return create_vqe_ansatz()
    

def assign_processor_params(processor, params):
    param_circuit = processor.get_circuit_parameters()

    for i, (k, param) in enumerate(param_circuit.items()):
        param.set_value(params[i])

def loss_function(params):
    # Assign parameters to circuit
    ansatz = create_ansatz()

    assign_processor_params(ansatz, params)

    loss = loss_function_prob_amplitudes(ansatz)
    print(f"{loss=}")

    return loss
def optimize_ansatz():
    ansatz = create_ansatz()
    param_circuit = ansatz.get_circuit_parameters()
    n_params = len(param_circuit)
    print(f"{n_params=}")
    params_init = [random.random()*np.pi for _ in param_circuit]
    
    methods = ["COBYLA"]

    o = optimize.minimize(loss_function, params_init, method="COBYLA", options={"maxiter": 100, "rhobge": 0.2})


    return o.x


def get_CCZ():
    ansatz = create_ansatz()
    best_params = optimize_ansatz()

    assign_processor_params(ansatz, best_params)

    return ansatz 


def get_performance_and_fidelity(ccz_processor):
    processor = pcvl.Processor("SLOS", 6)
    processor.add(4, pcvl.BS.H())
    processor.add(0, ccz_processor)
    processor.add(4, pcvl.BS.H())

    states = {
        pcvl.BasicState([1, 0, 1, 0, 1, 0]): "000",  # |000⟩
        pcvl.BasicState([1, 0, 1, 0, 0, 1]): "001",  # |001⟩
        pcvl.BasicState([1, 0, 0, 1, 1, 0]): "010",  # |010⟩
        pcvl.BasicState([1, 0, 0, 1, 0, 1]): "011",  # |011⟩
        pcvl.BasicState([0, 1, 1, 0, 1, 0]): "100",  # |100⟩
        pcvl.BasicState([0, 1, 1, 0, 0, 1]): "101",  # |101⟩
        pcvl.BasicState([0, 1, 0, 1, 1, 0]): "110",  # |110⟩
        pcvl.BasicState([0, 1, 0, 1, 0, 1]): "111",  # |111⟩
    }


    ca = pcvl.algorithm.Analyzer(processor, states)

    #pcvl.pdisplay(processor, recursive=False)

    truth_table = {
        "000": "000",  # No change
        "001": "001",  # No change
        "010": "010",  # No change
        "011": "011",  # No change
        "100": "100",  # No change
        "101": "101",  # No change
        "110": "111",  # Target flips
        "111": "110",  # Target flips
    }

    ca.compute(expected=truth_table)

    state = pcvl.BasicState("|0,1,0,1,0,1>")

    sim = pcvl.SimulatorFactory().build(processor)

    return ca.performance, ca.fidelity.real


optimize_ansatz()
#ccz = get_CCZ()





#performance, fidelity = get_performance_and_fidelity(ccz)
#score = score_processor()

#print(f"{performance=}, {fidelity=}")
#print(f"{score=}")