import random
from qiskit.quantum_info import Operator
from wirestack.optimize import optimize
from wirestack.convert import to_qiskit
from wirestack.random_circuit import random_gate


def test_random_circuits_preserve_unitary():
    rng = random.Random(42)
    for _ in range(300):
        n = rng.randint(2, 4)
        c = [random_gate(rng, n) for _ in range(rng.randint(5, 40))]
        out = optimize(c, n)
        assert len(out) <= len(c)
        assert Operator(to_qiskit(c, n)).equiv(Operator(to_qiskit(out, n)))