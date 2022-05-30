#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Radical Main Control Program test client.
"""

import socket
import struct
import sys

from mcp_pb2 import Command, ResetCommand, ResetResponse

# connect to the MCP
mcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mcp_sock.connect(("localhost", int(sys.argv[1])))

# make command
command = Command(reset=ResetCommand())
command_data = command.SerializeToString()

# send command
command_len = struct.pack(">L", len(command_data))
mcp_sock.sendall(command_len + command_data)

# receive response length
response_len_data = b""
while len(response_len_data) < 4:
    response_len_data += mcp_sock.recv(4 - len(response_len_data))
(response_len,) = struct.unpack(">L", response_len_data)

# receive response
response_data = b""
while len(response_data) < response_len:
    response_data += mcp_sock.recv(response_len - len(response_data))

# get response
response = ResetResponse().FromString(response_data)
print(response)
print(type(response))
