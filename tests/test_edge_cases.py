import math
from qiskit.quantum_info import Operator
from wirestack.gates import Gate
from wirestack.optimize import optimize
from wirestack.convert import to_qiskit


def run(c, n):
    out = optimize(c, n)
    assert Operator(to_qiskit(c, n)).equiv(Operator(to_qiskit(out, n)))
    return out


def test_gate_on_target_blocks_cx():
    c = [Gate("cx", (0, 1)), Gate("h", (1,)), Gate("cx", (0, 1))]
    assert run(c, 2) == c


def test_reversed_cx_does_not_cancel():
    c = [Gate("cx", (0, 1)), Gate("cx", (1, 0))]
    assert run(c, 2) == c


def test_repeated_s_does_not_cancel():
    c = [Gate("s", (0,)), Gate("s", (0,))]
    assert run(c, 1) == c


def test_unrelated_wire_does_not_block():
    c = [Gate("cx", (0, 2)), Gate("h", (1,)), Gate("cx", (0, 2))]
    assert run(c, 3) == [Gate("h", (1,))]


def test_rz_merges_to_zero():
    c = [Gate("rz", (0,), (0.5,)), Gate("rz", (0,), (-0.5,))]
    assert run(c, 1) == []


def test_rz_partial_merge():
    out = run([Gate("rz", (0,), (0.2,)), Gate("rz", (0,), (0.3,))], 1)
    assert len(out) == 1 and math.isclose(out[0].params[0], 0.5)


def test_cascade():
    c = [Gate("h",(0,)), Gate("cx",(0,1)), Gate("s",(2,)), Gate("s",(2,)),
         Gate("x",(1,)), Gate("cx",(1,0)), Gate("cx",(1,0)), Gate("x",(1,)),
         Gate("rz",(2,),(0.5,)), Gate("rz",(2,),(-0.5,)), Gate("cx",(0,1)),
         Gate("h",(0,)), Gate("cx",(0,2)), Gate("h",(1,)), Gate("cx",(0,2))]
    assert run(c, 3) == [Gate("s",(2,)), Gate("s",(2,)), Gate("h",(1,))]