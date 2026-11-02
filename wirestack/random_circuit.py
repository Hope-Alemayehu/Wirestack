import math
from .gates import Gate

SINGLE = ["h", "x", "z", "s", "sdg"]
ANGLES = [0.3, math.pi / 4, math.pi / 2]


def random_gate(rng, n):
    r = rng.random()
    if r < 0.2:
        a, b = rng.sample(range(n), 2)
        return Gate("cx", (a, b))
    if r < 0.4:
        return Gate("rz", (rng.randrange(n),), (rng.choice([-1, 1]) * rng.choice(ANGLES),))
    return Gate(rng.choice(SINGLE), (rng.randrange(n),))
