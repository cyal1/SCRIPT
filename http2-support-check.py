#!/usr/bin/env python3

"""
https://python-hyper.org/projects/h2/en/stable/plain-sockets-example.html
plain_sockets_client.py
~~~~~~~~~~~~~~~~~~~~~~~

Just enough code to send a GET request via h2 to an HTTP/2 server and receive a response body.
This is *not* a complete production-ready HTTP/2 client!
"""

import socket
import sys
import logging
import ssl
import certifi
import concurrent.futures
import h2.connection
import h2.events
from urllib3.util import parse_url
from h2.connection import H2Connection
from h2.events import (
    ResponseReceived, DataReceived, StreamEnded, StreamReset,
    SettingsAcknowledged,
)


class HttpStruct:
    _headers: list = None
    _data: bytes = b''

    def getHeaders(self):
        return self._headers

    def getData(self):
        return self._data

    def setHeaders(self, headers):
        self._headers = headers

    def setData(self, data):
        self._data = data

    def __str__(self) -> str:
        return f"<HttpStruct>{dict({'headers': self._headers, 'data': self._data})}"


def establish_tcp_connection(host, port, timeout=15):
    """
    This function establishes a client-side TCP connection. How it works isn't
    very important to this example. For the purpose of this example we connect
    to localhost.
    """
    socket.setdefaulttimeout(timeout)
    return socket.create_connection((host, port))


def get_http2_ssl_context():
    """
    This function creates an SSLContext object that is suitably configured for
    HTTP/2. If you're working with Python TLS directly, you'll want to do the
    exact same setup as this function does.
    """
    # Get the basic context from the standard library.
    ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)

    # RFC 7540 Section 9.2: Implementations of HTTP/2 MUST use TLS version 1.2
    # or higher. Disable TLS 1.1 and lower.
    ctx.options |= (
            ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    )

    # RFC 7540 Section 9.2.1: A deployment of HTTP/2 over TLS 1.2 MUST disable
    # compression.
    ctx.options |= ssl.OP_NO_COMPRESSION

    # RFC 7540 Section 9.2.2: "deployments of HTTP/2 that use TLS 1.2 MUST
    # support TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256". In practice, the
    # blocklist defined in this section allows only the AES GCM and ChaCha20
    # cipher suites with ephemeral key negotiation.
    ctx.set_ciphers("ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20")

    # We want to negotiate using NPN and ALPN. ALPN is mandatory, but NPN may
    # be absent, so allow that. This setup allows for negotiation of HTTP/1.1.
    ctx.set_alpn_protocols(["h2", "http/1.1"])

    try:
        ctx.set_npn_protocols(["h2", "http/1.1"])
    except NotImplementedError:
        pass

    return ctx


def negotiate_tls(tcp_conn, context, host, http2_prior_knowledge=False):
    """
    Given an established TCP connection and a HTTP/2-appropriate TLS context,
    this function:

    1. wraps TLS around the TCP connection.
    2. confirms that HTTP/2 was negotiated and, if it was not, throws an error.
    """
    # Note that SNI is mandatory for HTTP/2, so you *must* pass the
    # server_hostname argument.
    tls_conn = context.wrap_socket(tcp_conn, server_hostname=host)

    # Always prefer the result from ALPN to that from NPN.
    # You can only check what protocol was negotiated once the handshake is
    # complete.

    if not http2_prior_knowledge:
        negotiated_protocol = tls_conn.selected_alpn_protocol()
        if negotiated_protocol is None:
            negotiated_protocol = tls_conn.selected_npn_protocol()
        if negotiated_protocol != "h2":
            raise RuntimeError(
                "Server didn't negotiate HTTP/2, if you know the server supports HTTP/2, set http2_prior_knowledge=True to skip negotiate.")

    return tls_conn


def request(method: str, url: str, headers: list[tuple[str, str]] = None, body: bytes = None,
            http2_prior_knowledge=False,
            normalize=True,
            validate=True,
            timeout: int = 10) -> HttpStruct:
    u = parse_url(url.strip())
    host = u.host
    port = u.port if u.port is not None else 443
    path = u.path if u.path is not None else '/'

    resp_seq = {}

    if headers is None:
        headers = [
            (':method', method),
            (':path', path),
            (':authority', host),
            (':scheme', 'https'),
        ]
        if body is not None:
            headers.append(("content-length", str(len(body))))

    # Step 1: Set up your TLS context.
    context = get_http2_ssl_context()
    # context.verify_mode = ssl.CERT_NONE

    # Step 2: Create a TCP connection.
    connection = establish_tcp_connection(host, port, timeout=timeout)

    # Step 3: Wrap the connection in TLS and validate that we negotiated HTTP/2
    tls_connection = negotiate_tls(connection, context, host, http2_prior_knowledge=http2_prior_knowledge)

    # Step 4: Create a client-side H2 connection.
    config = h2.connection.H2Configuration()
    config.validate_outbound_headers = validate
    config.normalize_outbound_headers = normalize
    config.validate_inbound_headers = validate
    http2_connection = H2Connection(config=config)

    # Step 5: Initiate the connection
    http2_connection.initiate_connection()

    if body is None:
        http2_connection.send_headers(stream_id=1, headers=headers, end_stream=True)
        resp_seq[1] = HttpStruct()
    else:
        http2_connection.send_headers(stream_id=1, headers=headers)
        http2_connection.send_data(stream_id=1, data=body, end_stream=True)
        resp_seq[1] = HttpStruct()
    tls_connection.sendall(http2_connection.data_to_send())
    response_stream_ended = False

    while not response_stream_ended:
        # read raw data from the socket
        # print("before receive data")
        data = tls_connection.recv(65536 * 1024)
        # print("after receive data before")

        if not data:
            logging.error("%s no data receive" % url)
            break

        # feed raw data into h2, and process resulting events
        events = http2_connection.receive_data(data)
        for event in events:
            # print(event)
            if isinstance(event, ResponseReceived):
                # resp_headers = event.headers
                resp_seq[event.stream_id].setHeaders(event.headers)

            elif isinstance(event, DataReceived):
                # update flow control so the server doesn't starve us
                http2_connection.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                # more response body data received
                # resp_body += event.data
                resp_seq[event.stream_id].setData(resp_seq[event.stream_id].getData() + event.data)
            elif isinstance(event, StreamEnded):
                # response body completed, let's exit the loop
                response_stream_ended = True
                break
            elif isinstance(event, SettingsAcknowledged):
                """
                Called when the remote party ACKs our settings. We send a SETTINGS
                frame as part of the preamble, so if we want to be very polite we can
                wait until the ACK for that frame comes before we start sending our
                request.
                """
                pass

            elif isinstance(event, StreamReset):
                logging.error("%s <StreamId: %d>: %s" % (url, event.stream_id, event.error_code))
                http2_connection.close_connection()
                tls_connection.close()
                return resp_seq[event.stream_id]
                # print(event.error_code)
                # raise RuntimeError("Stream reset: %d" % event.error_code)

        # send any pending data to the server
        tls_connection.sendall(http2_connection.data_to_send())

    # tell the server we are closing the h2 connection
    http2_connection.close_connection()
    tls_connection.sendall(http2_connection.data_to_send())

    # close the socket
    tls_connection.close()

    # print(resp_body)
    return resp_seq[1]


def load_url(url):
    return request("GET", url=url, timeout=15, http2_prior_knowledge=True)


if sys.stdin.isatty():
    print("""
Usage:
    echo https://www.baidu.com/ | python3 http2-support-check.py
    cat urls.txt | python3 http2-support-check.py
        """)
    exit()


# with open(sys.argv[1]) as f:
#     url_list = f.readlines()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers = 50) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url.strip()): url.strip() for url in sys.stdin}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result() 
        except Exception as exc:
            logging.warning("%s: %s" % (url, exc))
            # print('%r generated an exception: %s' % (url, exc))
        else:
            if data.getHeaders() is not None:
                print(url)
