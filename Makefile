SRC_DIR := ./src
BUILD_DIR := ./build
MPYC_FLAGS := 
TTY_DEVICE := /dev/cu.wchusbserial14610

SRC_LIST := $(wildcard $(SRC_DIR)/*.py)
BUILD_LIST := $(patsubst $(SRC_DIR)/%.py, $(BUILD_DIR)/%.mpy, $(SRC_LIST))

.PHONY: all upload clean

all: $(BUILD_DIR) $(BUILD_LIST)

$(BUILD_LIST): $(SRC_LIST)
	./bin/mpy-cross $< -o $@ $(MPYC_FLAGS)

$(BUILD_DIR):
	mkdir -p $@

mpy-sync: all venv
	. venv/bin/activate ; cd $(BUILD_DIR) ; mpy-sync --port $(TTY_DEVICE)

py-sync: all venv
	. venv/bin/activate ; cd $(SRC_DIR) ; mpy-sync --port $(TTY_DEVICE)

clean:
	rm -rf $(BUILD_DIR)

venv:
	virtualenv venv --python=python3
	. venv/bin/activate ; pip install -r requirements.txt
