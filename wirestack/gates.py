from dataclasses import dataclass

SELF_INVERSE = {"h", "x", "z", "cx"}
INVERSE_PAIRS = {"s": "sdg", "sdg": "s"}
MERGEABLE = {"rz"}


@dataclass(frozen=True)
class Gate:
    name: str
    qubits: tuple[int, ...]
    params: tuple[float, ...] = ()

    def __repr__(self):
        q = ",".join(map(str, self.qubits))
        if self.params:
            p = ",".join(f"{x:g}" for x in self.params)
            return f"{self.name.upper()}({p})({q})"
        return f"{self.name.upper()}({q})"


def is_inverse(a: Gate, b: Gate) -> bool:
    if a.qubits != b.qubits:
        return False
    if a.name in SELF_INVERSE:
        return a.name == b.name
    return INVERSE_PAIRS.get(a.name) == b.name


def can_merge(a: Gate, b: Gate) -> bool:
    return a.qubits == b.qubits and a.name == b.name and a.name in MERGEABLE