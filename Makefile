dir_test:
	# Some stupid "sanity check" tests to make sure that running
	# and importing from "anywhere" works
	echo 'import sim_game' | python3
	echo 'from sim_game import game' | python3
	cd sim_game && python3 -c 'import game'
	cd sim_game && python3 -c 'from game import Game'
	python3 sim_game/ci_dummy.py
	python3 tests/test_ci_dummy.py

test: dir_test
	py.test

run:
	python3 sim_game

run-exe:
	python3.exe sim_game

.PHONY: dir_test test run
