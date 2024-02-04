#This is an example of the file you must have in your main git branch
import perceval as pcvl
from auto_grader import score_processor
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

    pcvl.pdisplay(QPU, recursive=False)

    return QPU

    #return create_ansatz()

def create_ansatz():

    n = 6
    circuit = pcvl.GenericInterferometer(n,
        lambda i: BS(theta=pcvl.P(f"theta{i}"),
        phi_tr=pcvl.P(f"phi_tr{i}")),
        phase_shifter_fun_gen=lambda i: PS(phi=pcvl.P(f"phi{i}")))
    
    return circuit


def loss_function(params):
    # Assign parameters to circuit
    ansatz = create_ansatz()
    param_circuit = ansatz.get_parameters()

    for i, value in enumerate(params):
        param_circuit[i].set_value(value)
    # TODO: generalize n number of modes (right now 6... might change later)
    processor = pcvl.Processor("SLOS", 6, ansatz)
    loss = -score_processor(processor)
    print(f"{-loss}")
    return loss

def optimize_ansatz():
    ansatz = create_ansatz()
    param_circuit = ansatz.get_parameters()
    n_params = len(param_circuit)
    print(f"{n_params=}")
    params_init = [random.random()*np.pi for _ in param_circuit]
    
    methods = ["COBYLA"]

    o = optimize.minimize(loss_function, params_init, method="Powell", options={"maxiter": 1000})


    return o.x


def get_CCZ():
    ansatz = create_ansatz()
    best_params = optimize_ansatz()
    param_circuit = ansatz.get_parameters()

    for i, value in enumerate(best_params):
        param_circuit[i].set_value(value)

    # TODO: generalize n number of modes (right now 6... might change later)
    return pcvl.Processor("SLOS", 6, ansatz)


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

    pcvl.pdisplay(processor, recursive=False)

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

    return ca.performance, ca.fidelity.real

optimize_ansatz()
#ccz = get_CCZ()





#performance, fidelity = get_performance_and_fidelity(ccz)
#score = score_processor()

#print(f"{performance=}, {fidelity=}")
#print(f"{score=}")