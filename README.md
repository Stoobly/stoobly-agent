# Stoobly Agent

Record requests to Stoobly. Mock or test HTTP/HTTPS requests.

## Prerequisite

- Python >=3.8

## Installation

```
pip3 install stoobly-agent
```

## Usage

### Run with both UI and proxy

```
stoobly-agent run
```

### Run with just proxy

```
stoobly-agent run --headless
```

### See available options

```
stoobly-agent --help
```

## For Developers

### Installation

```
pip install .
```

### Test

```
pytest stoobly_agent/test
```

### Deployment

- Bump the version in `setup.py` with each PR so the CI automation will publish new artifacts with that new version.

