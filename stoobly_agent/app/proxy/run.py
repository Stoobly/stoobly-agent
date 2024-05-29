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

INTERCEPT_HANDLER_FILENAME = 'intercept_handler.py'

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
    options = (
        'block_global=false',
        f"scripts={__get_intercept_handler_path()}",
        'upstream_cert=false'
    )

    config.set(options)

def __with_cli_options(config: MitmproxyConfig, cli_options: dict):
    __commit_options(cli_options)
    __filter_options(cli_options)

    options = []
    def append_option(key, val):
        if isinstance(val, bool):
            options.append(f"{key}={str(val).lower()}")
        else:
            options.append(f"{key}={val}")

    for key, val in cli_options.items():
        if isinstance(val, tuple):
            for v in val:
                append_option(key, v)
        else:
            append_option(key, val)

    config.set(tuple(options))

def __commit_options(options: dict):
    settings = Settings.instance()

    settings.proxy.intercept.active = not not options.get('intercept')

    if options.get('proxy_host') and options.get('proxy_port'):
        settings.proxy.url = f"http://{options.get('proxy_host')}:{options.get('proxy_port')}"

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

    if 'certs' in options and not options['certs']:
        del options['certs']

    if 'cert_passphrase' in options and not options['cert_passphrase']:
        del options['cert_passphrase']

    if 'headless' in options:
        del options['headless']

    if 'intercept' in options:
        del options['intercept']

    if 'lifecycle_hooks_path' in options:
        del options['lifecycle_hooks_path']

    if 'proxyless' in options:
        del options['proxyless']

    if 'public_directory_path' in options:
        del options['public_directory_path']

    if 'response_fixtures_path' in options:
        del options['response_fixtures_path']

    if 'ui_host' in options:
        del options['ui_host']

    if 'ui_port' in options:
        del options['ui_port']

    del options['log_level']
    del options['proxy_host']
    del options['proxy_mode']
    del options['proxy_port']