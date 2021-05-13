run:
	python3 src/main.py

watchexec:
	watchexec --clear --exts py,yaml python3 src/main.py

test:
	python3 src/test/test_helpers.py

watch-test:
	watchexec --clear --exts py,yaml python3 src/test/test_helpers.py

install:
	python3 -m pip install -r requirements.txt

freeze:
	python3 -m pip freeze -r requirements.txt

lint:
	flake8 *.py
