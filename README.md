# wirestack

A single-pass peephole optimizer for quantum circuits. It cancels adjacent inverse gates and merges consecutive Rz rotations in O(n), using one stack per qubit wire.

## Example

```text
Input (15 gates):
H(0)  CX(0,1)  S(2)  S(2)  X(1)  CX(1,0)  CX(1,0)  X(1)
Rz(0.5)(2)  Rz(-0.5)(2)  CX(0,1)  H(0)  CX(0,2)  H(1)  CX(0,2)

Output (3 gates):
S(2)  S(2)  H(1)
```

Most of the reduction is a cascade: cancelling `CX(1,0) CX(1,0)` exposes `X(1) X(1)`, then `CX(0,1) CX(0,1)`, then `H(0) H(0)`.

## Usage

```python
from wirestack.gates import Gate
from wirestack.optimize import optimize

circuit = [Gate("h", (0,)), Gate("cx", (0, 1)), Gate("cx", (0, 1)), Gate("h", (0,))]
optimize(circuit, num_qubits=2)   # []
```

Run the tests and benchmark from the repo root:

```bash
pip install qiskit pytest
python -m pytest -v
python -m benchmarks.run
```

## How it works

Each wire keeps a stack of the surviving gates that touch it. For each incoming gate, in circuit order:

1. **Check for a match.** All of its wires must have the same gate on top, acting on the same qubits in the same order.
2. **If matched, simplify.**
   - Inverse gates: delete the earlier gate and pop it from its stacks.
   - Two `Rz` gates: merge the angles, deleting the gate if the sum is 0 mod 2π.
3. **Otherwise, keep it.** Append the gate and push it onto every wire it touches.

Popping a gate re-exposes the one beneath it, which is how cascades resolve in one pass. Pushing onto every wire is what makes blocking work: `CX(0,1) H(1) CX(0,1)` is left unchanged.

### Complexity

- **Time is O(n).** Each gate does constant work per wire it touches (at most 2), and a gate can be pushed once and popped at most once. That last point is why cascades don't blow up the cost: a long cascade of pops is "paid for" by the earlier pushes, so it's amortized.
- **Space is O(n + q).** This covers the output list, the stack entries, and one stack per qubit.

## Supported gates

| Rule | Gates |
| --- | --- |
| Self-inverse | `h`, `x`, `z`, `cx` |
| Inverse pair | `s` / `sdg` |
| Merge | `rz(a)` + `rz(b)` → `rz(a+b)` |

## Verification

Tests compare unitaries before and after optimization, up to global phase, on:

- hand-written edge cases (blocking gates, reversed CX direction, non-inverse repeats like `S S`)
- 300 seeded random circuits

## Results

Average gate-count reduction on random circuits (100 trials per cell, seed 0):

| Qubits | 50 gates | 200 gates | 1000 gates |
| --- | --- | --- | --- |
| 3 | 16.0% | 16.9% | 17.3% |
| 5 | 14.9% | 15.6% | 16.2% |
| 8 | 14.2% | 15.0% | 15.7% |

Reduction falls slightly with more qubits, because two random gates are less likely to share a wire. It rises slightly with length, because longer circuits give cascades more room to form.

**Caveat:** these circuits use a small gate alphabet, which makes cancellations unusually common. The numbers are not a measure of real-world gains, which need structured benchmark circuits and a comparison against existing passes.

## Roadmap

- [ ] Commutation-aware cancellation (e.g. Rz through a CX control, X through a CX target)
- [ ] Port as a Qiskit `TransformationPass` on the DAG representation
- [ ] Benchmark against Qiskit's `InverseCancellation` and `Optimize1qGatesDecomposition`

## License

MIT
