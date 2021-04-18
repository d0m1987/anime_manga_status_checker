install:
	echo "Creating virtual environment"
	python3 -m venv env
	echo "Updating pip"
	./env/bin/python3 -m pip install --upgrade pip
	echo "Installing requirements.txt"
	./env/bin/python3 -m pip install -r requirements.txt

pytest_to_console:
	echo "Running pytest tests to console"
	./env/bin/python3 -m pytest tests

pytest_to_file:
	echo "Running pytest tests to file pytest.output"
	./env/bin/python3 -m pytest tests >> pytest.output
