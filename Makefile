mytest:
	pytest -s test.py --disable-warnings

pretty:
	black test.py ./classes/*

clean:
	rm -rf ./*/__pycache__ 
	rm -rf ./__pycache__

check: mytest clean pretty