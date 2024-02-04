# Linear Optical Circuits Optimisation
MIT Quantum Computing Competition - Quandela Challenge

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Installation](#2-installation)
- [3. Usage](#3-usage)
- [4. Optimization Techniques](#4-optimization-techniques)
- [5. Results](#5-results)
- [6. Future Work](#6-future-work)
- [7. Contributors](#7-contributors)
- [8. License](#8-license)

## 1. Introduction

This project aims to replicate and implement the findings detailed in [[1]](https://www.semanticscholar.org/paper/Quantum-gates-using-linear-optics-and-postselection-Knill/17d7ca6fc3bb99d14f75be708409a2350d72bbae), authored by Knill, E. (2002). The initial phase involves reproducing the results obtained by Knill. Following this, we will apply the same methodology used by Knill (2002) or explore alternative approaches to solve the problem outlined in [[6]](https://journals.aps.org/pra/pdf/10.1103/PhysRevA.79.042326).

The goa of the project is to construct a CCZ using an optimal Linear Optical Circuits using the perceval library.

Optimising the linear optics circuit involves tweaking parameters, e.g. beam splitter ratios, phase shifts, and other optical elements to achieve desired outcomes. To do so we used VQE algorithm.


## 2. Installation

The project was developed using a virtual environment. Please follow the steps below to install `venv`. Note that these instructions are for Linux/Unix-based systems. For Windows machines, please see the instructions [here](https://it.engineering.oregonstate.edu/setting-virtual-environments-python).

## 3. Usage

Use the `autograder.py` to check the work
## 4. Optimization Techniques
We used VQE algorithm and designed amn ansatz following the methodology from [6]


### Implementation of `get_CCZ()` Function:

To implement the `get_CCZ()` function, we follow the design principles gathered from [paper 6]:

**Design:**

- We use dual-rail encoding, where the computational state consists of Mc photons in Nc = 2M optical modes, with Mc = 3. Therefore, we have Nc = 6 optical modes for the qubits. Additionally, 3 modes are reserved for unoccupied ancilla, Na.
- Modes distribution:
  - Modes 0-1 represent qubit 1 (control - qubit).
  - Modes 2-3 represent qubit 2 (control - qubit).
  - Modes 4-5 represent qubit 3 (target - qubit).
  - Modes 6, 7, and 8 are unentangled ancilla photons.
- The measurement is applied to the ancilla modes.

**Transformation:**

The transformation is represented as (a_in)i† → (U)i,j (a_out)j†. We need to find the entry of U = N x N = 9 x 9, where N is the total number of modes, i.e., Nc + Na = 9. The matrix U is defined as exp(sum(xj * Hj)), with the sum running from j=1 to N^2. Here, Hj is a complete set of complex anti-Hermitian N x N matrices.

**Ansatz for U:**

To reduce the parameter space and improve convergence, an ansatz for U is considered: U_ij = U_ji = δij for i = 2, 4, 6. This means U acts nontrivially only on computational modes 1, 3, and 5.



**Circuit Implementation:**

see function in `main.py`

**Procedure:**


**Controlled Application:**  


**Refinement and Optimization:** 



**Post-Selection with Ancillas:** 

Ancilla qubits for post-selection are used

### 4.1 Goal of the Project
## 5. Results
## 6. Future Work
## 7. Contributors
## 8. License
## 9. References

[[1]]() Aaronson, S., & Arkhipov, A. (2011, June). The computational complexity of linear optics. In Proceedings of the forty-third annual ACM symposium on Theory of computing (pp. 333-342).

[[2]]() Reck, M., Zeilinger, A., Bernstein, H. J., & Bertani, P. (1994). Experimental realization of any discrete unitary operator. Physical review letters, 73(1), 58.

[[3]]() Clements, W. R., Humphreys, P. C., Metcalf, B. J., Kolthammer, W. S., & Walmsley, I. A. (2016). Optimal design for universal multiport interferometers. Optica, 3(12), 1460-1465.

[[4]]() Knill, E., Laflamme, R., & Milburn, G. J. (2001). A scheme for efficient quantum computation with linear optics. nature, 409(6816), 46-52.

[[5]](https://www.semanticscholar.org/paper/Quantum-gates-using-linear-optics-and-postselection-Knill/17d7ca6fc3bb99d14f75be708409a2350d72bbae) Knill, E. (2002). Quantum gates using linear optics and postselection. Physical Review A, 66(5), 052306.

[[6]](https://journals.aps.org/pra/pdf/10.1103/PhysRevA.79.042326) Uskov, D. B., Kaplan, L., Smith, A. M., Huver, S. D., & Dowling, J. P. (2009). Maximal success probabilities of linear-optical quantum gates. Physical Review A, 79(4), 042326.
