.PHONY: test tests/*

test: tests/

tests/%:
	python -m unittest discover pizzad/$@ -p 'test_*.py'
