run:
	python3 src/main.py
	cd public && python3 -m http.server 9999

test:
	python3 -m unittest discover -s src 
