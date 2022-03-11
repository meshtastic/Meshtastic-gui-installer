# lint the codebase
lint:
	pylint *.py meshtastic_flasher/*.py meshtastic_flasher/tests/*.py bin/*.py

test:
	pytest

# Note: Might want to 'pip install .' first.
url:
	bin/url_check.py

# run the coverage report and open results in a browser
cov:
	pytest --cov-report html --cov=meshtastic_flasher

# show the slowest unit tests
slow:
	pytest --durations=5

open:
	# on mac, this will open the coverage report in a browser
	open htmlcov/index.html

upload:
	# generate token in pypi
	rm -rf dist/
	pip install twine
	pip install build
	python -m build --sdist --wheel --outdir dist/ .
	twine upload dist/*
