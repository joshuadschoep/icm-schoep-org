PYTHON=python3
PIP=$(PYTHON) -m pip
SRC_DIR=api
GLOBAL_FILES=$(SRC_DIR)/request.py $(SRC_DIR)/response.py $(SRC_DIR)/malmuthharville.py $(SRC_DIR)/tysen.py
INDEX_FILE=$(SRC_DIR)/handler.py
BUILD_ZIP = handler.zip

pkg handler.zip: INSTALL_ARGS = -t pkg --platform manylinux2014_x86_64 --python-version 312 --only-binary=:all: --upgrade
pkg: install
	mkdir -p pkg
	cp $(GLOBAL_FILES) pkg
	cp $(INDEX_FILE) pkg/index.py

handler.zip: pkg
	cd pkg && zip -r ../$(BUILD_ZIP) .

.PHONY: app
app:
	cd app && npm run build

install: 
	$(PIP) install -r requirements.txt $(INSTALL_ARGS)

.PHONY: clean
clean:
	rm -rf pkg handler.zip
	rm -rf app/dist