PYTHON=python3
PIP=$(PYTHON) -m pip
SRC_DIR=api
GLOBAL_FILES=$(SRC_DIR)/request.py $(SRC_DIR)/response.py

mh-pkg mh.zip: INSTALL_ARGS = -t .mh-pkg --platform manylinux2014_x86_64 --python-version 312 --only-binary=:all: --upgrade
mh-pkg mh.zip: MODULE_FILES = $(SRC_DIR)/malmuthharville.py
mh-pkg mh.zip: INDEX_FILE = $(SRC_DIR)/mh_handler.py
mh-pkg: install
	mkdir -p .mh-pkg
	cp $(GLOBAL_FILES) $(MODULE_FILES) .mh-pkg
	cp $(INDEX_FILE) .mh-pkg/index.py

mh.zip: BUILD_ZIP = mh.zip
mh.zip: mh-pkg
	cd .mh-pkg && zip -r ../$(BUILD_ZIP) .

tsen-pkg tysen.zip: INSTALL_ARGS = -t .tysen-pkg --platform manylinux2014_x86_64 --python-version 312 --only-binary=:all: --upgrade
tysen-pkg tysen.zip: MODULE_FILES = $(SRC_DIR)/tysen.py
tysen-pkg tysen.zip: INDEX_FILE = $(SRC_DIR)/tysen_handler.py
tysen-pkg: install
	mkdir -p .tysen-pkg
	cp $(GLOBAL_FILES) $(MODULE_FILES) .tysen-pkg
	cp $(INDEX_FILE) .tysen-pkg/index.py

app/dist:
	cd app && npm run build

tysen.zip: BUILD_ZIP = tysen.zip
tysen.zip: install tysen-pkg
	cd .tysen-pkg && zip -r ../$(BUILD_ZIP) .

install: 
	$(PIP) install -r requirements.txt $(INSTALL_ARGS)

.PHONY: clean
clean:
	rm -rf .tysen-pkg tysen.zip
	rm -rf .mh-pkg mh.zip
	rm -rf app/dist