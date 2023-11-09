.PHONY: test

test:
	python -m unittest discover pizzad/tests -p 'test_*.py'
