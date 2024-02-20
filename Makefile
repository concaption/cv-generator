setup:
	chmod +x ./setup.sh &&\
		./setup.sh
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
test:
	python3 -m pytest -vv --cov=main test_*.py &&\
	python3 -m pytest --nbval notebook.ipynb
format:
	black *.py
lint:
	pylint --disable=R,C *.py
refactor: format lint
deploy:
	# deploy goes here
run:
	chmod +x ./main.py &&\
		./main.py
all: install lint test format deploy
