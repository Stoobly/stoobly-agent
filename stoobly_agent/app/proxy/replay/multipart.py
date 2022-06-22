import mimetypes
import re
import pdb

from urllib.parse import quote

from mitmproxy.net.http import headers

CRLF = b'\r\n'

def encode(head, l):

    k = head.get("content-type")
    if k:
        k = headers.parse_content_type(k)
        if k is not None:
            try:
                boundary = k[2]["boundary"].encode("ascii")
                boundary = quote(boundary)
            except (KeyError, UnicodeError):
                return b""

            hdrs = []
            for key, value in l:
                file_type = mimetypes.guess_type(str(key))[0] or "text/plain; charset=utf-8"

                if key:
                    hdrs.append(b"--%b" % boundary.encode('utf-8'))
                    disposition = b'form-data; name="%b"' % key
                    hdrs.append(b"Content-Disposition: %b" % disposition)
                    hdrs.append(b"Content-Type: %b" % file_type.encode('utf-8'))
                    hdrs.append(b'')
                    hdrs.append(value)
                #hdrs.append(b'')

                if value is not None:
                    # If boundary is found in value then raise ValueError
                    if re.search(rb"^--%b$" % re.escape(boundary.encode('utf-8')), value):
                        raise ValueError(b"boundary found in encoded string")

            hdrs.append(b"--%b--\r\n" % boundary.encode('utf-8'))

            temp = b"\r\n".join(hdrs)
            return temp


def decode(hdrs, content):
    """
        Takes a multipart boundary encoded string and returns list of (key, value) tuples.
    """
    if not isinstance(content, bytes) and not isinstance(content, str):
        return

    v = hdrs.get("content-type")
    if not v:
        return

    v = headers.parse_content_type(v)
    if not v:
        return

    try:
        boundary = v[2]["boundary"].encode("ascii")
    except (KeyError, UnicodeError):
        return

    boundary_parts = content.split(b"--" + boundary)
    if len(boundary_parts) == 0:
        return

    rx = re.compile(br'\bname="([^"]+)"')
    r = []
    for i in boundary_parts:
        parts = i.splitlines(True)

        if len(parts) > 1 and parts[0][0:2] != b"--":
            match = rx.search(parts[1])
            if match:
                key = match.group(1)

                # Continue parsing until we see just a line with CRLF
                ar = parts[2:]
                for i, ele in enumerate(ar):
                    if ele == CRLF:
                        value = b"".join(parts[3 + i:])

                        # Remove CRLF preceding the next boundary
                        length = len(value)
                        if value[length - 2:] == CRLF:
                            value = value[0:length - 2]

                        r.append((key, value))
                        break
    return r