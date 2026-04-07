from stoobly_agent.app.proxy.replay import replay_request_service


class TestHandlePathHeader():
  def test_does_not_absolutize_url_like_token(self):
    headers = {}
    raw = 'https://example.com/hooks.js'

    handle_path_header = getattr(replay_request_service, '__handle_path_header')
    handle_path_header('x-test-header', raw, headers)

    assert headers['x-test-header'] == raw
