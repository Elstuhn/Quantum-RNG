import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, execute
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.tools.visualization import plot_histogram
import matplotlib.pyplot as plt
import seaborn as sns
import time
from collections import defaultdict
import scipy.stats as ss
from tqdm import tqdm
import random 

def QRNG(start:int, stop:int)->int:
    """
    Generates a number between start and stop inclusive
    """
    startTime = time.time()
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
    time_taken = result.time_taken
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
            endTime = time.time()
            return value, endTime-startTime

totalTime = 0
values = defaultdict(int)
values2 = []
for i in tqdm(range(100000)):
    result, time_taken = QRNG(-20, 100)
    totalTime += time_taken
    values[result] += 1
    values2.append(result)
print("Average time taken:", round(totalTime/10000, 10))
keys = list(values.keys())
vals = [values[k] for k in keys]
sns.barplot(x=keys, y=vals)
plt.title("Random Number Generator Distribution")
plt.xticks(rotation=45, size=9)
plt.ylabel("Frequency")
plt.xlabel("Number Generated")
plt.show()
start = time.time()
test = ss.randint.rvs(-10, 100, size=100000)
end = time.time()
print("KS test time taken:", end-start)
ksTest = ss.kstest(values2, test)
print(ksTest)
print("Kolmogorov-Smirnov Test Results:")
print("Test statistic:", ksTest[0])
print("P-value:", round(ksTest[1], 5))
start = time.time()
random.randint(1, 100)
end = time.time()
print(end-start)
