clean: pyc cache

pyc:
	rm -f *.pyc src/*.pyc test/*.pyc imp-interpreter/*.pyc

cache:
	rm -rf src/__pycache__ imp-interpreter/__pycache__
