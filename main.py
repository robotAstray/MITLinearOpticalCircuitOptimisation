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


def create_ccz_with_cnot_and_rx_and_hadamard():
    QPU = pcvl.Processor("SLOS", 6)

    QPU.add_port(0, Port(Encoding.DUAL_RAIL, 'ctrl0'))
    QPU.add_port(2, Port(Encoding.DUAL_RAIL, 'ctrl1'))
    QPU.add_port(4, Port(Encoding.DUAL_RAIL, 'data'))

    QPU.add([2, 3, 4, 5], catalog["heralded cnot"].build_processor())

    theta = np.pi / 4

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=-theta))
    QPU.add(4, BS.H())


    QPU.add([0, 1, 4, 5], catalog["heralded cnot"].build_processor())

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=theta))
    QPU.add(4, BS.H())

    QPU.add([2, 3, 4, 5], catalog["heralded cnot"].build_processor())

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=-theta))
    QPU.add(4, BS.H())

    QPU.add([0, 1, 4, 5], catalog["heralded cnot"].build_processor())

    QPU.add(2, BS.H())
    QPU.add(2, BS.Rx(theta=theta))
    QPU.add(2, BS.H())

    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=theta))
    QPU.add(4, BS.H())

    QPU.add([0, 1, 2, 3], catalog["heralded cnot"].build_processor())

    QPU.add(0, BS.H())
    QPU.add(0, BS.Rx(theta=theta))
    QPU.add(0, BS.H())

    QPU.add(2, BS.H())
    QPU.add(2, BS.Rx(theta=-theta))
    QPU.add(2, BS.H())

    pcvl.pdisplay(QPU, recursive=False)

    return QPU

def get_CCZ() -> pcvl.Processor:
    return create_ccz_with_cnot_and_rx_and_hadamard()
    return pcvl.catalog["postprocessed ccz"].build_processor()
    #return create_ansatz()

def create_ansatz(ancillas):
    # Processor(kwargs.get("backend", "SLOS"), self.build_circuit(**kwargs), name=kwargs.get("name"))
    List_Parameters=[]

    p = pcvl.Processor("SLOS", 6 + ancillas)


    return p, List_Parameters

def optimize_ansatz(ansatz):
    """
    tq = tqdm(desc='Minimizing...') #Displaying progress bar
    radius1=[]
    E1=[]
    init_param=[]

    H=H1

    for R in range(len(H)):            #We try to find the ground state eigenvalue for each radius R
        radius1.append(H[R][0])
        if (init_param==[]):           #
                init_param = [2*(np.pi)*random.random() for _ in List_Parameters]
        else:
            for i in range(len(init_param)):
                init_param[i]=p.get_parameters()[i]._value

    """





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


ccz = get_CCZ()


def loss_function(processor):

    return -score_processor(processor)




performance, fidelity = get_performance_and_fidelity(ccz)
score = score_processor()

print(f"{performance=}, {fidelity=}")
print(f"{score=}")