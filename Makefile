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

test:
	echo "Implementar tests!"
	# /usr/bin/python3.8 -m pytest --cov=src ./ -vv

build: 
	docker build -t api-seed .

prod:
	docker run -it --net=host -p 5000:5000 api-seed