# lint the codebase
lint:
	pylint *.py

upload:
	# generate token in pypi
	rm -rf dist/
	pip install twine
	pip install build
	python -m build --sdist --wheel --outdir dist/ .
	cp logo.png meshtastic_theme.xml dist/
	twine upload dist/*
