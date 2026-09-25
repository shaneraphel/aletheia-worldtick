"""Precision checks. These fail closed when a pinned identity moves."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from audit import run as audit_run
from complete import completed_reach, measured_closure, measured_tick
from datalog import datalog_fixpoint
from decode import GO, REST, neural_class, zero_fill
from datalog_bench import N_EDGES, N_FACTS, N_NODES, SEED, world
from occgrid import occupancy_graph, occupied_points, read_occgrid, write_occgrid
from policy import policy_iteration, row0_greedy
from tick import reach_after, world_tick

ROOT = Path(__file__).resolve().parents[1]
CHAIN = [(0, 1), (1, 2)]
TRAP = [[10, 1], [-100, -100]]


class PrecisionTest(unittest.TestCase):
    def test_chain_tick_is_not_closure(self) -> None:
        self.assertEqual(world_tick(3, [0], CHAIN), 2)
        self.assertEqual(datalog_fixpoint(3, [0], CHAIN), 3)
        self.assertEqual(reach_after(3, [0], CHAIN, 3), 3)

    def test_empty_facts_refuse(self) -> None:
        with self.assertRaises(ValueError):
            datalog_fixpoint(3, [], CHAIN)
        with self.assertRaises(ValueError):
            world_tick(3, [], CHAIN)
        with self.assertRaises(ValueError):
            datalog_fixpoint(-1, [0], CHAIN)
        with self.assertRaises(ValueError):
            reach_after(3, [0], CHAIN, -1)

    def test_pinned_world_reach(self) -> None:
        facts, edges = world(N_NODES, N_FACTS, N_EDGES, SEED)
        reach = datalog_fixpoint(N_NODES, facts, edges)
        pinned = json.loads((ROOT / "results" / "DATALOG_EVIDENCE.json").read_text())
        self.assertEqual(reach, pinned["reach_first"])
        self.assertEqual(reach, pinned["reach_second"])
        self.assertEqual(reach_after(N_NODES, facts, edges, N_NODES), reach)
        self.assertLess(world_tick(N_NODES, facts, edges), reach)

    def test_policy_disagrees_and_refuses_empty(self) -> None:
        self.assertEqual(row0_greedy(TRAP), 0)
        self.assertEqual(policy_iteration(TRAP), 1)
        self.assertEqual(policy_iteration([[1, 3], [0, 2]]), 1)
        self.assertEqual(policy_iteration(TRAP), policy_iteration(TRAP))
        with self.assertRaises(ValueError):
            policy_iteration([])
        with self.assertRaises(ValueError):
            row0_greedy([[]])

    def test_occupancy_map_is_a_path(self) -> None:
        grid = read_occgrid(ROOT / "resources" / "synthetic" / "world.yaml")
        self.assertEqual(len(occupied_points(grid)), 3)
        n, edges = occupancy_graph(grid)
        self.assertEqual(world_tick(n, [0], edges), 2)
        self.assertEqual(datalog_fixpoint(n, [0], edges), 3)

    def test_completion_matches_seen_map_and_tick_is_smaller(self) -> None:
        hole = [1, None, 0]
        seen = [1, 0, 0]
        self.assertEqual(completed_reach(hole), 3)
        self.assertEqual(measured_closure(seen), 3)
        self.assertEqual(measured_tick(seen), 2)
        with self.assertRaises(ValueError):
            measured_tick(hole)
        self.assertEqual(neural_class(GO), 1)
        self.assertEqual(neural_class(REST), 0)
        self.assertEqual(neural_class(zero_fill(8)), 0)
        with self.assertRaises(ValueError):
            neural_class([])

    def test_imputation_erases_the_mask(self) -> None:
        rec = audit_run(n=200, seed=7)
        self.assertEqual(rec["filled_maps_with_mask_markers"], 0)
        self.assertEqual(
            rec["filled_maps_matching_truth"] + rec["roads_with_occluded_obstacle"],
            rec["n"],
        )

    def test_closed_loop_never_crashes(self) -> None:
        from closedloop import run as closedloop_run

        rec = closedloop_run(n=200, seed=3)
        self.assertEqual(rec["outcomes"]["crash"], 0)
        self.assertEqual(rec["outcomes"]["timeout"], 0)
        self.assertEqual(
            rec["outcomes"]["reached"] + rec["outcomes"]["correct_stop"],
            rec["n"],
        )

    def test_breakeven_is_exact(self) -> None:
        from fractions import Fraction

        from tradeoff import run as tradeoff_run

        rec = tradeoff_run()
        self.assertEqual(rec["one_step"]["breakeven_exact"], "2353/552")
        self.assertEqual(rec["full_walk"]["breakeven_exact"], "20975/2995")
        self.assertEqual(
            Fraction(rec["full_walk"]["waits"], rec["full_walk"]["crashes"]),
            Fraction(20975, 2995),
        )

    def test_blank_grid_refuses(self) -> None:
        with self.assertRaises(ValueError):
            occupied_points([[0, 0], [0, -1]])
        with self.assertRaises(ValueError):
            write_occgrid("/tmp/aletheia-blank-should-not-write", [])


if __name__ == "__main__":
    unittest.main()
