# Stoobly Agent

🌐 Stoobly is a man-in-the-middle proxy tool and REST API to **easily record, retrieve and mock stored HTTP/HTTPS requests and responses**

🚀 Create scalable API mocks with little setup time. 

⚡ **Maintaining hard-coded inputs and responses is expensive.** De-clutter your codebase and streamline updates by making schema changes and replaying requests to get the latest changes.

💡 Stoobly works by recording requests and and their corresponding responses. The next time the request is sent to our agent proxy, **we compare the current response to the recorded response.**

🔨 Need deep customization? Use **advanced features** like grouping requests into scenarios, rewriting requests, excluding requests using your own tailored matching rules, and test lifecycle hooks.

See our docs for more detailed information! https://docs.stoobly.com

## Prerequisite

- Python >= 3.8, < 3.11

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
