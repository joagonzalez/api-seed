clean:
	rm -rf coverage/
	rm -rf logs/*
	rm -rf .pytest_cache
	coverage erase

install:
	python -m pip install --upgrade -r requirements.txt

lint:
	python -m flake8 src/

run:
	python run.py

test:
	echo "Implementar tests!"
	# python -m pytest --cov=src ./ -vv

build: 
	docker build -t api-seed .

prod:
	docker run -it --net=host -p 5000:5000 api-seed