# Stoobly Agent

[![Release Version](https://img.shields.io/github/v/release/Stoobly/stoobly-agent)](https://github.com/Stoobly/stoobly-agent/releases/latest)
![PyPI](https://img.shields.io/pypi/v/stoobly-agent?color=green)

[![CI](https://github.com/Stoobly/stoobly-agent/actions/workflows/tests.yaml/badge.svg)](https://github.com/Stoobly/stoobly-agent/actions/workflows/tests.yaml)
[![CodeQL](https://github.com/Stoobly/stoobly-agent/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/Stoobly/stoobly-agent/actions/workflows/github-code-scanning/codeql)


🌐 Stoobly is a feature-rich man-in-the-middle proxy tool to **record and mock HTTP/HTTPS requests and responses.**

🚀 Easily create scalable API mocks with little setup time. 

⚡ Maintaining hard-coded inputs and responses is expensive. De-clutter your codebase and **streamline maintenance with replay and record.**

💡 Upon request interception, mocking is configurable to match against all request components.

🔨 Need advanced configuration? Take advantage of features like scenarios, filters, rewriting, match rules, and lifecycle hooks.

See our docs for more detailed information! https://docs.stoobly.com

## Prerequisite

- Python 3.10, 3.11, 3.12

## Installation

To install [see our guides here](https://docs.stoobly.com/getting-started/install-and-run)

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

## Next steps

Configure the proxy settings by [following this guide](https://docs.stoobly.com/getting-started/proxy-configuration)

Start easily recording requests [with this guide](https://docs.stoobly.com/getting-started/record-requests)

Then, try mocking your requests [with this guide!](https://docs.stoobly.com/guides/mocking-apis)


## Having trouble?

File a new [Github issue here](https://github.com/Stoobly/stoobly-agent/issues) and we'll take a look
