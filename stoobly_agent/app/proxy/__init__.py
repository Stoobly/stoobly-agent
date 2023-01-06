import asyncio
import os
import pdb
import signal

from mitmproxy.net import tls

from stoobly_agent.config.mitmproxy import MitmproxyConfig

# Monkey patch for OpenSSL unsafe legacy renegotiation disabled
# See: https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled
tls.DEFAULT_OPTIONS |= 0x4 

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode

CONNECTION_STRATEGIES = ['eager', 'lazy']
INTERCEPT_HANDLER_FILENAME = 'intercept_handler.py'
INTERCEPT_MODES = [mode.MOCK, mode.RECORD, mode.TEST]

def run(**kwargs):
    async def main():
        options = Options()
        master = DumpMaster(options)
        config = MitmproxyConfig.instance() 
        config.with_master(master) # Initialize mitmproxy config instance

        cli_options = kwargs.copy()
        __with_static_options(config, cli_options)
        __with_cli_options(config, cli_options)

        config.dump()

        loop = asyncio.get_running_loop()

        def _sigint(*_):
            loop.call_soon_threadsafe(getattr(master, "prompt_for_exit", master.shutdown))

        def _sigterm(*_):
            loop.call_soon_threadsafe(master.shutdown)

        # We can't use loop.add_signal_handler because that's not available on Windows' Proactorloop,
        # but signal.signal just works fine for our purposes.
        signal.signal(signal.SIGINT, _sigint)
        signal.signal(signal.SIGTERM, _sigterm)

        await master.run()

        return master

    return asyncio.run(main())

def __get_intercept_handler_path():
    cwd = os.path.dirname(os.path.realpath(__file__))
    script = os.path.join(cwd, INTERCEPT_HANDLER_FILENAME)
    return script

def __with_static_options(config: MitmproxyConfig, cli_options):
    config.set('block_global=false')
    config.set('flow_detail=1')
    config.set(f"scripts={__get_intercept_handler_path()}")
    config.set('upstream_cert=false')

def __with_cli_options(config: MitmproxyConfig, cli_options: dict):
    __commit_options(cli_options)
    __filter_options(cli_options)

    for key, val in cli_options.items():
        if isinstance(val, bool):
            config.set(f"{key}={str(val).lower()}")
        else:
            config.set(f"{key}={val}")

def __commit_options(options: dict):
    settings = Settings.instance()

    # Set intercept to not active on start
    settings.proxy.intercept.active = False

    if options.get('proxy_host') and options.get('proxy_port'):
        settings.proxy.url = f"http://{options.get('proxy_host')}:{options.get('proxy_port')}"

    if options.get('intercept_mode'):
        settings.proxy.intercept.mode = options['intercept_mode']
        settings.proxy.intercept.active = True

    settings.ui.active = not options.get('headless')

    settings.commit()

def __filter_options(options):
    ''' 
    Filter out non-mitmproxy options
    '''

    options['listen_host'] = options['proxy_host']
    options['listen_port'] = options['proxy_port']
    options['mode'] = options['proxy_mode']

    if 'api_url' in options:
        del options['api_url']

    if 'headless' in options:
        del options['headless']

    if 'ui_host' in options:
        del options['ui_host']

    if 'ui_port' in options:
        del options['ui_port']

    del options['intercept_mode']
    del options['log_level']
    del options['proxy_host']
    del options['proxy_mode']
    del options['proxy_port']