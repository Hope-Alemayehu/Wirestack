# wirestack

A single-pass peephole optimizer for quantum circuits. It cancels adjacent inverse gates and merges consecutive Rz rotations, using one stack per qubit wire to catch cascading cancellations in one sweep.

## Example

```
Input (15 gates):
H(0)  CX(0,1)  S(2)  S(2)  X(1)  CX(1,0)  CX(1,0)  X(1)
Rz(0.5)(2)  Rz(-0.5)(2)  CX(0,1)  H(0)  CX(0,2)  H(1)  CX(0,2)

Output (3 gates):
S(2)  S(2)  H(1)
```

The unitary is unchanged. Most of the reduction comes from a cascade: cancelling `CX(1,0) CX(1,0)` exposes `X(1) X(1)`, which exposes `CX(0,1) CX(0,1)`, which exposes `H(0) H(0)`.

## How it works

Each qubit wire keeps a stack of indices pointing to the surviving gates that touch it. Gates are processed in circuit order:

1. For an incoming gate on qubits `Q`, look at the top of every stack in `Q`.
2. If all tops point to the same gate, and that gate acts on the same qubits in the same order:
   - if it is the inverse of the incoming gate, delete it and pop it from every stack it was on
   - if both are `Rz`, merge the angles, and delete the gate if the result is 0 mod 2π
3. Otherwise, append the gate and push its index onto every stack in `Q`.

Popping a cancelled gate re-exposes the gate beneath it, so cascades are resolved in a single pass. The pass runs in O(n) time for a circuit with n gates.

A gate is pushed onto every wire it touches, not only its control. That way, a gate on any of those wires correctly blocks cancellation. For example, `CX(0,1) H(1) CX(0,1)` is left unchanged.

## Supported gates

| Rule | Gates |
|---|---|
| Self-inverse | `h`, `x`, `z`, `cx` |
| Inverse pair | `s` / `sdg` |
| Merge | `rz(a)` + `rz(b)` → `rz(a+b)` |

## Verification

Correctness is checked by comparing the unitary before and after optimization, up to global phase, on:

- hand-written edge cases (blocking gates, reversed CX direction, non-inverse repeats like `S S`)
- randomly generated circuits with injected redundancy

## Results

_To be filled in after benchmarking: average gate-count reduction on random circuits._

## Roadmap

- [ ] Commutation-aware cancellation (e.g. Rz through a CX control, X through a CX target)
- [ ] Port as a Qiskit `TransformationPass` on the DAG representation
- [ ] Benchmark against Qiskit's `InverseCancellation` and `Optimize1qGatesDecomposition`

## License

MIT