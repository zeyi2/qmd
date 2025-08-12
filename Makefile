PHASE ?= test_phase
PYTHON := python3

GENERATOR_DIR := generator
TEMPLATE_DIR := template
BUILD_DIR := build
PHASE_BUILD_DIR := $(BUILD_DIR)/$(PHASE)
PHASE_SRC_DIR := $(PHASE_BUILD_DIR)/src
GENERATED_GO_SRC := $(PHASE_SRC_DIR)/main.go

.PHONY: all build clean

all: build

build: $(GENERATED_GO_SRC)
	@echo "--> Compiling Go binaries for phase: $(PHASE)..."
	@GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o $(PHASE_BUILD_DIR)/quiz_linux_amd64 $(GENERATED_GO_SRC)
	@GOOS=linux GOARCH=arm64 go build -ldflags="-s -w" -o $(PHASE_BUILD_DIR)/quiz_linux_arm64 $(GENERATED_GO_SRC)
	@echo "--> Build complete. Binaries are in $(PHASE_BUILD_DIR)/"

$(GENERATED_GO_SRC): $(PHASE)/questions.qmd $(PHASE)/answers.txt $(GENERATOR_DIR)/generator.py $(TEMPLATE_DIR)/main.go.template
	@echo "--> Generating Go source code for phase: $(PHASE)..."
	@mkdir -p $(PHASE_SRC_DIR)
	@$(PYTHON) $(GENERATOR_DIR)/generator.py \
		--qmd $(PHASE)/questions.qmd \
		--answers $(PHASE)/answers.txt \
		--template $(TEMPLATE_DIR)/main.go.template \
		--output $(GENERATED_GO_SRC) \
		--phase $(PHASE)

clean:
	@echo "--> Cleaning up build directory..."
	@rm -rf $(BUILD_DIR)
	@echo "--> Done."
