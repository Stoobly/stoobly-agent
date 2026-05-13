TEST_CONTAINER_NAME = stoobly.test
TEST_DIR = /root/stoobly-agent

cert:
	HOSTNAME=$(hostname) HOSTNAME="$${HOSTNAME:-$(DEFAULT_HOSTNAME)}" && \
	mkdir -p $(CERTS_DIR) && cd $(CERTS_DIR); \
	mkcert --install && \
	mkcert $$HOSTNAME && \
	mkcert -pkcs12 $$HOSTNAME && \
	cat $$HOSTNAME.pem >> $$HOSTNAME-joined.pem && \
	cat $$HOSTNAME-key.pem >> $$HOSTNAME-joined.pem && \
	cp $$HOSTNAME.pem $$HOSTNAME.crt && \
	cp $$HOSTNAME-key.pem $$HOSTNAME.key

clean:
	rm -rf dist
	rm -rf build
	rm -rf stoobly.egg-info

test:
	poetry install --with test
	poetry run pytest --maxfail=1 -m "not e2e" stoobly_agent/test/

test/build:
	docker rm -f ${TEST_CONTAINER_NAME}
	docker run -itd --name ${TEST_CONTAINER_NAME} python:$(version) /bin/bash
	docker cp $$(pwd) stoobly.test:${TEST_DIR}

test/e2e:
	poetry install --with test
	STOOBLY_IMAGE_USE_LOCAL=1 poetry run pytest --verbose --capture=no -m e2e stoobly_agent/test/

test/e2e/forward-proxy-docker:
	poetry install --with test
	STOOBLY_IMAGE_USE_LOCAL=1 poetry run pytest --verbose --capture=no -m e2e \
		stoobly_agent/test/app/cli/scaffold/docker/request_log_forward_proxy_test.py

test/e2e/reverse-proxy-docker:
	poetry install --with test
	STOOBLY_IMAGE_USE_LOCAL=1 poetry run pytest --verbose --capture=no -m e2e \
		stoobly_agent/test/app/cli/scaffold/docker/request_log_reverse_proxy_test.py

test/e2e/multi-namespace:
	poetry install --with test
	STOOBLY_IMAGE_USE_LOCAL=1 poetry run pytest --verbose --capture=no -m e2e \
		stoobly_agent/test/app/cli/scaffold/docker/request_log_multi_namespace_test.py

test/e2e/local:
	poetry install --with test
	poetry run pytest --verbose --capture=no -m e2e \
		stoobly_agent/test/app/cli/scaffold/local/

test/e2e/workflow-cli:
	poetry install --with test
	STOOBLY_IMAGE_USE_LOCAL=1 poetry run pytest --verbose --capture=no -m e2e \
		stoobly_agent/test/app/cli/scaffold/docker/workflow_test.py \
		stoobly_agent/test/app/cli/scaffold/docker/cli_test.py

test/e2e-parallel:
	poetry install --with test
	EXIT=0; \
	$(MAKE) test/e2e/forward-proxy-docker & PID1=$$!; \
	$(MAKE) test/e2e/reverse-proxy-docker & PID2=$$!; \
	$(MAKE) test/e2e/multi-namespace      & PID3=$$!; \
	$(MAKE) test/e2e/local               & PID4=$$!; \
	$(MAKE) test/e2e/workflow-cli        & PID5=$$!; \
	wait $$PID1 || EXIT=1; \
	wait $$PID2 || EXIT=1; \
	wait $$PID3 || EXIT=1; \
	wait $$PID4 || EXIT=1; \
	wait $$PID5 || EXIT=1; \
	exit $$EXIT

test/python: test/build
	docker exec -it ${TEST_CONTAINER_NAME} sh -c "cd ${TEST_DIR} && pip3 install poetry && poetry install && make test"

test/run: test/build
	docker exec -it ${TEST_CONTAINER_NAME} sh -c "cd ${TEST_DIR} && pip install . && stoobly-agent run"
