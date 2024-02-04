#!/usr/bin/env python3


# Designing Optical Circuit using Perceval Quandela
# We are going to use 9 modes
# 3 qubits and 3 ancilla modes
# i.e. CCZ gate with 6 heralded modes (3 qubits)
# only three ancilla photons are sufficient to implement a three-qubit Toffoli gate with high fidelity,
# we use the same method for CCZ constrcution
# Need to find the unitary matrix U, that performs the desired transformation 
# This unitary matrix U is special and know that U: is Uij = Uji = δij for i = 2, 4, 6, i.e., U is
# designed to act nontrivially only on the computational modes 1, 3, and 5.
# Therefore we expect something like
# | 1   0   0   0   0   0   0   0   0 |
# | 0   φ1  0   0   0   0   0   0   0 |
# | 0   0   1   0   0   0   0   0   0 |
# | 0   0   0   φ2  0   0   0   0   0 |
# | 0   0   0   0   1   0   0   0   0 |
# | 0   0   0   0   0   φ3  0   0   0 |
# | 0   0   0   0   0   0   1   0   0 |
# | 0   0   0   0   0   0   0   d   0 |
# | 0   0   0   0   0   0   0   0   1 |

# Import libraries 

#This is an example of the file you must have in your main git branch
import perceval as pcvl
from perceval.components import Circuit, Processor, BS, PERM, Port, Unitary
from perceval.utils import Encoding, PostSelect, Matrix
import sympy as sp
import numpy as np

# from tqdm.auto import tqdm
import numpy as np
from scipy.optimize import minimize
import random
import matplotlib.pyplot as plt
simulator = pcvl.Simulator(pcvl.NaiveBackend())
     

import numpy as np


def get_CNOT() -> pcvl.Processor:
    """
    Returns a CNOT gate with S = 2/27, known as Kml's CNOT.

    Returns:
        pcvl.Processor: Processor representing the CNOT gate.
    """
    return pcvl.catalog["klm_cnot"].build_processor()

def create_ccz_with_cnot_and_rx_and_hadamard() -> pcvl.Processor:
    """
    Creates a linear optical circuit for implementing the CCZ gate using dual-rail encoding.

    Returns:
        pcvl.Processor: Processor representing the CCZ gate circuit.
    """

    # Define parameters for the T and T-dagger gates
    tetha = np.pi / 4
    tetha_dg = -(np.pi / 4)

    # Define a source for the linear optical circuit
    source = pcvl.Source(emission_probability=0.4, multiphoton_component=0.1)

    # Obtain the CNOT gate with S = 2/27
    cnot = get_CNOT()

    # Create a processor for the CCZ gate circuit
    QPU = pcvl.Processor("SLOS", 9, source)

    # Add dual encoding to the qubits
    QPU.add_port(0, Port(Encoding.DUAL_RAIL, 'ctrl0'))
    QPU.add_port(2, Port(Encoding.DUAL_RAIL, 'ctrl1'))
    QPU.add_port(4, Port(Encoding.DUAL_RAIL, 'data'))
        # Build the CCZ circuit
    QPU.add([2, 3, 4, 5], cnot)  # CNOT on qubits 2 and 3 (control) and 4 (target)

    # Add T-dagger gate to qubit 2
    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=tetha_dg))
    QPU.add(4, BS.H())

    QPU.add([0, 1, 4, 5], cnot)  # CNOT on qubits 0 and 1 (control) and 4 (target)

    # Add T gate to qubit 2
    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=tetha))
    QPU.add(4, BS.H())

    QPU.add([2, 3, 4, 5], cnot)  # CNOT on qubits 2 and 3 (control) and 4 (target)

    # Add T-dagger gate to qubit 2
    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=tetha_dg))
    QPU.add(4, BS.H())

    QPU.add([0, 1, 4, 5], cnot)  # CNOT on qubits 0 and 1 (control) and 4 (target)

    # Add T gate to qubit 1
    QPU.add(2, BS.H())
    QPU.add(2, BS.Rx(theta=tetha))
    QPU.add(2, BS.H())

    # Add T gate to qubit 2
    QPU.add(4, BS.H())
    QPU.add(4, BS.Rx(theta=tetha))
    QPU.add(4, BS.H())

    QPU.add([0, 1, 2, 3], cnot)  # CNOT on qubits 0 and 1 (control) and 2 (target)

    # Add T gate to qubit 0
    QPU.add(0, BS.H())
    QPU.add(0, BS.Rx(theta=tetha))
    QPU.add(0, BS.H())

    # Add T-dagger gate to qubit 1
    QPU.add(2, BS.H())
    QPU.add(2, BS.Rx(theta=tetha_dg))
    QPU.add(2, BS.H())

    return QPU




def VQE_optimise_params():
    #List of the parameters φ1,φ2,...,φ8
    List_Parameters=[] # to store the parameters used in the ansatz.
    # VQE is a 6 optical mode circuit
    VQE=pcvl.Circuit(9) # Circuit Initialization
    pass

def get_CCZ():
    return 
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


performance, fidelity = get_performance_and_fidelity(ccz)

print(f"{performance=}, {fidelity=}")
