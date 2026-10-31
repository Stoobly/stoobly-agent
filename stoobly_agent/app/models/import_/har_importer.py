import base64
import json
import re
from typing import List, Tuple, Union

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.proxy.record import REQUEST_DELIMITTER
from stoobly_agent.app.settings import Settings

_GOR_CONTROL_LINE = re.compile(rb'^[12] ')


def looks_like_gor(raw_data: Union[bytes, bytearray, str]) -> bool:
  if isinstance(raw_data, str):
    raw_bytes = raw_data.encode('utf-8', errors='replace')
  else:
    raw_bytes = bytes(raw_data)

  if REQUEST_DELIMITTER in raw_bytes:
    return True

  # GOR payloads start with a type-1 (request) or type-2 (response) control line.
  # json.loads often parses the leading "1" as a number and fails with Extra data.
  first_line = raw_bytes.lstrip(b'\r\n').split(b'\n', 1)[0]
  return bool(_GOR_CONTROL_LINE.match(first_line))


class HarImporter:

  def import_file(self, raw_data, scenario_id, settings: Settings = None, **_kwargs) -> Tuple[dict, int]:
    settings = settings or Settings.instance()

    if looks_like_gor(raw_data):
      return {
        'error': 'Content looks like GOR. Try format GOR instead.'
      }, 400

    try:
      if isinstance(raw_data, (bytes, bytearray)):
        raw_data = raw_data.decode('utf-8')
      data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
      return {'error': f'Invalid HAR file: could not parse JSON ({e})'}, 400

    entries = (data.get('log') or {}).get('entries') if isinstance(data, dict) else None
    if not isinstance(entries, list):
      return {'error': 'Invalid HAR file: missing log.entries'}, 400

    created = []
    for entry in entries:
      if not isinstance(entry, dict):
        continue

      resource_type = entry.get('_resourceType')
      if resource_type is not None and resource_type not in ('xhr', 'document'):
        continue

      request = entry.get('request') or {}
      if not isinstance(request, dict):
        request = {}
      response = entry.get('response') or {}
      if not isinstance(response, dict):
        response = {}
      response = self.__preprocess_response(response)

      builder = RequestBuilder(
        method=request.get('method') or 'GET',
        url=request.get('url'),
        request_headers=self.__headers_to_dict(request.get('headers')),
        request_body=self.__request_body(request.get('postData')),
        response_headers=self.__headers_to_dict(response.get('headers')),
        response_body=self.__response_body(response.get('content') or {}),
        status_code=response.get('status') or 0,
        scenario_id=scenario_id,
      ).with_settings(settings)

      res, status = builder.build(skip_if_not_allowed=True)
      if res is None and status is None:
        continue
      if status != 200:
        return res, status

      created.append(res['list'][0])

    return {'list': created, 'total': len(created)}, 200

  def __headers_to_dict(self, headers: List[dict]) -> dict:
    if not isinstance(headers, list):
      return {}

    result = {}
    for header in headers:
      name = header.get('name')
      if not name or name.lower() == 'content-encoding':
        continue
      if not self.__valid_header_name(name):
        continue
      result[name] = header.get('value') or ''
    return result

  def __valid_header_name(self, name: str) -> bool:
    # Mirror Ruby: header['name'] =~ /[^:\s][^:\r\n]*/
    if not name or name[0] in (':', ' ', '\t'):
      return False
    return '\r' not in name and '\n' not in name and ':' not in name[1:]

  def __request_body(self, post_data) -> bytes:
    if not isinstance(post_data, dict):
      return b''
    text = post_data.get('text')
    if text is None:
      return b''
    return text.encode() if isinstance(text, str) else text

  def __response_body(self, content: dict) -> bytes:
    text = content.get('text')
    if text is None:
      return b''
    if isinstance(text, bytes):
      return text
    return text.encode() if isinstance(text, str) else b''

  def __preprocess_response(self, response: dict) -> dict:
    headers = response.get('headers') or []
    if isinstance(headers, list):
      response = {**response, 'headers': [
        h for h in headers
        if isinstance(h, dict) and (h.get('name') or '').lower() != 'content-encoding'
      ]}

    content = response.get('content') or {}
    encoding = content.get('encoding')
    if encoding == 'base64' and content.get('text') is not None:
      decoded = base64.b64decode(content['text'])
      content = {**content, 'text': decoded, 'encoding': None, 'size': len(decoded)}
      response = {**response, 'content': content}

    return response
