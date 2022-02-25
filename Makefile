# lint the codebase
lint:
	pylint *.py meshtastic_flasher/*.py meshtastic_flasher/tests/*.py

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

mac:
	# for locally testing binary on mac
	pip install pyinstaller
	pip install -r requirements.txt
	pyinstaller -F -n meshtastic-flasher-mac --add-binary "meshtastic_flasher/fields.json:." --add-binary "meshtastic_flasher/logo.png:." --add-binary "meshtastic_flasher/meshtastic_theme.xml:." --add-binary "meshtastic_flasher/help.svg:." --add-binary "meshtastic_flasher/info.svg:." --add-binary "meshtastic_flasher/options.svg:." --add-binary "meshtastic_flasher/cog.svg:." --collect-all meshtastic --collect-all esptool meshtastic_flasher/main.py
