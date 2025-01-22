import pdb
import pytest

from stoobly_agent.test.test_helper import reset

from stoobly_agent.config.constants.mitmproxy import DEFAULT_CONF_DIR_PATH
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
      assert certificate_authority.certs_dir == DEFAULT_CONF_DIR_PATH

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