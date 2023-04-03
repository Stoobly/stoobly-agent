import os
import subprocess
import sys

class CACertInstaller():

    def __init__(self):
        home_dir = os.path.expanduser('~')
        self.mitmproxy_certs_dir = os.path.join(home_dir, '.mitmproxy')
        self.pem_file_name = 'mitmproxy-ca-cert.pem'
        self.cer_file_name = 'mitmproxy-ca-cert.cer'
        self.crt_file_name = 'mitmproxy-ca-cert.crt'

    @property
    def mitm_crt_absolute_path(self):
        return os.path.join(self.mitmproxy_certs_dir, self.crt_file_name)

    # https://askubuntu.com/a/94861
    def handle_debian(self):
        extra_ca_certs_dir = '/usr/local/share/ca-certificates/extra'

        mitm_cer_absolute_path = os.path.join(self.mitmproxy_certs_dir, self.cer_file_name)
        self.__ensure_exists(mitm_cer_absolute_path)

        extra_crt_absolute_path = os.path.join(extra_ca_certs_dir, self.crt_file_name)

        subprocess.run(f"sudo mkdir -p {extra_ca_certs_dir}".split(), check=True)
        subprocess.run(f"sudo cp {mitm_cer_absolute_path} {extra_crt_absolute_path}".split(), check=True)
        subprocess.run("sudo update-ca-certificates".split(), check=True)

    # https://www.dssw.co.uk/reference/security.html
    def handle_darwin(self):
        system_keychain_path = '/Library/Keychains/System.keychain'

        mitm_pem_absolute_path = os.path.join(self.mitmproxy_certs_dir, self.pem_file_name)
        self.__ensure_exists(mitm_pem_absolute_path)

        subprocess.run(f"sudo security add-trusted-cert -d -p ssl -p basic -k {system_keychain_path} {mitm_pem_absolute_path}".split(), check=True)

    def handle_rhel(self):
        ca_trust_dir = '/etc/pki/ca-trust/source/anchors'

        mitm_cer_absolute_path = os.path.join(self.mitmproxy_certs_dir, self.cer_file_name)
        self.__ensure_exists(mitm_cer_absolute_path)

        ca_trust_crt_absolute_path = os.path.join(ca_trust_dir, self.crt_file_name)

        subprocess.run(f"sudo cp {mitm_cer_absolute_path} {ca_trust_crt_absolute_path}".split(), check=True)
        subprocess.run("sudo update-ca-trust extract".split(), check=True)

    def __ensure_exists(self, file_path):
        if not os.path.exists(file_path):
            print("Error: Proxy has not been started", file=sys.stderr)
            sys.exit(1)