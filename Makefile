#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = bottle_sorting_system
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format





## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	$(PYTHON_INTERPRETER) -m venv .venv
	@echo ">>> New virtualenv created. Activate with:\n    source .venv/bin/activate"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make dataset
VAL_SIZE ?= 0.1
TEST_SIZE ?= 0.1

.PHONY: data
data:
	$(PYTHON_INTERPRETER) src/modeling/dataset.py --val_size $(VAL_SIZE) --test_size $(TEST_SIZE)


## Train dataset (use `make train MODEL=your_model.pt EPOCHS=epochs_number BATCH=batch_size` to override defaults)
MODEL ?= yolov8s.pt
EPOCHS ?= 75
BATCH ?= 4

.PHONY: train
train:
	$(PYTHON_INTERPRETER) src/modeling/training.py --model $(MODEL) --epochs $(EPOCHS) --batch $(BATCH)


## Run the bottle sorting system (make sure to have a camera connected and MODEL_PATH set correctly in src/config.py)

.PHONY: run
run:
	$(PYTHON_INTERPRETER) main.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
