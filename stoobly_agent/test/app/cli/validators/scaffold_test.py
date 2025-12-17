import pytest

from stoobly_agent.app.cli.validators.scaffold import validate_service_name
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_SERVICES


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
