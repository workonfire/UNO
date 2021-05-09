init:
	pip install -r requirements.txt

test:
	mypy uno
	python -m unittest discover uno

dist:
	python setup.py sdist

install:
	pip install .

