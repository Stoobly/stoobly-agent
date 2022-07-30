import cgi
import json
import pdb
import urllib.parse

from mitmproxy.coretypes.multidict import MultiDict
from typing import Dict, Union

from .multipart import decode as multipart_decode, encode as multipart_encode

JSON = 'application/json'
MULTIPART_FORM = 'multipart/form-data'
WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'

def decode_response(content, content_type: Union[bytes, None, str]) -> Union[dict, list, MultiDict]:
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

def encode_response(content, content_type: Union[bytes, None, str]) -> Union[bytes, str]:
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
        return content

def parse_multipart_form_data(content, content_type) -> Dict[bytes, bytes]:
    headers = {'content-type': content_type}
    decoded_multipart = multipart_decode(headers, content)

    if not decoded_multipart:
        return content

    params_array = []
    for ele in decoded_multipart:
        params_array.append((ele[0].decode(), ele[1].decode()))

    return MultiDict(params_array)

def parse_www_form_urlencoded(content):
    try:
        return urllib.parse.parse_qs(content)
    except:
        return content

def serialize_json(o):
    return json.dumps(o)

def serialize_multipart_form_data(o: MultiDict, content_type: Union[bytes, str]) -> bytes:
    _o = MultiDict()
    for k, v in o.items():
        if isinstance(k, str):
            k = k.encode()

        if not isinstance(v, str) and not isinstance(v, bytes):
            v = str(v)

        if isinstance(v, str):
            v = v.encode()
        
        _o.add(k, v)

    headers = {'content-type': content_type}
    return multipart_encode(headers, _o.items())

def serialize_www_form_urlencoded(o):
    return urllib.parse.urlencode(o)

def normalize_header( header):
    if isinstance(header, bytes):
        header = header.decode('utf-8')
    return cgi.parse_header(header)[0].lower()

def is_traversable(content):
    return isinstance(content, list) or isinstance(content, dict) or isinstance(content, MultiDict)