# lint the codebase
lint:
	pylint *.py meshtastic_flasher/*.py

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
	pyinstaller -F -n meshtastic-flasher-mac --add-binary "meshtastic_flasher/logo.png:." --add-binary "meshtastic_flasher/meshtastic_theme.xml:." --collect-all meshtastic --collect-all esptool meshtastic_flasher/installer.py
