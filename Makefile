dir_test:
	# Some stupid "sanity check" tests to make sure that running
	# and importing from "anywhere" works
	echo 'import src' | python3
	echo 'from src import game' | python3
	cd src && python3 -c 'import game'
	cd src && python3 -c 'from game import Game'
	python3 src/ci_dummy.py
	python3 tests/test_ci_dummy.py

test: dir_test
	py.test

run:
	python3 src/main.py

run-exe:
	python3.exe src/main.py

.PHONY: dir_test test run
