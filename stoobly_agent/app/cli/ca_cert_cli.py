import click
import pdb
import sys

from stoobly_agent.config.data_dir import DataDir

from .helpers.certificate_authority import CertificateAuthority

@click.group(
    epilog="Run 'stoobly-agent COMMAND --help' for more information on a command.",
    help="Manage CA certificate"
)
@click.pass_context
def ca_cert(ctx):
    pass

@ca_cert.command()
@click.option('--ca-certs-dir-path', default=DataDir.instance().mitmproxy_conf_dir_path, help='Path to ca certs directory used to sign SSL certs. Defaults to ~/.mitmproxy')
@click.option('--certs-dir-path', default=DataDir.instance().certs_dir_path, help='Output directory.')
@click.argument('hostname')
def mkcert(**kwargs):
    mitmproxy_ca_certs_dir = kwargs['ca_certs_dir_path']

    installer = CertificateAuthority(mitmproxy_ca_certs_dir)

    try:
        installer.sign(kwargs['hostname'], kwargs['certs_dir_path'])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

@ca_cert.command()
@click.option('--ca-certs-dir-path', default=DataDir.instance().mitmproxy_conf_dir_path, help='Path to ca certs directory.')
def install(**kwargs):
    mitmproxy_ca_certs_dir = kwargs['ca_certs_dir_path']
    installer = CertificateAuthority(mitmproxy_ca_certs_dir)

    try:
        installer.install()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

@ca_cert.command()
def uninstall():
    print("Not yet implemented. Stay tuned!")