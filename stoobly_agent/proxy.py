import os

from mitmdump import DumpMaster, Options

def run(**kwargs):
    cwd = os.path.dirname(os.path.realpath(__file__))
    script = os.path.join(cwd, 'record.py')

    fixed_options = {
        'flow_detail': 1,
        'scripts': script,
    }

    opts = Options(**{**kwargs, **fixed_options})
    m = DumpMaster(opts)
    m.run()
