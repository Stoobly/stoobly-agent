deploy:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	docker build --no-cache -t ${image} .
	docker push ${image} 

clean:
	rm -rf dist
	rm -rf build
	rm -rf stoobly.egg-info
