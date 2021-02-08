install:
	echo "Creating virtual environment"
	python -m venv env
	echo "Updating pip"
	./env/bin/python -m pip install --upgrade pip
	echo "Installing requirements.txt"
	./env/bin/python -m pip install -r requirements.txt

pytest_to_console:
	echo "Running pytest tests to console"
	./env/bin/python -m pytest tests

pytest_to_file:
	echo "Running pytest tests to file pytest.output"
	./env/bin/python -m pytest tests >> pytest.output