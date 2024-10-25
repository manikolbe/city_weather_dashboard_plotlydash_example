.PHONY: setup run clean
PROJ-NAME := $(notdir $(shell pwd))
PY-VER := 3.13.0


# install:
# 	@echo "Creating virtual environment..."
# 	pyenv virtualenv $(PY-VER) $(PROJ-NAME) || true
# 	@echo "Activating virtual environment..."
# 	pyenv activate $(PROJ-NAME)	
# 	@echo "Installing dependencies..."
# 	pip install -r requirements.txt

install:
	@echo "Creating virtual environment..."
	pyenv virtualenv $(PY-VER) $(PROJ-NAME) || true
	@echo "Installing dependencies in the virtual environment..."
	PYENV_VERSION=$(PROJ-NAME) pip install -r requirements.txt


# run:
# 	@echo "Activating virtual environment..." || true
# 	pyenv activate $(PROJ-NAME)
# 	@echo "Running code..."
# 	python$(PY-VER) run main.py

run:
	@echo "Running code..."
	PYENV_VERSION=$(PROJ-NAME) python -m streamlit run main.py


clean:
	@echo "Removing virtual environment..."
	pyenv uninstall -f $(PROJ-NAME)