TOP = $(shell pwd)
VENV_PATH ?= venv
PROPERTIES_FILE ?= ./properties.txt
ENVIRONMENT ?= production
JUNITXML ?= ./test-pythonlib-junit.xml

export PYTHONPATH = $(TOP)
$(info PYTHONPATH = $(PYTHONPATH))

default: setupvenv

setupvenv:
	$(info ==========)
	$(info > setupenv)
	$(info ==========)
	virtualenv $(VENV_PATH)
	source $(VENV_PATH)/bin/activate ; pip install -r requirements.txt

clean:
	$(info =======)
	$(info > clean)
	$(info =======)
	rm -rf $(VENV_PATH)

test: setupvenv
	$(info ===================)
	$(info > test)
	$(info ===================)
	source $(VENV_PATH)/bin/activate ; py.test -lvvs --color=yes tests --color=yes --junitxml=$(JUNITXML)
