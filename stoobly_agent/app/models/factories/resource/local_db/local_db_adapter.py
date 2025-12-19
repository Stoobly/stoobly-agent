import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import Response as MitmproxyResponse

class LocalDBAdapter():

  def content_encoding_header(self, new_headers: dict, old_headers: dict):
    content_encoding = new_headers.get('content-encoding')
    if not content_encoding:
      # If content-encoding has changed, we will need to decode 'text' and re-encode it
      content_encoding = old_headers.get('content-encoding') 
    return content_encoding

  def encode_body(self, body: str, content_encoding: str):
    # If a content encoding is set in the response headers, encode the body
    # TODO: we may want to create a separate endpoint for this and have the client drive encoding before updating
    # otherwise, there's an assumption that the 'text' will always be provided as decoded

    if content_encoding:
      # Lazy import for runtime usage
      from mitmproxy.http import Response as MitmproxyResponse
      # Use MitmproxyResponse to encode the body
      res = MitmproxyResponse.make(
          200,
          body,
          {'content-encoding': content_encoding}
      )
      return res.raw_content
    else: 
      return body.encode()

  def success(self, d):
    return d, 200

  def bad_request(self, d = ''):
    return d, 400

  def not_found(self, d = 'Not Found'):
    return d, 404

  def conflict(self, d = ''):
    return d, 409

  def internal_error(self, d = 'Internal Error'):
    return d, 500

  def validate_uuid(self, id: str):
    try:
      uuid.UUID(id)
      return True
    except Exception:
      return False