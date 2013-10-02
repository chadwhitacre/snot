dev: nose py.test
	./env/bin/pip install -e ./

clean:
	rm -rf env
	find . -name \*.pyc -delete

env/bin/pip:
	python virtualenv_support/virtualenv.py env --prompt="[snot]"

env/bin/nosetests: env/bin/pip
	./env/bin/pip install nose
nose: env/bin/nosetests

env/bin/py.test: env/bin/pip
	./env/bin/pip install pytest
py.test: env/bin/py.test
