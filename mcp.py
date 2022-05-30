#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Radical Main Control Program.
"""

import random
import socket
import struct
import sys

from mcp_pb2 import (
    Command,
    ResetResponse,
    DiagnosticResponse,
    KeyResponse,
    KeyInjectResponse,
    KyberNTTResponse,
    SaberSBMResponse,
    KeygenResponse,
    EncapsulateResponse,
    DecapsulateResponse,
    SignResponse,
    VerifyResponse,
    EncryptResponse,
    DecryptResponse,
    UsageData,
)


def generate_usage_data():
    return UsageData(
        cycles=random.randrange(1000, 100000),
        seconds=random.random() * 0.1,
        power_io=random.random(),
        power_hci=random.random(),
        power_main=random.random(),
        power_core=random.random(),
    )


def handle_reset(_reset_command):
    print("Resetting chip...")
    return ResetResponse()


def handle_diagnostic(diagnostic_command):
    print(f"Performing diagnostic #{diagnostic_command.diagnositc}...")
    success = (random.random() > 0.8)
    return DiagnosticResponse(
        success=success,
        error="" if success else "Something went wrong!",
        usage=generate_usage_data()
    )


def handle_key(key_command):
    pass


def handle_inject():
    pass


def handle_ntt():
    pass


def handle_sbm():
    pass


def handle_keygen():
    pass


def handle_encaps():
    pass


def handle_decaps():
    pass


def handle_sign():
    pass


def handle_verify():
    pass


def handle_encrypt():
    pass


def handle_decrypt():
    pass


command_handlers = {
    "reset": handle_reset,
    "diagnostic": handle_diagnostic,
    "key": handle_key,
    "inject": handle_inject,
    "ntt": handle_ntt,
    "sbm": handle_sbm,
    "keygen": handle_keygen,
    "encaps": handle_encaps,
    "decaps": handle_decaps,
    "sign": handle_sign,
    "verify": handle_verify,
    "encrypt": handle_encrypt,
    "decrypt": handle_decrypt,
}


def main():
    mcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mcp_sock.bind(("localhost", int(sys.argv[1])))
    mcp_sock.listen(1)

    while True:
        # create a connection
        (client_sock, address) = mcp_sock.accept()

        # receive command length
        command_len_data = b''
        while len(command_len_data) < 4:
            command_len_data += client_sock.recv(4 - len(command_len_data))
        (command_len,) = struct.unpack('>L', command_len_data)

        # receive command data
        command_data = b''
        while len(command_data) < command_len:
            command_data += client_sock.recv(command_len - len(command_data))

        # get command
        command = Command().FromString(command_data)
        command_type = command.WhichOneof("command")
        real_command = getattr(command, command_type)

        # make response
        response = command_handlers[command_type](real_command)
        response_data = response.SerializeToString()

        # send response
        response_len = struct.pack('>L', len(response_data))
        client_sock.sendall(response_len + response_data)


if __name__ == "__main__":
    main()
