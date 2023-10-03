test:
	poetry run pytest stoobly_agent/test/

clean:
	rm -rf dist
	rm -rf build
	rm -rf stoobly.egg-info
