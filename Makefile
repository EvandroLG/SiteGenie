.PYTHON: all install lint run test

all: install lint run test

install:
	pip install -r requirements.txt

lint:
	flake8 src

run:
	python3 src/main.py
	cd public && python3 -m http.server 9999

test:
	python3 -m unittest discover -s src 
