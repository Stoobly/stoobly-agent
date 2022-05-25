import cgi
import json
import pdb
import urllib.parse

from mitmproxy.coretypes.multidict import MultiDict
from mitmproxy.net.http.multipart import decode as multipart_decode, encode as multipart_encode
from typing import Dict, Union

JSON = 'application/json'
MULTIPART_FORM = 'multipart/form-data'
WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'

def decode_response(content, content_type: Union[bytes, None, str]):
    if not content_type:
        return content

    _content_type = normalize_header(content_type)

    decoded_response = content
    if _content_type == JSON:
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        decoded_response = parse_json(content)
    elif _content_type == WWW_FORM_URLENCODED:
        decoded_response = parse_www_form_urlencoded(content)
    elif _content_type == MULTIPART_FORM:
        decoded_response = parse_multipart_form_data(content, content_type)

    return decoded_response

def encode_response(content, content_type: Union[bytes, None, str]):
    if not content_type:
        raise ValueError('Missing content_type value')

    _content_type = normalize_header(content_type)

    encoded_response = content
    if _content_type == JSON:
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        encoded_response = serialize_json(content)
    elif _content_type == WWW_FORM_URLENCODED:
        encoded_response = serialize_www_form_urlencoded(content)
    elif _content_type == MULTIPART_FORM:
        encoded_response = serialize_multipart_form_data(content, content_type)

    return encoded_response   

def parse_json(content):
    try:
        return json.loads(content)
    except:
        return {}

def parse_multipart_form_data(content, content_type) -> Dict[bytes, bytes]:
    headers = {'content-type': content_type}
    params_array = multipart_decode(headers, content)
    return MultiDict(params_array)

def parse_www_form_urlencoded(content):
    try:
        return urllib.parse.parse_qs(content)
    except:
        return {}

def serialize_json(o):
    return json.dumps(o)

def serialize_multipart_form_data(o: MultiDict, content_type: Union[bytes, str]):
    headers = {'content-type': content_type}
    return multipart_encode(headers, o.items())

def serialize_www_form_urlencoded(o):
    return urllib.parse.urlencode(o)

def normalize_header( header):
    if isinstance(header, bytes):
        header = header.decode('utf-8')
    return cgi.parse_header(header)[0].lower()