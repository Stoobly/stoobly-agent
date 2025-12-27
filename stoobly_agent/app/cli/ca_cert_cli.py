import click
import os
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
@click.option(
    '--ca-certs-dir-path', 
    default=DataDir.instance().ca_certs_dir_path, 
    help='Path to ca certs directory used to sign SSL certs.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    '--certs-dir-path',
    default=DataDir.instance().certs_dir_path,
    help='Output directory.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.argument('hostname')
def mkcert(**kwargs):
    ca_certs_dir_path = kwargs['ca_certs_dir_path']

    installer = CertificateAuthority(ca_certs_dir_path)

    try:
        installer.sign(kwargs['hostname'], kwargs['certs_dir_path'])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

@ca_cert.command()
@click.option(
    '--ca-certs-dir-path',
    default=DataDir.instance().ca_certs_dir_path,
    help='Path to ca certs directory.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def install(**kwargs):
    ca_certs_dir_path = kwargs['ca_certs_dir_path']

    ca_cert_install(ca_certs_dir_path)

@ca_cert.command()
@click.option(
    '--ca-certs-dir-path',
    default=DataDir.instance().ca_certs_dir_path,
    help='Path to ca certs directory.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    '--format',
    type=click.Choice(['cer', 'p12', 'pem']),
    required=True,
    help='Certificate format: cer, p12, or pem.'
)
def show(**kwargs):
    ca_certs_dir_path = kwargs['ca_certs_dir_path']
    format_type = kwargs['format']
    
    installer = CertificateAuthority(ca_certs_dir_path)
    
    try:
        # Map format to file extension
        extension_map = {
            'cer': '.cer',
            'p12': '.p12',
            'pem': '.pem'
        }
        extension = extension_map[format_type]
        
        # Get the certificate path
        cert_path = installer.ca_cert_path(extension)
        
        # Check if certificate exists
        if not os.path.exists(cert_path):
            print(f"Certificate file not found: {cert_path}", file=sys.stderr)
            print("Run 'stoobly-agent ca-cert install' to generate certificates.", file=sys.stderr)
            sys.exit(1)
        
        # Output only the path to stdout (suitable for scripting)
        print(cert_path)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

@ca_cert.command()
def uninstall():
    print("Not yet implemented. Stay tuned!")

def ca_cert_install(ca_certs_dir_path: str):
    installer = CertificateAuthority(ca_certs_dir_path)

    try:
        installer.install()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)