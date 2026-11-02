import random
import sys
from wirestack.optimize import optimize
from wirestack.random_circuit import random_gate

# The bars and rules need UTF-8 even when output is piped on Windows.
sys.stdout.reconfigure(encoding="utf-8")

rng = random.Random(0)
TRIALS = 100
RULE = "─" * 62

print(f"\nwirestack benchmark: random circuits, {TRIALS} trials per row\n")
print(f"{'Qubits':>6}  {'Gates in':>8}  {'Avg out':>8}  {'Reduction':>9}  (█ = 1%)")
print(RULE)
for n in (3, 5, 8):
    for i, size in enumerate((50, 200, 1000)):
        before = after = 0
        for _ in range(TRIALS):
            c = [random_gate(rng, n) for _ in range(size)]
            before += len(c)
            after += len(optimize(c, n))
        reduction = 100 * (1 - after / before)
        label = n if i == 0 else ""
        bar = "█" * round(reduction)
        print(f"{label:>6}  {size:>8}  {after / TRIALS:>8.1f}  {reduction:>8.1f}%  {bar}")
    print(RULE)
