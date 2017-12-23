run:
	python3 sim_game

check:
	echo 'import sim_game' | python3
	echo 'from sim_game import game' | python3
	python3 sim_game/ci_dummy.py
	python3 tests/test_ci_dummy.py

run-exe:
	python3.exe sim_game

.PHONY: dir_test test run
