venv: .venv/touchfile

.venv/touchfile: requirements.txt
	test -d .venv || virtualenv .venv
	. .venv/bin/activate
	.venv/bin/python -m pip install --upgrade pip
	pip install -r requirements.txt
	touch .venv/touchfile

test: venv
	. .venv/bin/activate
	.venv/bin/python -m unittest discover -s easai_tests -p *_unittests.py

test-all: venv
	. .venv/bin/activate
	.venv/bin/python -m unittest discover -s easai_tests -p *tests.py

build: venv
	. .venv/bin/activate
	.venv/bin/python -m build

package: test-all build

upload: venv
	. .venv/bin/activate
	.venv/bin/python -m twine upload dist/easai-0.0.9*.*

publish: package upload