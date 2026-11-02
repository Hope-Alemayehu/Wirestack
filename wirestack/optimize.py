import math
from .gates import Gate, is_inverse, can_merge


def optimize(circuit: list[Gate], num_qubits: int) -> list[Gate]:
    out: list[Gate | None] = []
    stacks: list[list[int]] = [[] for _ in range(num_qubits)]

    for g in circuit:
        tops = {stacks[q][-1] if stacks[q] else None for q in g.qubits}
        j = tops.pop() if len(tops) == 1 else None

        if j is not None:
            prev = out[j]
            if is_inverse(prev, g):
                _remove(j, out, stacks)
                continue
            if can_merge(prev, g):
                angle = (prev.params[0] + g.params[0]) % (2 * math.pi)
                if math.isclose(angle, 0, abs_tol=1e-9) or math.isclose(angle, 2 * math.pi, abs_tol=1e-9):
                    _remove(j, out, stacks)
                else:
                    out[j] = Gate(prev.name, prev.qubits, (angle,))
                continue

        out.append(g)
        for q in g.qubits:
            stacks[q].append(len(out) - 1)

    return [g for g in out if g is not None]


def _remove(j: int, out: list, stacks: list[list[int]]) -> None:
    for q in out[j].qubits:
        stacks[q].pop()
    out[j] = None