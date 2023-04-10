# https://stackoverflow.com/a/27132934
# Determine this makefile's path.
# Be sure to place this BEFORE `include` directives, if any.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

build-image:
	docker build -t ${image} .

push-image:
	docker push ${image}

deploy\:docker:
	@$(MAKE) -f $(THIS_FILE) build-image
	@$(MAKE) -f $(THIS_FILE) push-image

deploy\:pip:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

test:
	pytest stoobly_agent/test/

clean:
	rm -rf dist
	rm -rf build
	rm -rf stoobly.egg-info
