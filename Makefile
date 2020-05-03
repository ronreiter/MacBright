venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
py2app: venv
	rm -rf build dist
	venv/bin/python setup.py py2app
	codesign -f -s "Apple Development" "dist/MacBright.app/" --timestamp=none --deep
	spctl -a -v dist/MacBright.app
	productbuild --component dist/MacBright.app dist/MacBright.pkg
	open dist
py2app-debug:
	venv/bin/python setup.py py2app -A
