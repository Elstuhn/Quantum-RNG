import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, execute
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit import QuantumCircuit


def QRNG(start:int, stop:int)->int:
    """
    Generates a number between start and stop inclusive
    """
    simulator = Aer.get_backend("qasm_simulator")
    if stop <= start:
        raise Exception("Numbers must be smaller to bigger")
    bits = np.floor(np.log2(stop) + 1) if abs(stop)>abs(start) else np.floor(np.log2(start) + 1)
    neg = False if start>=0 else True
    bits = int(bits) if not neg else int(bits)+1
    qr = QuantumRegister(bits)
    cr = ClassicalRegister(bits)
    circuit = QuantumCircuit(qr, cr)
    for i in range(bits):
        circuit.h(i)
    circuit.measure(qr, cr)
    result = execute(circuit, backend=simulator, shots=20).result()
    results = list(result.get_counts().keys())
    for i in results:
        if neg:
            sign = i[0]
            mag = i[1:]
            value = int(mag, 2)
            if int(sign):
                value = -value  
        else:
            value = int(i, 2)
        if value >= start and value <= stop:
            return value