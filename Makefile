PYTHON ?= python3.12

.PHONY: check show bench evidence paper

check:
	$(PYTHON) worldtick.py --verify-precision
	$(PYTHON) -m unittest discover -s tests -v

show:
	$(PYTHON) show_tick.py
	$(PYTHON) show_story.py
	$(PYTHON) show_policy.py
	$(PYTHON) show_networkx.py
	$(PYTHON) show_occgrid.py
	$(PYTHON) show_mcap.py
	$(PYTHON) show_rosbag2.py
	$(PYTHON) show_rosbags.py

bench:
	$(PYTHON) tick_bench.py
	$(PYTHON) datalog_bench.py
	$(PYTHON) policy_bench.py

evidence:
	$(PYTHON) campaign.py
	$(PYTHON) hidden.py
	$(PYTHON) sweep.py
	$(PYTHON) horizon.py
	$(PYTHON) foresight.py
	$(PYTHON) bcisweep.py
	$(PYTHON) decide.py
	$(PYTHON) fillchoice.py
	$(PYTHON) audit.py
	$(PYTHON) cost.py
	$(PYTHON) robust.py
	$(PYTHON) closedloop.py
	$(PYTHON) tradeoff.py
	$(PYTHON) stats.py
	$(PYTHON) grid2d.py
	$(PYTHON) plandepth.py
	$(PYTHON) selector.py
	$(PYTHON) partition.py
	$(PYTHON) signfill.py
	$(PYTHON) decisive.py
	$(PYTHON) askdepth.py
	$(PYTHON) session.py
	$(PYTHON) fleet.py
	$(PYTHON) media.py
	$(PYTHON) pace.py

paper:
	$(PYTHON) paper/check_numbers.py
