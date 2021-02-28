clean:
	rm -rf coverage/
	rm -rf logs/*
	rm -rf .pytest_cache
	coverage erase

install:
	/usr/bin/python3.8 -m pip install --upgrade -r requirements.txt

lint:
	/usr/bin/python3.8 -m flake8 src/

run:
	/usr/bin/python3.8 run.py
