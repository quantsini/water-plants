SRC_DIR := ./src
BUILD_DIR := ./build
MPYC_FLAGS := 
TTY_DEVICE := /dev/cu.wchusbserial14610

SRC_LIST := $(wildcard $(SRC_DIR)/*.py)
BUILD_LIST := $(patsubst $(SRC_DIR)/%.py, $(BUILD_DIR)/%.mpy, $(SRC_LIST))

.PHONY: all upload clean

all: $(BUILD_DIR) $(BUILD_LIST)
	cp src/boot.py build/boot.py
	rm build/boot.mpy

$(BUILD_LIST): $(SRC_LIST)
	./bin/mpy-cross $< -o $@ $(MPYC_FLAGS)

$(BUILD_DIR):
	mkdir -p $@

upload: all venv
	. venv/bin/activate ; cd build ; mpy-sync --port $(TTY_DEVICE)

clean:
	rm -rf build

venv:
	virtualenv venv --python=python3
	. venv/bin/activate ; pip install -r requirements.txt
