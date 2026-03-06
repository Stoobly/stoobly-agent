import pdb
import pytest
import tempfile

from stoobly_agent.test.test_helper import reset

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.app.cli.helpers.certificate_authority import CertificateAuthority

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()

class TestCertificateAuthority():

  @pytest.fixture(autouse=True, scope='class')
  def certificate_authority(self):
    return CertificateAuthority(DataDir.instance().certs_dir_path)

  class TestWhenCertDirConfigured():

    def test_defaults_to_not_installed(self, certificate_authority: CertificateAuthority):
      assert not certificate_authority.certs_generated

    def test_generates(self, certificate_authority: CertificateAuthority):
      certificate_authority.generate_certs()
      assert certificate_authority.certs_generated

  class TestWhenCertDirNotConfigured():

    @pytest.fixture(autouse=True, scope='class')
    def certificate_authority(self):
      return CertificateAuthority()

    def test_defaults_to_mitmproxy_confdir(self, certificate_authority: CertificateAuthority):
      assert certificate_authority.certs_dir == DataDir.instance().ca_certs_dir_path

  class TestSign():

    class TestWhenExistentHostname():

      @pytest.fixture(scope='class')
      def hostname(self):
        return 'www.google.com'

      @pytest.fixture(autouse=True, scope='class')
      def sign(self, certificate_authority: CertificateAuthority, hostname: str):
        certificate_authority.sign(hostname)

      def test_signed(self, certificate_authority: CertificateAuthority, hostname: str):
        assert certificate_authority.signed(hostname)

    class TestWhenNonExistentHostname():

      @pytest.fixture(scope='class')
      def hostname(self):
        return 'test.stoobly.com'

      @pytest.fixture(autouse=True, scope='class')
      def sign(self, certificate_authority: CertificateAuthority, hostname: str):
        certificate_authority.sign(hostname)

      def test_signed(self, certificate_authority: CertificateAuthority, hostname: str):
        assert certificate_authority.signed(hostname)

    class TestWhenSigned():

      @pytest.fixture(scope='class')
      def hostname(self):
        return 'www.google.com'

      @pytest.fixture(autouse=True, scope='class')
      def sign(self, certificate_authority: CertificateAuthority, hostname: str):
        certificate_authority.sign(hostname)

      def test_it_does_not_sign(self, certificate_authority: CertificateAuthority, hostname: str):
        assert not certificate_authority.sign(hostname)

    class TestWhenSignedByDifferentCA():

      @pytest.fixture(scope='class')
      def hostname(self):
        return 'test.stoobly.com'

      @pytest.fixture(scope='class')
      def other_ca_dir(self):
        """Create a temporary directory for a different CA"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

      @pytest.fixture(autouse=True, scope='class')
      def setup_cas(self, certificate_authority: CertificateAuthority, other_ca_dir: str):
        """Ensure both CAs have their certificates generated"""
        # Generate certificates for the first CA (if not already generated)
        if not certificate_authority.certs_generated:
          certificate_authority.generate_certs()

      @pytest.fixture(scope='class')
      def other_ca(self, other_ca_dir):
        """Create a second CertificateAuthority with a different CA"""
        other_ca = CertificateAuthority(other_ca_dir)
        other_ca.generate_certs()
        return other_ca

      @pytest.fixture(autouse=True, scope='class')
      def sign_with_other_ca(self, other_ca: CertificateAuthority, hostname: str, other_ca_dir):
        """Sign a certificate with the different CA"""
        other_ca.sign(hostname, dest=other_ca_dir)

      def test_signed_returns_false(self, certificate_authority: CertificateAuthority, hostname: str, other_ca_dir: str):
        """Verify that signed returns False when certificate was signed by a different CA"""
        # Use the destination directory where the certificate was signed by the other CA
        assert not certificate_authority.signed(hostname, dest=other_ca_dir)