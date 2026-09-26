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

    def test_wilson_intervals_bracket_estimates(self) -> None:
        from stats import run as stats_run

        rec = stats_run()["rates"]
        for key, r in rec.items():
            self.assertLess(r["lo"], r["p"])
            self.assertLess(r["p"], r["hi"])
        self.assertLess(rec["one-step collision"]["hi"] - rec["one-step collision"]["lo"], 0.02)

    def test_pessimistic_path_never_crashes_2d(self) -> None:
        from grid2d import run as grid2d_run

        rec = grid2d_run(n=50, seed=11)
        self.assertEqual(rec["pessimistic"]["crash"], 0)
        self.assertEqual(
            rec["optimistic"]["crash"] + rec["optimistic"]["stopped"] + rec["optimistic"]["reached"],
            rec["n"],
        )

    def test_depth_one_matches_infinite_horizon(self) -> None:
        from plandepth import finite_action, run as plandepth_run

        self.assertEqual([finite_action([[10, 1], [-100, -100]], d) for d in range(3)], [0, 1, 1])
        rec = plandepth_run(n=50, seed=5)
        for p in rec["points"][1:]:
            self.assertEqual(p["match_infinite"], rec["n"])

    def test_nested_plans_keep_the_shorter_score_on_the_optimistic_path(self) -> None:
        from partition import audit, cell, run as partition_run

        rec = partition_run(n=40, seed=9)
        self.assertEqual(rec["inclusion_holds"], rec["n"])
        self.assertEqual(rec["visual_equals_optimistic"], rec["n"])
        self.assertEqual(rec["crash_cell_was_masked"], rec["n"])
        self.assertEqual(
            rec["cells"]["only_pessimistic"] + rec["cells"]["both"],
            rec["both_paths_exist"],
        )
        self.assertEqual(
            rec["gap_strictly_shorter"] + rec["gap_equal_length"],
            rec["cells"]["only_pessimistic"],
        )
        self.assertEqual(rec["only_optimistic_uses_a_masked_free_cell"], rec["cells"]["only_optimistic"])
        # The four labels are exhaustive on one grid as well as on the batch.
        true, seen = __import__("grid2d").make_grid(__import__("random").Random(2))
        self.assertIn(cell(audit(true, seen)), ("both", "only_optimistic", "only_pessimistic", "neither"))
        self.assertEqual(rec["equal_length_only_optimistic"], 0)

    def test_zero_fill_direction_follows_the_erased_sign(self) -> None:
        from decode import neural_class
        from signfill import flips

        false_rest, false_go = flips([1, 1, 1, 1, 1, 1, 1, 1], 3)
        self.assertEqual((false_rest, false_go), (0, 0))
        hidden = [1, 0, 0, 0, 0, 0, 0, -2]
        self.assertEqual(neural_class(hidden), 0)
        self.assertEqual(flips(hidden, 1), (0, 1))

    def test_one_question_does_not_cover_the_crashes(self) -> None:
        from decisive import run as decisive_run

        rec = decisive_run(n=40, seed=4)
        after = rec["after_one_question"]
        self.assertEqual(rec["asked_cell_was_masked"], rec["crashes"])
        self.assertEqual(sum(after.values()), rec["crashes"])

    def test_asking_until_clear_terminates(self) -> None:
        from askdepth import ask_until_clear
        from grid2d import make_grid
        import random

        true, seen = make_grid(random.Random(4))
        asked, status = ask_until_clear(true, seen)
        self.assertIn(status, ("reached", "stopped"))
        self.assertGreaterEqual(asked, 0)
        self.assertLess(asked, 64)

    def test_a_dropped_window_holds_the_scene(self) -> None:
        from session import coach_audio, naive_audio

        hidden = [1, 0, 0, 0, 0, 0, 0, -2]
        self.assertEqual(naive_audio(hidden, 1), "movement")
        self.assertEqual(coach_audio(hidden, 1), "hold")
        self.assertEqual(coach_audio(hidden, 0), "rest")

    def test_parallel_count_matches_serial(self) -> None:
        from fleet import run as fleet_run

        rec = fleet_run(n=24, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["workers"], 2)

    def test_empty_wave_is_legal_and_empty_samples_raise(self) -> None:
        from media import wave_frames

        self.assertEqual(wave_frames([]), 0)
        self.assertEqual(wave_frames([1, 0, 2, 0, 1, 0, 3, 0]), 8)
        with self.assertRaises(ValueError):
            neural_class([])

    def test_a_dropped_window_does_not_change_the_rate(self) -> None:
        from pace import hz_of, label, naive_label

        samples = [1, 0, 0, 0, 0, 0, 0, -2]
        self.assertEqual(label(samples), "rest")
        self.assertEqual(naive_label(samples), "movement")
        self.assertEqual((hz_of("rest"), hz_of("movement")), (2, 6))

    def test_the_picture_stops_at_the_camera(self) -> None:
        from room import run as room_run
        from room import split_path

        admitted, tail = split_path([(0, 0), (1, 0), (2, 0)], [[0, 1, 0]], [[0, None, 0]])
        self.assertEqual(admitted, [(0, 0)])
        self.assertEqual(tail[0], (1, 0))
        rec = room_run(n=16, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["serial"]["admitted_hits"], 0)

    def test_an_attempt_does_not_enter_an_unseen_cell(self) -> None:
        from attempt import classify
        from grid2d import H, W

        true = [[0] * W for _ in range(H)]
        seen = [[0] * W for _ in range(H)]
        true[0][1] = 1
        seen[0][1] = None
        samples = [1, 0, 2, 0, 1, 0, 3, 0]
        self.assertEqual(classify(true, seen, samples, False), "attempt_unseen")
        self.assertEqual(classify(true, seen, samples, True), "hold")

    def test_a_dropped_window_stores_no_class(self) -> None:
        from ledger import run as ledger_run

        rec = ledger_run(n=12, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["serial"]["class_on_drop"], 0)
        self.assertEqual(rec["serial"]["unseen_cell"], 0)

    def test_an_unseen_person_is_not_drawn(self) -> None:
        from company import one_map

        seen = [[0] * 16 for _ in range(16)]
        true = [[0] * 16 for _ in range(16)]
        seen[4][4] = None
        row = one_map(true, seen)
        self.assertGreaterEqual(row["hidden"], 1)

    def test_a_held_frame_repaints_the_same_pixels(self) -> None:
        from framecheck import paint
        from grid2d import make_grid
        import random

        true, seen = make_grid(random.Random(1))
        self.assertEqual(paint(true, seen, False), paint(true, seen, False))

    def test_a_dropped_window_moves_neither_clock(self) -> None:
        from clock import run as clock_run

        rec = clock_run(n=8, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["serial"]["drop_frame"], 0)
        self.assertEqual(rec["serial"]["drop_rate"], 0)

    def test_filled_nearness_is_not_seen_ground(self) -> None:
        from near import distances

        origin = (0, 0)
        dist = distances(origin, lambda p: p != (1, 0))
        self.assertNotIn((1, 0), dist)
        self.assertIn((0, 1), dist)

    def test_a_missing_sample_does_not_close_the_coach(self) -> None:
        from aperture import finger_step, run as aperture_run

        last, coach, buffer = finger_step(4, None)
        self.assertEqual((last, coach, buffer), (4, False, True))
        last, coach, buffer = finger_step(None, None)
        self.assertEqual((last, coach, buffer), (None, False, True))
        last, coach, buffer = finger_step(None, 0)
        self.assertEqual((last, coach, buffer), (0, True, True))
        rec = aperture_run(n=4, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["serial"]["unjustified"], 0)
        self.assertEqual(rec["zero_alloc"], [0, 0, 0, 0, 0])

    def test_a_late_signal_matches_when_both_arrived(self) -> None:
        import random

        from late import run as late_run
        from late import step

        _, _, row = step(True, False, random.Random(1))
        self.assertFalse(row["both_arrived"] and row["both_arrived_differ"])
        rec = late_run(n=4, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["serial"]["both_arrived_differ"], 0)

    def test_tenants_do_not_move_each_other(self) -> None:
        from tenant import run as tenant_run

        rec = tenant_run(n_tenants=3, n_requests=12, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["isolated"], 3)
        self.assertEqual(rec["noisy_unchanged"], 3)
        s = rec["serial"]
        self.assertEqual(s["held_requests"] + s["full_updates"], s["requests"])

    def test_the_picture_knows_how_old_it_is(self) -> None:
        from stale import run as stale_run

        rec = stale_run(n=6, workers=2)
        self.assertTrue(rec["equal"])
        s = rec["serial"]
        self.assertEqual(s["burst_frozen"], 3 * s["sessions"])
        self.assertGreaterEqual(s["age_max"], 3)
        self.assertLessEqual(s["new_frames"], s["sessions"] * 16 - 3 * s["sessions"])

    def test_sound_can_change_while_the_picture_stays(self) -> None:
        from reel import run as reel_run

        rec = reel_run(n=6, workers=2)
        self.assertTrue(rec["equal"])
        self.assertEqual(rec["serial"]["drop_pixel"], 0)

    def test_visual_selector_trails_the_oracle(self) -> None:
        from selector import choose
        from grid2d import make_grid
        import random

        rng = random.Random(1)
        true, seen = make_grid(rng)
        picked = choose(true, seen)
        self.assertIn(picked["visual"], ("reached", "crash", "stopped"))
        self.assertIn(picked["oracle"], ("reached", "crash", "stopped"))

    def test_blank_grid_refuses(self) -> None:
        with self.assertRaises(ValueError):
            occupied_points([[0, 0], [0, -1]])
        with self.assertRaises(ValueError):
            write_occgrid("/tmp/aletheia-blank-should-not-write", [])


if __name__ == "__main__":
    unittest.main()
