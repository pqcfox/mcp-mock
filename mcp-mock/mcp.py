#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Radical Main Control Program.
"""

import random
import socket
import struct
import sys

import mcp_pb2
import util
import saber
import kyber


def generate_usage_data():
    """Generate fake usage data."""
    return mcp_pb2.UsageData(
        cycles=random.randrange(1000, 100000),
        seconds=random.random() * 0.1,
        power_io=random.random(),
        power_hci=random.random(),
        power_main=random.random(),
        power_core=random.random(),
    )


def handle_reset(_reset_command):
    """Handle a reset command."""
    print("Resetting chip...")
    return mcp_pb2.ResetResponse()


def handle_diagnostic(diagnostic_command):
    """Handle a diagnostic run command."""
    print(f"Performing diagnostic #{diagnostic_command.diagnostic}...")
    success = random.random() < 0.8
    return mcp_pb2.DiagnosticResponse(
        success=success,
        error="" if success else "Something went wrong!",
        usage=generate_usage_data(),
    )


def handle_key(key_command):
    """Handle a key storage command."""
    print("Storing key in slot #{key_command.slot_num}...")
    success = random.random() < 0.8
    return mcp_pb2.KeyResponse(success=success, usage=generate_usage_data())


def handle_inject(inject_command):
    """Handle a key injection command."""
    print("Injecting key in slot #{inject_command.slot_num}...")
    success = random.random() < 0.8
    return mcp_pb2.KeyResponse(success=success, usage=generate_usage_data())


def handle_ntt(ntt_command):
    print("Performing NTT...")
    result = kyber.ntt(list(ntt_command.poly))
    return mcp_pb2.KyberNTTResponse(result=result, usage=generate_usage_data())


# TODO: write!
def handle_secret_ntt(secret_command):
    print("Performing Dilithium NTT on secret...")


# TODO: make this 13 OR 10 bits
def handle_sbm(sbm_command):
    print("Performing SBM...")
    result = saber.sbm(
        list(sbm_command.poly_a),
        list(sbm_command.poly_b),
        mod=2**10 if sbm_command.post_round else 2**13,
    )
    return mcp_pb2.SaberSBMResponse(
        result=result,
        usage=generate_usage_data(),
    )


def handle_keygen(keygen_command):
    print("Generating key in slot #{keygen_command.slot_num}")
    return mcp_pb2.KeygenResponse()


command_handlers = {
    "reset": handle_reset,
    "diagnostic": handle_diagnostic,
    "key": handle_key,
    "inject": handle_inject,
    "ntt": handle_ntt,
    "sbm": handle_sbm,
    "keygen": handle_keygen,
}


def main():
    mcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mcp_sock.bind(("localhost", int(sys.argv[1])))
    mcp_sock.listen(1)

    while True:
        # create a connection
        (client_sock, _) = mcp_sock.accept()

        # receive command length
        command_data = util.receive_length_prefix_data(client_sock)

        # get command
        command = mcp_pb2.Command().FromString(command_data)
        command_type = command.WhichOneof("command")
        real_command = getattr(command, command_type)

        # make response
        response = command_handlers[command_type](real_command)
        response_data = response.SerializeToString()

        # send response
        util.send_length_prefix_data(client_sock, response_data)


if __name__ == "__main__":
    main()
