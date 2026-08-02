"""
generate_tests.py
------------------
Drives generators.py + solver.py to produce a complete ROAD.INP / ROAD.OUT
test suite for the "Con duong" (ROAD) problem.

Subtasks (from the statement):
  ST1: n <= 1000,    A_i <= 10^6   (30%)
  ST2: n <= 10^5,    A_i <= 1000   (30%)
  ST3: n <= 10^5,    A_i <= 10^6   (40%, full constraints)

Every test is built by a generator from generators.py, solved with the
verified O((n + factors) log maxA) BFS in solver.py (solve_fast), and
written out as a pair of files:
    tests/<subtask>/<NN>_<name>.INP
    tests/<subtask>/<NN>_<name>.OUT

A quick internal check re-validates every generated array against the
subtask's own (n, maxA) bounds before writing it out, so a bad bound in a
test plan fails loudly at generation time instead of silently producing an
invalid test.
"""

import os
import time
import generators as G
from common import make_1indexed
from solver import solve_fast

OUT_ROOT = os.path.join(os.path.dirname(__file__), "tests")

SUBTASKS = {
    "subtask1": {"n_max": 1000, "a_max": 1_000_000},
    "subtask2": {"n_max": 100_000, "a_max": 1000},
    "subtask3": {"n_max": 100_000, "a_max": 1_000_000},
}


def _unwrap(result):
    """Generators either return `A` or `(A, expected_hops)`. Normalize to A."""
    if isinstance(result, tuple):
        return result[0]
    return result


def _validate(subtask, name, A, n):
    bounds = SUBTASKS[subtask]
    assert n == len(A) - 1, f"{subtask}/{name}: len(A)-1={len(A)-1} != n={n}"
    assert 2 <= n <= bounds["n_max"], f"{subtask}/{name}: n={n} out of bounds"
    for i in range(1, n + 1):
        v = A[i]
        assert 1 <= v <= bounds["a_max"], f"{subtask}/{name}: A[{i}]={v} out of bounds"


def write_test(subtask, idx, name, A, n):
    _validate(subtask, name, A, n)
    ans = solve_fast(A, n)

    folder = os.path.join(OUT_ROOT, subtask)
    os.makedirs(folder, exist_ok=True)
    base = f"{idx:02d}_{name}"
    inp_path = os.path.join(folder, base + ".INP")
    out_path = os.path.join(folder, base + ".OUT")

    with open(inp_path, "w") as f:
        f.write(f"{n}\n")
        f.write(" ".join(str(A[i]) for i in range(1, n + 1)))
        f.write("\n")
    with open(out_path, "w") as f:
        f.write(f"{ans}\n")

    return ans


def build_subtask1():
    """n <= 1000, A_i <= 1_000_000."""
    subtask = "subtask1"
    n_max, a_max = 1000, 1_000_000
    plan = [
        ("sample", lambda: make_1indexed([2, 3, 6, 5, 15])),
        ("edge_connected", G.gen_edge_connected),
        ("edge_disconnected", G.gen_edge_disconnected),
        ("isolated_start", lambda: G.gen_edge_isolated_start(n_max, a_max, 101)),
        ("isolated_end", lambda: G.gen_edge_isolated_end(n_max, a_max, 102)),
        ("all_same_small", lambda: G.gen_all_same(50, 6)),
        ("all_same_max_n", lambda: G.gen_all_same(n_max, 999_983)),
        ("forced_chain_max", lambda: G.gen_forced_chain(n_max, a_max, 103)),
        ("greedy_trap", lambda: G.gen_greedy_trap(n_max, a_max, 104)),
        ("wall_minus_one", lambda: G.gen_wall(n_max - 1, a_max, 105)),
        ("controlled_random", lambda: G.gen_controlled_random(n_max, a_max, 106)),
        ("controlled_random_2", lambda: G.gen_controlled_random(n_max, a_max, 107)),
        ("uniform_random", lambda: G.gen_uniform_random(n_max, a_max, 108)),
        ("gcd_stress", lambda: G.gen_gcd_stress(n_max, a_max, 109)),
        ("spf_stress", lambda: G.gen_spf_stress(n_max, a_max, 110)),
        ("final_boss", lambda: G.gen_final_boss(n_max, a_max, 111)),
        ("tiny_n2_prime", lambda: make_1indexed([999983, 999979])),
    ]
    return subtask, plan


def build_subtask2():
    """n <= 100_000, A_i <= 1000."""
    subtask = "subtask2"
    n_max, a_max = 100_000, 1000
    plan = [
        ("edge_connected", G.gen_edge_connected),
        ("edge_disconnected", G.gen_edge_disconnected),
        ("isolated_start", lambda: G.gen_edge_isolated_start(n_max, a_max, 201)),
        ("isolated_end", lambda: G.gen_edge_isolated_end(n_max, a_max, 202)),
        ("all_same_max_n", lambda: G.gen_all_same(n_max, 997)),
        ("forced_chain_max", lambda: G.gen_forced_chain(n_max, a_max, 203)),
        ("greedy_trap", lambda: G.gen_greedy_trap(n_max, a_max, 204)),
        ("wall_minus_one", lambda: G.gen_wall(n_max - 1, a_max, 205)),
        ("controlled_random", lambda: G.gen_controlled_random(n_max, a_max, 206)),
        ("controlled_random_2", lambda: G.gen_controlled_random(n_max, a_max, 207)),
        ("uniform_random", lambda: G.gen_uniform_random(n_max, a_max, 208)),
        ("spf_stress", lambda: G.gen_spf_stress(n_max, a_max, 209)),
        ("final_boss", lambda: G.gen_final_boss(n_max, a_max, 210)),
        ("mid_n_forced_chain", lambda: G.gen_forced_chain(5000, a_max, 211)),
    ]
    return subtask, plan


def build_subtask3():
    """n <= 100_000, A_i <= 1_000_000 (full constraints)."""
    subtask = "subtask3"
    n_max, a_max = 100_000, 1_000_000
    plan = [
        ("edge_connected", G.gen_edge_connected),
        ("edge_disconnected", G.gen_edge_disconnected),
        ("isolated_start", lambda: G.gen_edge_isolated_start(n_max, a_max, 301)),
        ("isolated_end", lambda: G.gen_edge_isolated_end(n_max, a_max, 302)),
        ("all_same_max_n", lambda: G.gen_all_same(n_max, 999_983)),
        ("forced_chain_max", lambda: G.gen_forced_chain(n_max, a_max, 303)),
        ("greedy_trap", lambda: G.gen_greedy_trap(n_max, a_max, 304)),
        ("wall_minus_one", lambda: G.gen_wall(n_max - 1, a_max, 305)),
        ("controlled_random", lambda: G.gen_controlled_random(n_max, a_max, 306)),
        ("controlled_random_2", lambda: G.gen_controlled_random(n_max, a_max, 307)),
        ("uniform_random", lambda: G.gen_uniform_random(n_max, a_max, 308)),
        ("gcd_stress", lambda: G.gen_gcd_stress(n_max, a_max, 309)),
        ("spf_stress", lambda: G.gen_spf_stress(n_max, a_max, 310)),
        ("final_boss", lambda: G.gen_final_boss(n_max, a_max, 311)),
        ("final_boss_2", lambda: G.gen_final_boss(n_max, a_max, 312)),
    ]
    return subtask, plan


def main():
    total = 0
    t_start = time.time()
    for build in (build_subtask1, build_subtask2, build_subtask3):
        subtask, plan = build()
        print(f"\n== {subtask} ==")
        for idx, (name, gen_fn) in enumerate(plan, start=1):
            t0 = time.time()
            result = gen_fn()
            A = _unwrap(result)
            n = len(A) - 1
            ans = write_test(subtask, idx, name, A, n)
            dt = time.time() - t0
            print(f"  {idx:02d}_{name:24s} n={n:6d}  answer={ans!s:6s} ({dt:.3f}s)")
            total += 1
    print(f"\nWrote {total} tests in {time.time() - t_start:.2f}s -> {OUT_ROOT}")


if __name__ == "__main__":
    main()