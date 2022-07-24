FLASHER=tinyprog.exe
BUILD_ARTIFACT=build/top.bin
DOCKER_BUILD_IMG=tiny-gfx

$(BUILD_ARTIFACT): $(wildcard src/*.py) $(DOCKER_BUILD_IMG)
	docker run --rm \
		-v $(shell pwd)/build:/opt/tiny-gfx/build \
		$(DOCKER_BUILD_IMG)

flash: $(BUILD_ARTIFACT)
	$(FLASHER) -p $(BUILD_ARTIFACT)

$(DOCKER_BUILD_IMG): $(wildcard src/*.py) Dockerfile
	docker build -t $(DOCKER_BUILD_IMG) .

clean:
	-rm -rf ./build
	-rm -r ./src/__pycache__
