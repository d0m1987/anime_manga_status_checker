install:
	echo "Creating virtual environment"
	python -m venv env
	echo "Updating pip"
	./env/bin/python -m pip install --upgrade pip
	echo "Installing requirements.txt"
	./env/bin/python -m pip install -r requirements.txt