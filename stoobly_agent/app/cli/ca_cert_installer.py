import os
import subprocess

class CACertInstaller():

    def __init__(self):
        home_dir = os.path.expanduser('~')
        self.mitmproxy_certs_dir = os.path.join(home_dir, '.mitmproxy')
        self.pem_file_name = 'mitmproxy-ca-cert.pem'
        self.crt_file_name = 'mitmproxy-ca-cert.crt'

    # https://askubuntu.com/a/94861
    def handle_debian(self):
        extra_ca_certs_dir = '/usr/local/share/ca-certificates/extra'
        mitm_pem_absolute_path = os.path.join(self.mitmproxy_certs_dir, self.pem_file_name)
        mitm_crt_absolute_path = os.path.join(self.mitmproxy_certs_dir, self.crt_file_name)
        extra_crt_absolute_path = os.path.join(extra_ca_certs_dir, self.crt_file_name)

        subprocess.run(f"sudo mkdir -p {extra_ca_certs_dir}".split(), check=True)
        subprocess.run(f"openssl x509 -in {mitm_pem_absolute_path} -inform PEM -out {mitm_crt_absolute_path}".split(), check=True)
        subprocess.run(f"sudo cp {mitm_crt_absolute_path} {extra_crt_absolute_path}".split(), check=True)
        subprocess.run('sudo update-ca-certificates'.split(), check=True)

    # https://www.dssw.co.uk/reference/security.html
    def handle_darwin(self):
        system_keychain_path = '/Library/Keychains/System.keychain'
        mitm_pem_absolute_path = os.path.join(self.mitmproxy_certs_dir, self.pem_file_name)

        subprocess.run(f"sudo security add-trusted-cert -d -p ssl -p basic -k {system_keychain_path} {mitm_pem_absolute_path}".split(), check=True)
