init:
	source venv/bin/activate
	pip install -r requirements.txt

mypy_test:
	mypy uno

test:
	python -m unittest discover tests

dist:
	python setup.py sdist

install:
	pip install .

archlinux_dist:
	makepkg -s