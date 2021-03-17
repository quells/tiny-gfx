FLASHER=tinyprog.exe
BUILD_ARTIFACT=build/top.bin
MAIN=src/gfx.py

$(BUILD_ARTIFACT): $(wildcard src/*.py)
	python3 $(MAIN)

flash: $(BUILD_ARTIFACT)
	$(FLASHER) -p $(BUILD_ARTIFACT)
