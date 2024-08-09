venv: .venv/touchfile

.venv/touchfile: requirements.txt
	test -d .venv || virtualenv .venv
	. .venv/bin/activate
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	touch .venv/touchfile

test: venv
	. .venv/bin/activate
	python3 -m unittest discover -s src/tests -p *_tests.py

package: venv
	. .venv/bin/activate
	python3 -m build

upload: venv
	. .venv/bin/activate
	python3 -m twine upload dist/easai-0.0.3*

publish: package upload