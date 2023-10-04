TEST_CONTAINER_NAME = stoobly.test
TEST_DIR = /root/stoobly-agent

clean:
	rm -rf dist
	rm -rf build
	rm -rf stoobly.egg-info

test:
	poetry install --only test
	poetry run pytest stoobly_agent/test/

test/build:
	docker rm -f ${TEST_CONTAINER_NAME}
	docker run -itd --name ${TEST_CONTAINER_NAME} python:$(version) /bin/bash
	docker cp $$(pwd) stoobly.test:${TEST_DIR}

test/python: test/build
	docker exec -it ${TEST_CONTAINER_NAME} sh -c "cd ${TEST_DIR} && pip3 install poetry && poetry install && make test"

test/run: test/build
	docker exec -it ${TEST_CONTAINER_NAME} sh -c "cd ${TEST_DIR} && pip install . && stoobly-agent run"
