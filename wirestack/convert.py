from qiskit import QuantumCircuit
from .gates import Gate


def to_qiskit(circuit: list[Gate], num_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(num_qubits)
    for g in circuit:
        getattr(qc, g.name)(*g.params, *g.qubits)
    return qc