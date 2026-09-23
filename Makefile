PYTHON ?= python3.12

.PHONY: check show bench

check:
	$(PYTHON) worldtick.py --verify-precision
	$(PYTHON) -m unittest discover -s tests -v

show:
	$(PYTHON) show_tick.py
	$(PYTHON) show_policy.py
	$(PYTHON) show_occgrid.py

bench:
	$(PYTHON) tick_bench.py
	$(PYTHON) datalog_bench.py
	$(PYTHON) policy_bench.py
