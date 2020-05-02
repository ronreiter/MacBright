venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
py2app: venv
	venv/bin/python setup.py py2app
py2app-debug:
	venv/bin/python setup.py py2app -A