import json
import os
import pytest

from unittest.mock import MagicMock, patch

from stoobly_agent.config.mitmproxy import MitmproxyConfig


@pytest.fixture(autouse=True)
def reset_singleton():
    MitmproxyConfig._MitmproxyConfig__instance = None
    yield
    MitmproxyConfig._MitmproxyConfig__instance = None


class TestMitmproxyConfig:

    class TestInstance:

        def test_returns_same_instance(self):
            master = MagicMock()
            a = MitmproxyConfig.instance(master)
            b = MitmproxyConfig.instance()
            assert a is b

        def test_raises_if_constructed_directly_after_singleton_set(self):
            master = MagicMock()
            MitmproxyConfig.instance(master)
            with pytest.raises(RuntimeError):
                MitmproxyConfig(master)

    class TestGet:

        class TestWithMaster:

            def test_returns_option_value(self):
                option_val = MagicMock()
                option_val.current.return_value = '0.0.0.0'

                master = MagicMock()
                master.options.__contains__ = MagicMock(return_value=True)
                master.options.items.return_value = [('listen_host', option_val)]

                config = MitmproxyConfig.instance(master)
                assert config.get('listen_host') == '0.0.0.0'

            def test_returns_none_for_unknown_key(self):
                master = MagicMock()
                master.options.__contains__ = MagicMock(return_value=False)

                config = MitmproxyConfig.instance(master)
                assert config.get('unknown_key') is None

        class TestWithoutMaster:

            def test_reads_from_json_file(self, tmp_path):
                json_path = str(tmp_path / 'options.json')
                with open(json_path, 'w') as f:
                    json.dump({'listen_host': '127.0.0.1'}, f)

                data_dir_mock = MagicMock()
                data_dir_mock.mitmproxy_options_json_path = json_path

                config = MitmproxyConfig.instance()

                with patch('stoobly_agent.config.mitmproxy.DataDir') as MockDataDir:
                    MockDataDir.instance.return_value = data_dir_mock
                    result = config.get('listen_host')

                assert result == '127.0.0.1'

            def test_returns_none_on_missing_file(self, tmp_path):
                data_dir_mock = MagicMock()
                data_dir_mock.mitmproxy_options_json_path = str(tmp_path / 'nonexistent.json')

                config = MitmproxyConfig.instance()

                with patch('stoobly_agent.config.mitmproxy.DataDir') as MockDataDir:
                    MockDataDir.instance.return_value = data_dir_mock
                    result = config.get('listen_host')

                assert result is None

    class TestSet:

        def test_calls_master_options_set(self):
            master = MagicMock()
            config = MitmproxyConfig.instance(master)
            config.set(('listen_host', '127.0.0.1'))
            master.options.set.assert_called_once_with('listen_host', '127.0.0.1')

        def test_noop_when_no_master(self):
            config = MitmproxyConfig.instance()
            config.set(('listen_host', '127.0.0.1'))

    class TestDump:

        def test_writes_json_file(self, tmp_path):
            json_path = str(tmp_path / 'options.json')

            data_dir_mock = MagicMock()
            data_dir_mock.mitmproxy_options_json_path = json_path

            option_val = MagicMock()
            option_val.current.return_value = '0.0.0.0'

            master = MagicMock()
            master.options.items.return_value = [('listen_host', option_val)]

            config = MitmproxyConfig.instance(master)

            with patch('stoobly_agent.config.mitmproxy.DataDir') as MockDataDir:
                MockDataDir.instance.return_value = data_dir_mock
                config.dump()

            assert os.path.exists(json_path)
            with open(json_path) as f:
                data = json.loads(f.read())
            assert data == {'listen_host': '0.0.0.0'}

        def test_noop_when_no_master(self):
            config = MitmproxyConfig.instance()
            config.dump()
