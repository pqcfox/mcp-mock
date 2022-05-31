"""Utilities shared between MCP client and server."""

import struct


def receive_data(sock, size):
    """Receive a fixed length of data over a socket."""
    data = b""
    while len(data) < size:
        data += sock.recv(size - len(data))
    return data


def receive_length_prefix_data(sock):
    """Receive length-prefixed data over a socket."""
    # receive data length
    data_len_data = receive_data(sock, 4)
    (data_len,) = struct.unpack(">L", data_len_data)

    # receive data itself
    data = receive_data(sock, data_len)
    while len(data) < data_len:
        data += sock.recv(data_len - len(data))

    return data


def send_length_prefix_data(sock, data):
    """Send length-prefixed data over a socket."""
    # make response length
    data_len = struct.pack(">L", len(data))

    # send length, then data
    sock.sendall(data_len + data)
