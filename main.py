import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, execute
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.tools.visualization import plot_histogram
import matplotlib.pyplot as plt

def QRNG(start:int, stop:int)->int:
    """
    Generates a number between start and stop inclusive
    """
    simulator = Aer.get_backend("qasm_simulator")
    if stop <= start:
        raise Exception("Numbers must be smaller to bigger")
    bits = np.floor(np.log2(stop) + 1)
    bits = int(bits)
    qr = QuantumRegister(bits)
    cr = ClassicalRegister(bits)
    circuit = QuantumCircuit(qr, cr)
    for i in range(bits):
        circuit.h(i)
    circuit.measure(qr, cr)
    circuit.draw(output="mpl")
    result = execute(circuit, backend=simulator, shots=10000).result()
    plot_histogram(result.get_counts(circuit))
    plt.show()

QRNG(1, 10)