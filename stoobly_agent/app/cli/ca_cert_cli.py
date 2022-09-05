
import click
import distro

from .ca_cert_installer import CACertInstaller

@click.group(
    epilog="Run 'stoobly-agent COMMAND --help' for more information on a command.",
    help="Manage CA certificate"
)
@click.pass_context
def ca_cert(ctx):
    pass

@ca_cert.command()
def install(**kwargs):
    distro_name = distro.name(pretty=True)

    installer = CACertInstaller()

    # Ubuntu or other Debian based
    if distro.like() == 'debian':
        print(f"Installing CA certificate for {distro_name}...")
        installer.handle_debian()
    # MacOS
    elif distro.id() == 'darwin':
        installer.handle_darwin()
    # elif distro.id() == 'rhel':
    #     return
    else:
        print(f"{distro_name} is not supported yet for automatic CA cert installation.")

@ca_cert.command()
def uninstall():
    print("Not yet implemented. Stay tuned!")