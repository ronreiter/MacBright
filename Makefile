venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
py2app: venv
	rm -rf build dist
	venv/bin/python setup.py py2app
	open dist
py2app-debug:
	venv/bin/python setup.py py2app -A