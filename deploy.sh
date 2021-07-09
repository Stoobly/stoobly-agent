python3 setup.py sdist bdist_wheel
twine upload dist/*

docker build --no-cache -t stoobly/agent:alpha .
docker push stoobly/agent:alpha
