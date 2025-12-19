import pytest

from stoobly_agent.app.cli.validators.scaffold import (
    validate_app_name,
    validate_hostname,
    validate_namespace,
    validate_network,
    validate_service_name,
)
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_SERVICES


class TestValidateAppName:

    def test_returns_valid_app_name(self):
        result = validate_app_name(None, None, "myapp")
        assert result == "myapp"

    def test_accepts_alphanumeric_names(self):
        result = validate_app_name(None, None, "app123")
        assert result == "app123"

    def test_accepts_names_with_dots(self):
        result = validate_app_name(None, None, "my.app")
        assert result == "my.app"

    def test_accepts_names_with_underscores(self):
        result = validate_app_name(None, None, "my_app")
        assert result == "my_app"

    def test_accepts_names_with_hyphens(self):
        result = validate_app_name(None, None, "my-app")
        assert result == "my-app"

    def test_accepts_mixed_case(self):
        result = validate_app_name(None, None, "MyApp")
        assert result == "MyApp"

    def test_rejects_name_with_spaces(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_app_name(None, None, "my app")
        assert exc_info.value.code == 1

    def test_rejects_name_with_special_characters(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_app_name(None, None, "my@app")
        assert exc_info.value.code == 1

    def test_rejects_name_with_slash(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_app_name(None, None, "my/app")
        assert exc_info.value.code == 1

    def test_rejects_empty_name(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_app_name(None, None, "")
        assert exc_info.value.code == 1


class TestValidateHostname:

    def test_returns_valid_hostname(self):
        result = validate_hostname(None, None, "example.com")
        assert result == "example.com"

    def test_accepts_alphanumeric_hostnames(self):
        result = validate_hostname(None, None, "host123")
        assert result == "host123"

    def test_accepts_hostnames_with_dots(self):
        result = validate_hostname(None, None, "sub.domain.example.com")
        assert result == "sub.domain.example.com"

    def test_accepts_hostnames_with_hyphens(self):
        result = validate_hostname(None, None, "my-hostname")
        assert result == "my-hostname"

    def test_accepts_mixed_case(self):
        result = validate_hostname(None, None, "MyHost.Example.COM")
        assert result == "MyHost.Example.COM"

    def test_rejects_hostname_with_spaces(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_hostname(None, None, "my host")
        assert exc_info.value.code == 1

    def test_rejects_hostname_with_special_characters(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_hostname(None, None, "host@name")
        assert exc_info.value.code == 1

    def test_rejects_hostname_with_underscore(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_hostname(None, None, "my_host")
        assert exc_info.value.code == 1

    def test_rejects_hostname_with_slash(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_hostname(None, None, "host/name")
        assert exc_info.value.code == 1

    def test_returns_none_when_hostname_is_none(self):
        result = validate_hostname(None, None, None)
        assert result is None

    def test_returns_none_when_hostname_is_empty(self):
        result = validate_hostname(None, None, "")
        assert result is None


class TestValidateNetwork:

    def test_returns_valid_network(self):
        result = validate_network(None, None, "mynetwork")
        assert result == "mynetwork"

    def test_accepts_alphanumeric_networks(self):
        result = validate_network(None, None, "network123")
        assert result == "network123"

    def test_accepts_networks_with_dots(self):
        result = validate_network(None, None, "my.network")
        assert result == "my.network"

    def test_accepts_networks_with_underscores(self):
        result = validate_network(None, None, "my_network")
        assert result == "my_network"

    def test_accepts_networks_with_hyphens(self):
        result = validate_network(None, None, "my-network")
        assert result == "my-network"

    def test_accepts_mixed_case(self):
        result = validate_network(None, None, "MyNetwork")
        assert result == "MyNetwork"

    def test_rejects_network_with_spaces(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_network(None, None, "my network")
        assert exc_info.value.code == 1

    def test_rejects_network_with_special_characters(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_network(None, None, "my@network")
        assert exc_info.value.code == 1

    def test_rejects_network_with_slash(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_network(None, None, "my/network")
        assert exc_info.value.code == 1

    def test_returns_none_when_network_is_none(self):
        result = validate_network(None, None, None)
        assert result is None

    def test_returns_none_when_network_is_empty(self):
        result = validate_network(None, None, "")
        assert result is None


class TestValidateNamespace:

    def test_returns_valid_namespace(self):
        result = validate_namespace(None, None, "mynamespace")
        assert result == "mynamespace"

    def test_accepts_lowercase_alphanumeric(self):
        result = validate_namespace(None, None, "namespace123")
        assert result == "namespace123"

    def test_accepts_namespaces_with_underscores(self):
        result = validate_namespace(None, None, "my_namespace")
        assert result == "my_namespace"

    def test_accepts_namespaces_with_hyphens(self):
        result = validate_namespace(None, None, "my-namespace")
        assert result == "my-namespace"

    def test_rejects_namespace_with_uppercase(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_namespace(None, None, "MyNamespace")
        assert exc_info.value.code == 1

    def test_rejects_namespace_with_dots(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_namespace(None, None, "my.namespace")
        assert exc_info.value.code == 1

    def test_rejects_namespace_with_spaces(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_namespace(None, None, "my namespace")
        assert exc_info.value.code == 1

    def test_rejects_namespace_with_special_characters(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_namespace(None, None, "my@namespace")
        assert exc_info.value.code == 1

    def test_rejects_namespace_starting_with_hyphen(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_namespace(None, None, "-namespace")
        assert exc_info.value.code == 1

    def test_rejects_namespace_starting_with_underscore(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_namespace(None, None, "_namespace")
        assert exc_info.value.code == 1

    def test_returns_none_when_namespace_is_none(self):
        result = validate_namespace(None, None, None)
        assert result is None

    def test_returns_none_when_namespace_is_empty(self):
        result = validate_namespace(None, None, "")
        assert result is None


class TestValidateServiceName:

    @pytest.mark.parametrize("core_service", CORE_SERVICES)
    def test_core_service_is_rejected(self, core_service: str):
        with pytest.raises(SystemExit) as exc_info:
            validate_service_name(None, None, core_service)
        assert exc_info.value.code == 1

    def test_returns_valid_service_name(self):
        result = validate_service_name(None, None, "service")
        assert result == "service"

    def test_accepts_alphanumeric_names(self):
        result = validate_service_name(None, None, "service123")
        assert result == "service123"

    def test_accepts_names_with_dots(self):
        result = validate_service_name(None, None, "my.service")
        assert result == "my.service"

    def test_accepts_names_with_underscores(self):
        result = validate_service_name(None, None, "my_service")
        assert result == "my_service"

    def test_accepts_names_with_hyphens(self):
        result = validate_service_name(None, None, "service-with-hyphens")
        assert result == "service-with-hyphens"

    def test_accepts_mixed_case(self):
        result = validate_service_name(None, None, "MyService")
        assert result == "MyService"
    
    def test_rejects_name_with_spaces(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_service_name(None, None, "my service")
        assert exc_info.value.code == 1

    def test_rejects_name_with_special_characters(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_service_name(None, None, "my@service")
        assert exc_info.value.code == 1

    def test_rejects_name_with_slash(self):
        with pytest.raises(SystemExit) as exc_info:
            validate_service_name(None, None, "my/service")
        assert exc_info.value.code == 1

    def test_returns_none_when_service_name_is_none(self):
        result = validate_service_name(None, None, None)
        assert result is None

    def test_returns_none_when_service_name_is_empty(self):
        result = validate_service_name(None, None, "")
        assert result is None
