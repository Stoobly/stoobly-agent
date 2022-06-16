import os
import pdb

from mitmdump import DumpMaster, Options
from mitmproxy.optmanager import _Option
from typing import Union

from stoobly_agent.app.settings import Settings

from ...config.constants import mode

INTERCEPT_HANDLER_FILENAME = 'intercept_handler.py'
INTERCEPT_MODES = [mode.MOCK, mode.RECORD, mode.TEST]

'''
Pass in options from run CLI
'''
def run(**kwargs):
    options = kwargs.copy()
    __commit_options(options)
    __filter_options(options)

    fixed_options = {
        'flow_detail': 1,
        'scripts': __get_intercept_handler_path(),
        'upstream_cert': False,
    }

    opts = Options(**{**options, **fixed_options})
    __set_connection_strategy(opts, 'lazy')

    m = DumpMaster(opts)
    m.run()

def __filter_options(options):
    # Filter out non-mitmproxy options
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
    del options['test_script']

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

def __get_intercept_handler_path():
    cwd = os.path.dirname(os.path.realpath(__file__))
    script = os.path.join(cwd, INTERCEPT_HANDLER_FILENAME)
    return script

'''
 Equivalent of:
 mitmdump connection_strategy={strategy}
'''
def __set_connection_strategy(opts, strategy):
    extra_options = {
        'dumper_filter': f"connection_strategy={strategy}",
        'readfile_filter': f"connection_strategy={strategy}",
        'save_stream_filter': f"connection_strategy={strategy}",
    }
    for k, v in extra_options.items():
        opts._options[k] = _Option(k, str, v, '', None)
    opts.update(**extra_options)
