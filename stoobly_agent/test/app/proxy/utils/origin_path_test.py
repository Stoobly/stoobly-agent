from os.path import expanduser

from stoobly_agent.app.proxy.utils.origin_path import parse_origin_path_item

class TestParseOriginPathItem():

    def test_parses_path_with_scheme_origin(self):
        path, origin = parse_origin_path_item("/dir/subdir:https://api.example.com")
        assert path == "/dir/subdir"
        assert origin == "https://api.example.com"

    def test_parses_path_with_scheme_and_port_origin(self):
        path, origin = parse_origin_path_item("/dir:https://api.example.com:8443")
        assert path == "/dir"
        assert origin == "https://api.example.com:8443"

    def test_parses_path_with_host_port_no_scheme(self):
        path, origin = parse_origin_path_item("folder:api.example.com:8080")
        assert path == "folder"
        assert origin == "api.example.com:8080"

    def test_parses_path_without_origin(self):
        path, origin = parse_origin_path_item("/just/a/path")
        assert path == "/just/a/path"
        assert origin is None

    def test_handles_multiple_colons_before_scheme(self):
        # Ensure we split at the last colon before the scheme delimiter
        s = "/a:b:c:https://example.com"
        path, origin = parse_origin_path_item(s)
        assert path == "/a:b:c"
        assert origin == "https://example.com"

    def test_item_is_full_url_no_explicit_path(self):
        # When the token itself looks like a URL, treat it as path with no origin
        s = "https://example.com/service"
        path, origin = parse_origin_path_item(s)
        assert path == s
        assert origin is None

    def test_empty_and_whitespace_inputs(self):
        assert parse_origin_path_item("") == (None, None)
        assert parse_origin_path_item("   ") == (None, None)

    def test_expands_user_home_without_origin(self):
        inp = "~/just/a/path"
        path, origin = parse_origin_path_item(inp)
        assert path == expanduser(inp)
        assert origin is None

    def test_expands_user_home_with_scheme_origin(self):
        inp = "~/dir:https://api.example.com"
        path, origin = parse_origin_path_item(inp)
        assert path == expanduser("~/dir")
        assert origin == "https://api.example.com"
