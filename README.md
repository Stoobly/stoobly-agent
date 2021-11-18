# Stoobly Agent

Record requests to Stoobly and mock HTTP/HTTPS requests

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

## For developers

- Bump up the version in `setup.py` with each PR so the CI automation will publish new artifacts with that new version.

