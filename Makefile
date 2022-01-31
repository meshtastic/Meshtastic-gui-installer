# lint the codebase
lint:
	pylint *.py

upload:
	# generate token in pypi
	rm -rf dist/
	pip install twine
	pip install build
	python -m build --sdist --wheel --outdir dist/ .
	twine upload dist/*
