from stoobly_agent.app.models.adapters import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

def verify_raw_request(raw_request: bytes):
  adapter = JoinedRequestAdapter(raw_request)
  response_string = adapter.build_response_string().get()
  python_response = RawHttpResponseAdapter(response_string).to_response()

  raw_response = PythonResponseAdapterFactory(python_response).raw_response()
  adapter.raw_response_string = raw_response

  joined_request = adapter.adapt()
  return joined_request.build()