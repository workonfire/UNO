init:
	pip install -r requirements.txt

mypy_test:
	mypy uno

test:
	python -m unittest discover uno/tests

dist:
	python setup.py sdist

install:
	pip install .

archlinux_dist:
	makepkg -s # Don't do it inside venv!

benchmark:
	time echo -e "computer_1\ncomputer_2\n1000\ny\n" | python -m uno --debug --cheats

benchmark_slow:
	time echo -e "computer_1\ncomputer_2\n5000\ny\n" | python -m uno --debug --cheats
