test:
	# some asserts here

pretty:
	black test.py 

clean:
	rm -rf ./classes/__pycache__ 

check: pretty clean