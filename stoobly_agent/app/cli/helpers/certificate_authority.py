import distro
import os
import pdb
import socket
import ssl
import subprocess

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.x509.oid import NameOID
from pathlib import Path

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger

LOG_ID = 'CertificateAuthority'

MITMPROXY_CN = 'mitmproxy'

class CertificateAuthority():

    def __init__(self, certs_dir = DataDir.instance().ca_certs_dir_path, cn = MITMPROXY_CN):
        self.certs_dir = certs_dir
        self.cn = cn
        self.key_size = 2048

    @property
    def certs_generated(self):
        if not os.path.exists(self.ca_cert_path('.pem')):
            return False

        if not os.path.exists(self.ca_cert_path('.cer')):
            return False

        if not os.path.exists(self.ca_path('.pem')):
            return False

        return True

    def ca_file_name(self, extension: str):
        return '{cn}-ca{extension}'.format(cn=self.cn, extension=extension)

    def ca_path(self, extension: str):
        file_name = self.ca_file_name(extension)
        return os.path.join(self.certs_dir, file_name)

    def ca_cert_file_name(self, extension: str):
        return '{cn}-ca-cert{extension}'.format(cn=self.cn, extension=extension)

    def ca_cert_path(self, extension: str):
        file_name = self.ca_cert_file_name(extension)
        return os.path.join(self.certs_dir, file_name)

    def generate_certs(self):
        from mitmproxy.certs import CertStore

        if not os.path.exists(self.certs_dir):
            os.makedirs(self.certs_dir, exist_ok=True)

        path = Path(self.certs_dir)

        CertStore.create_store(path, self.cn, self.key_size)

    # https://askubuntu.com/a/94861
    def handle_debian(self):
        extra_ca_certs_dir = '/usr/local/share/ca-certificates/extra'

        ca_cert_path = self.ca_cert_path('.cer')
        self.__ensure_exists(ca_cert_path)

        extra_crt_absolute_path = os.path.join(extra_ca_certs_dir, self.ca_cert_file_name('.crt'))

        subprocess.run(f"sudo mkdir -p {extra_ca_certs_dir}".split(), check=True)
        subprocess.run(f"sudo cp {ca_cert_path} {extra_crt_absolute_path}".split(), check=True)
        subprocess.run("sudo update-ca-certificates".split(), check=True)

    # https://www.dssw.co.uk/reference/security.html
    def handle_darwin(self):
        system_keychain_path = '/Library/Keychains/System.keychain'

        ca_cert_path = self.ca_cert_path('.pem')
        self.__ensure_exists(ca_cert_path)

        subprocess.run(f"sudo security add-trusted-cert -d -p ssl -p basic -k {system_keychain_path} {ca_cert_path}".split(), check=True)

    def handle_rhel(self):
        ca_trust_dir = '/etc/pki/ca-trust/source/anchors'

        ca_cert_path = self.ca_cert_path('.cer')
        self.__ensure_exists(ca_cert_path)

        ca_trust_crt_absolute_path = os.path.join(ca_trust_dir, self.crt_file_name)

        subprocess.run(f"sudo cp {ca_cert_path} {ca_trust_crt_absolute_path}".split(), check=True)
        subprocess.run("sudo update-ca-trust extract".split(), check=True)

    def install(self):
        if not self.certs_generated:
            self.generate_certs()

        distro_name = distro.name(pretty=True)

        # Ubuntu or other Debian based
        if distro.like() == 'debian':
            self.handle_debian()
        # MacOS
        elif distro.id() == 'darwin':
            self.handle_darwin()
        # elif distro.id() == 'rhel':
        #     return
        else:
            raise TypeError(
                f"{distro_name} is not supported yet for automatic installation. For manual installation, see https://docs.mitmproxy.org/stable/concepts-certificates/"
            )

    def sign(self, hostname: str, dest = None, port = 443):
        from mitmproxy.certs import CertStore

        dest = dest or self.certs_dir

        if self.signed(hostname, dest):
            return False

        store = CertStore.from_store(self.certs_dir, self.cn, self.key_size)
        organization, alt_names = self.__cert_details(hostname, port)
        cert_entry = store.get_cert(alt_names[0], alt_names, organization)

        crt_path = os.path.join(dest, f"{hostname}.crt")
        with open(crt_path, 'wb') as fp:
            cert = cert_entry.cert
            crt = cert.to_pem()
            fp.write(crt)

        key_path = os.path.join(dest, f"{hostname}.key")
        with open(key_path, 'wb') as fp:
            private_key = cert_entry.privatekey
            key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
            fp.write(key)

        joined_path = os.path.join(dest, f"{hostname}-joined.pem")
        with open(joined_path, 'wb') as fp:
            fp.write(b"\n".join([crt, key]))

        return True

    def signed(self, hostname: str, dest = None):
        dest = dest or self.certs_dir

        crt_path = os.path.join(dest, f"{hostname}.crt")
        if not os.path.exists(crt_path):
            return False

        key_path = os.path.join(dest, f"{hostname}.key")
        if not os.path.exists(key_path):
            return False

        joined_path = os.path.join(dest, f"{hostname}-joined.pem")
        if not os.path.exists(joined_path):
            return False

        # Verify the certificate was signed by this CA
        try:
            # Load the CA certificate
            ca_cert_path = self.ca_cert_path('.pem')
            if not os.path.exists(ca_cert_path):
                return False
                
            with open(ca_cert_path, 'rb') as f:
                ca_cert_data = f.read()
                ca_cert = x509.load_pem_x509_certificate(ca_cert_data, default_backend())
            
            # Load the signed certificate
            with open(crt_path, 'rb') as f:
                cert_data = f.read()
                certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Check 1: Verify issuer matches CA subject
            if certificate.issuer != ca_cert.subject:
                return False
            
            # Check 2: Verify the signature using CA's public key
            from cryptography.hazmat.primitives.asymmetric import padding
            
            ca_public_key = ca_cert.public_key()
            
            # Handle different key types
            if isinstance(ca_public_key, rsa.RSAPublicKey):
                # RSA signature verification - check if PSS or PKCS1v15 padding is used
                signature_algorithm = certificate.signature_algorithm_oid
                
                # Check if signature uses PSS padding
                if signature_algorithm in (
                    x509.SignatureAlgorithmOID.RSASSA_PSS,
                ):
                    # Use PSS padding with MGF1 and MAX_LENGTH salt
                    ca_public_key.verify(
                        certificate.signature,
                        certificate.tbs_certificate_bytes,
                        padding.PSS(
                            mgf=padding.MGF1(certificate.signature_hash_algorithm),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        certificate.signature_hash_algorithm,
                    )
                else:
                    # Use PKCS1v15 padding (default for most RSA signatures)
                    ca_public_key.verify(
                        certificate.signature,
                        certificate.tbs_certificate_bytes,
                        padding.PKCS1v15(),
                        certificate.signature_hash_algorithm,
                    )
            elif isinstance(ca_public_key, ec.EllipticCurvePublicKey):
                # ECDSA signature verification (uses different padding)
                ca_public_key.verify(
                    certificate.signature,
                    certificate.tbs_certificate_bytes,
                    ec.ECDSA(certificate.signature_hash_algorithm),
                )
            else:
                # Unknown key type - log warning and assume valid
                Logger.instance(LOG_ID).warning(f"Unknown key type for CA certificate: {type(ca_public_key)}")
                return False
            
            return True
        except InvalidSignature:
            Logger.instance(LOG_ID).warning(f"Certificate signature verification failed for {hostname}: certificate was not signed by this CA")
            return False
        except Exception as e:
            Logger.instance(LOG_ID).warning(f"Certificate verification failed for {hostname}: {e}")
            return False

    def __ensure_exists(self, file_path):
        if not os.path.exists(file_path):
            self.generate_certs()

    def __cert_details(self, domain: str, port: int = 443):
        """
        Retrieves the organization name and subject alternative names from an HTTPS domain's certificate.

        :param domain: The domain name (e.g., 'example.com').
        :param port: The port number (default: 443 for HTTPS).
        :return: A tuple containing the organization name and a list of alternative names (or None if not found).
        """
        alt_names = [domain]
        try:
            # Connect to the server and get the certificate
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            timeout = 2.5
            with socket.create_connection((domain, port), timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert_der = ssock.getpeercert(binary_form=True)

            # Parse the certificate
            cert = x509.load_der_x509_certificate(cert_der, default_backend())

            # Extract the organization name
            try:
                org_name = cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
            except IndexError:
                org_name = None

            # Extract the Subject Alternative Names (SANs)
            try:
                ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
                alt_names.extend(ext.value.get_values_for_type(x509.DNSName))
            except x509.ExtensionNotFound:
                alt_names = []

            return org_name, alt_names

        except Exception as e:
            Logger.instance(LOG_ID).debug(f"Could not retrieve certificate for {domain}: {e}")
            return None, alt_names