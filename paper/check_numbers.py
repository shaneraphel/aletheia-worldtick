#!/usr/bin/env python3.12
"""Every number cited in paper.md, checked against results/*.json.

Usage: python3.12 paper/check_numbers.py
Exits nonzero on the first mismatch.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
PAPER = ROOT / "paper" / "paper.md"


def load(name: str) -> dict:
    return json.loads((RES / name).read_text())


_checks = 0


def check(cond: bool, label: str) -> None:
    global _checks
    _checks += 1
    if not cond:
        raise SystemExit(f"number check failed: {label}")
    print(f"ok: {label}")


def main() -> int:
    text = PAPER.read_text()
    story = json.loads((RES / "STORY.json").read_text())
    campaign = load("CAMPAIGN.json")
    hidden = load("HIDDEN.json")
    decide = load("DECIDE.json")
    fill = load("FILLCHOICE.json")
    sweep = {p["drop"]: p["completion_hits"] for p in load("SWEEP.json")["points"]}
    sweep_tick = {p["drop"]: p["tick_hits"] for p in load("SWEEP.json")["points"]}
    horizon = {p["horizon"]: p["reach"] for p in load("HORIZON.json")["points"]}
    fore = load("FORESIGHT.json")
    bci = {p["dropped"]: p["read_as_rest"] for p in load("BCISWEEP.json")["points"]}
    audit = load("AUDIT.json")
    robust = load("ROBUST.json")
    closed = load("CLOSEDLOOP.json")

    check(story["world_model"]["completed_reach"] == 3, "story completed reach 3")
    check(story["world_model"]["seen_tick"] == 2, "story measured tick 2")
    check(story["bci"]["go"] == 1 and story["bci"]["zerofill"] == 0, "story go 1, zerofill 0")
    check(story["action"] == {"row": 0, "tick": 1}, "story action 0 vs 1")
    check(campaign["world_model"] == {"completed_equals_8": 10000, "tick_equals_2": 10000, "hole_raised": 10000}, "campaign world 10k")
    check(campaign["action"]["differ"] == 10000, "campaign actions differ 10k")
    check((hidden["roads_with_a_hidden_obstacle"], hidden["completion_enters_hidden_obstacle"], hidden["tick_enters_hidden_obstacle"]) == (8564, 2995, 0), "hidden 8564/2995/0")
    check((decide["completion_crashes"], decide["tick_crashes"], decide["tick_extra_stops"], decide["completion_extra_stops"]) == (552, 0, 2353, 0), "decide 552/0/2353/0")
    check((fill["optimistic"]["crash"], fill["optimistic"]["stop"], fill["optimistic"]["reached"]) == (2995, 6993, 12), "optimistic 2995/6993/12")
    check((fill["pessimistic"]["crash"], fill["pessimistic"]["stop"], fill["pessimistic"]["reached"]) == (0, 10000, 0), "pessimistic 0/10000/0")
    check([sweep[d] for d in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5)] == [0, 503, 934, 2002, 2914, 3970, 5084], "sweep curve")
    check(all(v == 0 for v in sweep_tick.values()), "sweep tick always 0")
    check([horizon[h] for h in (0, 1, 2, 3, 4, 6, 8, 12)] == [8, 24, 50, 92, 138, 205, 212, 214], "horizon curve")
    check(fore["first_flip_discount"] == 0.10 and abs(fore["threshold_value"] - 9 / 101) < 1e-12, "foresight 9/101 flips at 0.10")
    check(fore["random_flips"] == 1000, "foresight 1000 random flips")
    check([bci[k] for k in range(9)] == [0, 0, 1, 9, 43, 161, 642, 2494, 10000], "bci dose-response")
    check((audit["roads_with_masked_cells"], audit["filled_maps_with_mask_markers"], audit["filled_maps_matching_truth"], audit["roads_with_occluded_obstacle"]) == (10000, 0, 1436, 8564), "audit 10000/0/1436/8564")
    check([r["sweep_completion_hits"] for r in robust["rows"]] == [605, 641, 580, 606, 560], "robust sweep rows")
    check([r["decide_completion_crashes"] for r in robust["rows"]] == [120, 143, 127, 126, 105], "robust decide rows")
    check(all(r["sweep_tick_hits"] == 0 and r["decide_tick_crashes"] == 0 for r in robust["rows"]), "robust tick zeros")
    check((closed["outcomes"]["crash"], closed["outcomes"]["reached"], closed["outcomes"]["correct_stop"]) == (0, 9, 9991), "closed loop 0/9/9991")
    check(closed["waits_total"] == 20975, "closed-loop waits 20975")
    trade = load("TRADEOFF.json")
    check(trade["one_step"]["breakeven_exact"] == "2353/552", "breakeven one step 2353/552")
    check(trade["full_walk"]["breakeven_exact"] == "20975/2995", "breakeven full walk 20975/2995")
    stats = load("STATS.json")["rates"]
    check((round(stats["one-step collision"]["lo"], 4), round(stats["one-step collision"]["hi"], 4)) == (0.0509, 0.0598), "wilson collision interval")
    check((round(stats["occluded road"]["lo"], 4), round(stats["occluded road"]["hi"], 4)) == (0.8494, 0.8631), "wilson occluded interval")
    grid = load("GRID2D.json")
    check((grid["optimistic"]["crash"], grid["optimistic"]["reached"], grid["optimistic"]["stopped"]) == (1439, 500, 61), "grid optimistic 1439/500/61")
    check((grid["pessimistic"]["crash"], grid["pessimistic"]["reached"], grid["pessimistic"]["stopped"]) == (0, 419, 1581), "grid pessimistic 0/419/1581")
    plan = load("PLANDEPTH.json")
    check([c["action"] for c in plan["trap_curve"]] == [0, 1, 1, 1, 1, 1], "trap depth curve 0-1-1-1-1-1")
    check(all(p["flipped_vs_myopic"] == 1000 and p["match_infinite"] == 1000 for p in plan["points"][1:]), "depth 1 matches infinite everywhere")
    sel = load("SELECTOR.json")
    check((sel["visual"]["reached"], sel["visual"]["crash"], sel["oracle"]["reached"], sel["gap_reached"]) == (500, 1439, 797, 297), "selector 500/1439/797/297")
    part = load("PARTITION.json")
    check((part["cells"]["both"], part["cells"]["only_optimistic"], part["cells"]["only_pessimistic"], part["cells"]["neither"]) == (122, 378, 297, 1203), "partition 122/378/297/1203")
    check((part["gap_strictly_shorter"], part["gap_equal_length"], part["inclusion_holds"], part["visual_equals_optimistic"]) == (129, 168, 2000, 2000), "gap 129 strict + 168 ties")
    check(part["equal_length_only_optimistic"] == 0 and part["strict_both_reach"] == 56, "tie flip loses no optimistic-only goal")
    sign = load("SIGNFILL.json")
    check([p["false_go"] for p in sign["nonnegative"]] == [0] * 9, "nonnegative false go is identically 0")
    check((sign["signed"][4]["false_rest"], sign["signed"][4]["false_go"]) == (1280, 1141), "signed drop-4 1280 rest / 1141 go")
    one = load("DECISIVE.json")
    check((one["crashes"], one["asked_cell_was_masked"]) == (1439, 1439), "first crash cell was masked")
    check((one["after_one_question"]["reached"], one["after_one_question"]["crash"], one["after_one_question"]["stopped"]) == (614, 786, 39), "one question 614/786/39")
    depth = load("ASKDEPTH.json")
    check(depth["questions_total"] == 2814 and depth["trials_needing_more_than_one_question"] == 786, "question depth 2814 / 786")
    check(depth["histogram"]["9"] == 1 and depth["ends"]["reached"] == 1854, "one grid needs 9 questions")
    sess = load("SESSION.json")
    check(sess["audio_retunes_from_zerofill"] == 2421 and sess["audio_holds"] == 10000, "session holds every dropped window")
    check(sess["picture"]["rendered_crash"] == 1439 and sess["picture"]["coach_crash"] == 0, "coach draws no completed crash")
    fleet = load("FLEET.json")
    check(fleet["equal"] and fleet["serial_crashes"] == 1439 and fleet["parallel_crashes"] == 1439, "fleet matches on 10 cores")
    media = load("MEDIA.json")
    check(media["wave_empty_frames"] == 0 and media["wave_tone_frames"] == 8 and media["tone_class"] == 1, "wave 0 frames, tone 8")
    check(media["libraries"]["open3d"]["empty_points"] == 0 and media["libraries"]["pillow"]["empty_size"] == [0, 0], "empty cloud and empty image")
    pace = load("PACE.json")
    check((pace["dropped"], pace["naive_disagrees_while_dropped"], pace["hold_changes_while_dropped"], pace["allowed_changes"]) == (3057, 712, 0, 3379), "pace 3057 dropped, 712 would retune, 0 holds move")
    room = load("ROOM.json")
    s = room["serial"]
    check(room["equal"] and (s["admitted"], s["tail"], s["tail_hits"], s["admitted_hits"], s["drew_past_camera"]) == (6657, 53456, 2474, 0, 1938), "picture stops: 6657 seen, 2474 obstacles undrawn")
    att = load("ATTEMPT.json")["serial"]
    check((att["hold"], att["attempt_unseen"], att["attempt_seen"], att["rest"]) == (572, 630, 22, 776), "attempt heard, cell unseen: 630")
    led = load("LEDGER.json")["serial"]
    check(led["class_on_drop"] == 0 and led["unseen_cell"] == 0 and led["classes_stored"] == 1428 and led["refused_steps"] == 630, "ledger stores 1428 classes and no drop class")
    comp = load("COMPANY.json")["serial"]
    check((comp["hidden"], comp["shown"], comp["filled_through_hidden"], comp["drawn_through"]) == (997, 3003, 19, 2), "unseen people 997, filled path through them 19")
    frame = load("FRAME.json")["serial"]
    check(frame["held_repaint"] == 0 and frame["differ"] == 2000 and frame["invented_cells"] == 127697, "held frame stable, fill colors 127697 unseen cells")
    clk = load("CLOCK.json")["serial"]
    check((clk["drop_frame"], clk["drop_rate"], clk["frame_moves"], clk["rate_moves"], clk["heard_after_end"]) == (0, 0, 3665, 10933, 6414), "one clock: picture 3665, heard after end 6414")
    near = load("NEAR.json")["serial"]
    check((near["only_fill"], near["shorter"], near["both"]) == (2301, 560, 1192), "filled walk reaches 2301 people the seen walk cannot")
    reel = load("REEL.json")["serial"]
    check((reel["pixel_changes"], reel["rate_only"], reel["drop_pixel"]) == (3665, 8377, 0), "sound changes without a new frame 8377")
    ap = load("APERTURE.json")["serial"]
    check((ap["invented"], ap["seen_open_closed"], ap["absent_closed"], ap["coach_closed"], ap["unjustified"]) == (43014, 38623, 4391, 19335, 0), "missing sample drawn closed 43014")
    late = load("LATE.json")["serial"]
    check((late["differ"], late["sound_differs"], late["finger_differs"], late["both_arrived_differ"], late["one_late"]) == (58569, 21864, 42417, 0, 67130), "late signal guessed 58569")
    ten = load("TENANT.json")
    ts = ten["serial"]
    check((ts["differ"], ts["held_requests"], ts["full_updates"], ten["isolated"], ten["noisy_unchanged"]) == (2981, 4078, 3922, 16, 16), "tenants isolated 16 of 16")
    st = load("STALE.json")["serial"]
    check((st["new_frames"], st["age_sum"], st["age_max"], st["differ"], st["burst_frozen"]) == (63903, 199886, 12, 75353, 30000), "frames know their age, burst frozen 30000")
    luck = load("LUCK.json")["serial"]
    check((luck["late_steps"], luck["guess_right"], luck["held_right"]) == (81428, 21801, 48700), "luck 81428 late, guess 21801, held 48700")
    check((luck["guess_brain_only"], luck["held_brain_only"], luck["guess_finger_only"], luck["held_finger_only"], luck["guess_both"], luck["held_both"]) == (16776, 16554, 4150, 26544, 875, 5602), "luck splits show the finger gap")
    cu = load("CATCHUP.json")["serial"]
    check((cu["delay_sum"], cu["never"], cu["held_before"], cu["guess_before"], cu["resync_mismatch"]) == (19448, 87, 6022, 2693, 0), "catch-up waits sum to 19448, mismatches 0")
    check(tuple(cu[f"delay{d}"] for d in range(1, 8)) == (4938, 2531, 1230, 646, 311, 180, 77), "catch-up histogram halves each step")
    rt = load("RATE.json")["serial"]
    check((rt["new_frames"], rt["finger_age_sum"], rt["brain_missing"], rt["differ"]) == (42145, 150000, 47865, 96605), "two speeds: 42145 new, finger ages exactly 150000")
    duo = load("DUO.json")["serial"]
    check((duo["bothmove"], duo["onlyA"], duo["onlyB"], duo["still"], duo["order_mismatch"]) == (132416, 13146, 13117, 1321, 0), "two hands move independently, order changes 0")
    check((duo["a_dark_b_moves"], duo["b_dark_a_moves"]) == (duo["onlyB"], duo["onlyA"]), "dark-move identity holds")
    dose = load("DOSE.json")["serial"]
    rates = ["0.00", "0.10", "0.20", "0.30", "0.40", "0.50"]
    check(tuple(dose[f"new_{r}"] for r in rates) == (160000, 129652, 102479, 78572, 57683, 40037), "dose new frames fall with the rate")
    check(tuple(dose[f"differ_{r}"] for r in rates) == (0, 20843, 40359, 58471, 75109, 90720), "dose disagreement rises with the rate")
    worst = load("WORST.json")["serial"]
    budgets = list(range(9))
    check(tuple(worst[f"maxage_{k}"] for k in budgets) == tuple(budgets), "oldest frame equals the budget")
    check(tuple(worst[f"agesum_{k}"] for k in budgets) == (0, 10000, 30000, 60000, 100000, 150000, 210000, 280000, 360000), "age sums are triangular")
    check(tuple(worst[f"new_{k}"] for k in budgets) == tuple((16 - k) * 10000 for k in budgets), "new frames follow the schedule")
    check(tuple(worst[f"differ_{k}"] for k in budgets) == (0, 9346, 18750, 27972, 37700, 46715, 56436, 65436, 75184), "worst-case disagreement pinned")
    rp = load("REPLAY.json")["serial"]
    check((rp["replayed"], rp["mismatch"], rp["clean"]) == (160000, 0, 10000), "replay matches on all 160000 rows")
    check((rp["updates"], rp["new"], rp["differ"]) == (71442, 78861, 58450), "replay totals pinned")
    trio = load("TRIO.json")["serial"]
    check((trio["new"], trio["differ"], trio["none"]) == (55321, 85303, 4306), "three streams: 55321 new, 4306 dark")
    gpu = load("GPU.json")
    check((gpu["cpu"]["new"], gpu["cpu"]["differ"], gpu["mismatch"]) == (783232, 586904, 0), "cpu and gpu count 783232 new, mismatch 0")
    check((gpu["gpu"]["new"], gpu["gpu"]["differ"]) == (783232, 586904), "gpu totals equal cpu totals")
    sysm = load("SYSTEM.json")
    check((len(sysm["nodes"]), len(sysm["edges"])) == (6, 6), "system diagram has 6 nodes and 6 edges")
    scene = load("SCENE.json")
    check((scene["vertices"], scene["triangles"], scene["held_at"], scene["guess_at"], scene["new_steps"], scene["replay_mismatch"]) == (205, 478, 6, 16, 6, 0), "clearing hand stops at 6, guess walks to 16")
    check(scene["held_inside"] == [] and scene["guess_inside"] == ["stump_round.obj"], "guess ends inside the stump, the held hand does not")
    vis = load("VISITOR.json")["serial"]
    check((vis["held_reaches"], vis["guess_reaches"], vis["only_guess"]) == (2138, 10000, 7862), "only the guessed hand reaches the other person 7862 times")
    grip = load("GRIP.json")["serial"]
    check((grip["guess_grip"], grip["held_grip"], grip["guess_stump"], grip["held_stump"]) == (2912, 0, 2912, 0), "guessed stump grips 2912, the hand the user sees grips 0")
    near = load("APPROACH.json")["serial"]
    check((near["invented"], near["observed"], near["stay_moved_on_miss"], near["guess_moved_on_miss"]) == (34142, 27605, 0, 38725), "missing signal walks them over 34142 times, the picture you see moves them 0")
    bill = load("BILL.json")["serial"]
    check((bill["differ"], bill["same"], bill["hand"], bill["grip"], bill["person"]) == (154689, 5311, 150279, 2989, 107227), "bills differ on 154689 lines")
    beside = load("BESIDE.json")["serial"]
    check((beside["only_guess"], beside["only_held"], beside["both"], beside["apart"]) == (27971, 65303, 4712, 62014), "beside disagreement 27971/65303/4712/62014")
    check(beside["only_guess"] + beside["only_held"] == 93274, "beside pictures disagree on 93274 steps")
    check((beside["you_closed"], beside["they_pulled"], beside["guess_shrunk_on_miss"], beside["held_moved_on_miss"]) == (3691, 3657, 17000, 0), "you walk in on 3691, the guessed picture pulls them on 3657")
    relay = load("RELAY.json")["serial"]
    check((relay["only_walk"], relay["only_packet"], relay["both"], relay["neither"]) == (47175, 15006, 2825, 94994), "relay beside accounts 47175/15006/2825/94994")
    check(relay["only_walk"] + relay["only_packet"] == 62181 and relay["packet_beside"] == 17831 and relay["walk_beside"] == 5 * relay["sessions"], "relay disagrees on 62181, delivered beside 17831")
    check((relay["differ"], relay["ahead"], relay["deliveries"], relay["lag_sum"], relay["overshoot"], relay["packet_stump"]) == (153195, 27192, 112198, 32098, 0, 0), "delivered place differs on 153195 steps and is never ahead")
    once = load("ONCE.json")["serial"]
    check((once["fresh"], once["again"], once["repeat_delivery"]) == (64234, 95766, 47964), "a repeated place stays on 95766 steps")
    check(once["fresh"] + once["again"] == once["sessions"] * 16 and once["fresh"] + once["repeat_delivery"] == once["deliveries"] == relay["deliveries"], "new pictures plus repeated deliveries are the same 112198 deliveries")
    check(once["ahead"] == relay["ahead"] and once["overshoot"] == 0, "the shown place is still never ahead")
    apart = load("APART.json")["serial"]
    check((apart["differ"], apart["you_closer"], apart["them_closer"], apart["same"]) == (27143, 26761, 382, 132857), "two distances differ on 27143 steps")
    check(apart["differ"] + apart["mirror"] == apart["ahead"] == relay["ahead"] and apart["mirror"] == 49, "a lagging copy leaves the distance unchanged on 49 mirror steps")
    check(apart["you_closer"] + apart["them_closer"] == apart["differ"] and apart["overshoot"] == 0, "the two sides of a differing distance add up")
    leap = load("LEAP.json")["serial"]
    check((leap["stay"], leap["step"], leap["leap"], leap["skipped"]) == (47964, 53880, 10354, 12190), "10354 deliveries jump, skipping 12190 indices")
    check(leap["stay"] == once["repeat_delivery"] and leap["stay"] + leap["step"] + leap["leap"] == leap["deliveries"] == relay["deliveries"], "staying deliveries are the same 47964 repeated places")
    check(leap["by2"] == 8796 and leap["by3"] == 1325 and leap["maxjump"] == 8 and leap["overshoot"] == 0, "8796 leaps of two indices, 1325 of three, none ahead of the sensors")
    clasp = load("CLASP.json")["serial"]
    check((clasp["closed"], clasp["same"], clasp["behind"], clasp["walk_differs"], clasp["stump_walk"]) == (14138, 10975, 3163, 12958, 915), "a closure behind their picture on 3163 steps, a stump grip on the every-step hand 915 times")
    check(clasp["same"] + clasp["behind"] == clasp["closed"] and clasp["closed"] + clasp["open_arrived"] + clasp["no_finger"] == clasp["sessions"] * 16, "closures, open angles, and missing angles add up")
    check((clasp["behind_sum"], clasp["open_arrived"], clasp["no_finger"], clasp["stump_sensor"], clasp["stump_shown"], clasp["overshoot"]) == (3738, 97960, 47902, 0, 0, 0), "the lagging closures are 3738 index steps behind, and the stump was not where the sensors were")
    latch = load("LATCH.json")["serial"]
    check((latch["differ"], latch["you_closed"], latch["you_open"], latch["same"]) == (7739, 4180, 3559, 152261), "the two grips differ on 7739 steps")
    check(latch["you_closed"] + latch["you_open"] == latch["differ"] == latch["unsent_differ"], "every grip difference is on a step that was not delivered")
    check(latch["deliveries"] == relay["deliveries"] and latch["delivery_mismatch"] == 0 and latch["overshoot"] == 0, "the same 112198 deliveries end with the grips matching")
    blend = load("BLEND.json")["serial"]
    check((blend["wrong"], blend["agree"], blend["closed_on_open"], blend["open_on_closed"]) == (2645, 9545, 1307, 1338), "painting the jump with the final grip is wrong on 2645 skipped places")
    check(blend["wrong"] + blend["agree"] == blend["skipped"] == leap["skipped"] and blend["leaps"] == leap["leap"], "the skipped places are the same 12190")
    check(blend["closed_on_open"] + blend["open_on_closed"] == blend["wrong"] and blend["deliveries"] == relay["deliveries"] and blend["overshoot"] == 0, "the two painting errors add up, and the deliveries match")
    pose = load("POSE.json")["serial"]
    check((pose["still"], pose["grip_only"], pose["place_only"], pose["both"]) == (43522, 4442, 50877, 13357), "4442 deliveries change the grip without moving the place")
    check(pose["still"] + pose["grip_only"] == once["repeat_delivery"] and pose["place_only"] + pose["both"] == once["fresh"], "unchanged places stay 47964, and place changes stay 64234")
    check(pose["still"] + pose["grip_only"] + pose["place_only"] + pose["both"] == pose["deliveries"] == relay["deliveries"] and pose["overshoot"] == 0, "the four kinds of delivery add up")
    omit = load("OMIT.json")["serial"]
    check((omit["episodes"], omit["seen"], omit["lost"], omit["closed_lost"], omit["open_lost"]) == (32742, 29571, 3171, 2507, 664), "2507 closures never appear on their picture")
    check(omit["seen"] + omit["lost"] == omit["episodes"] and omit["closed_lost"] + omit["open_lost"] == omit["lost"], "omitted runs add up")
    check((omit["lost_steps"], omit["closed_lost_steps"], omit["deliveries"], omit["overshoot"]) == (3751, 2830, 112198, 0), "omitted closures last 2830 steps, and the deliveries match")
    whole = load("WHOLE.json")["serial"]
    check((whole["closed"], whole["saw"], whole["never"], whole["quiet"]) == (7727, 6878, 849, 2273), "6878 + 849 = 7727 sessions where the hand closed")
    check(whole["saw"] + whole["never"] == whole["closed"] and whole["closed"] + whole["quiet"] == whole["sessions"], "sessions that closed and sessions that did not add to 10000")
    phrase = load("PHRASE.json")["serial"]
    check((phrase["sent"], phrase["still"], phrase["behind"], phrase["finished_tick"], phrase["finished_sent"]) == (68676, 43522, 6468, 10000, 0), "the sent playhead finishes in none and is still in the first half in 6468 sessions")
    check(phrase["still"] == pose["still"] and phrase["sent"] == pose["grip_only"] + pose["place_only"] + pose["both"] and phrase["tick"] == 160000 and phrase["overshoot"] == 0, "the phrase advances once for each new picture, 68676 times")
    tempo = load("TEMPO.json")["serial"]
    check((tempo["shortfall"], tempo["double_finish"], tempo["double_exact"], tempo["double_past"], tempo["mode_n"]) == (91324, 3532, 1799, 1733, 2226), "doubling finishes 3532 sessions, and 1733 of them run past the end")
    check(tempo["hist"] == [0, 3, 42, 172, 630, 1353, 2042, 2226, 1799, 1046, 467, 172, 39, 8, 1, 0, 0], "the waiting playhead ends between one new picture and fourteen")
    check(tempo["shortfall"] + phrase["sent"] == phrase["tick"] and tempo["double_finish"] + phrase["behind"] == tempo["sessions"] and tempo["double_exact"] + tempo["double_past"] == tempo["double_finish"] and tempo["double_short"] == phrase["behind"] and tempo["sent"] == phrase["sent"] and tempo["finished"] == 0 and tempo["left_at_nearest"] == 2 and tempo["floor_sessions"] == 3 and tempo["overshoot"] == 0, "the shortfall is the steps that were not a new picture")

    for token in ["2,995", "8,564", "10,000", "9/101", "1,436", "2,353", "5,084", "214", "2494", "1,000", "129", "168", "1141", "1280", "786", "614", "2814", "1854", "2421", "Open3D", "3057", "712", "6657", "53456", "2474", "1938", "630", "1428", "3003", "997", "127697", "3665", "6414", "2301", "8377", "43014", "38623", "4391", "58569", "21864", "42417", "2981", "4078", "3922", "63903", "199886", "75353", "81428", "21801", "48700", "19448", "4938", "6022", "42145", "150000", "96605", "132416", "13146", "13117", "129652", "40037", "90720", "360000", "75184", "46715", "71442", "78861", "58450", "55321", "85303", "4306", "783232", "586904", "2138", "7862", "2912", "34142", "27605", "38725", "154689", "5311", "107227", "27971", "65303", "4712", "62014", "93274", "3691", "3657", "17000", "50,000", "17831", "47175", "15006", "2825", "94994", "62181", "153195", "27192", "112198", "32098", "64234", "95766", "47964", "27143", "26761", "132857", "382", "53880", "10354", "12190", "8796", "1325", "14138", "10975", "3163", "12958", "915", "3738", "97960", "47902", "7739", "4180", "3559", "152261", "2645", "9545", "1307", "1338", "43522", "4442", "50877", "13357", "32742", "29571", "3171", "2507", "664", "3751", "2830", "7727", "6878", "2273", "6878 + 849", "68676", "6468", "91324", "3532", "1799", "1733", "2226"]:
        check(token in text, f"paper cites {token}")
    print(f"all {_checks} number checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
