#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Radical Main Control Program test client.
"""

import base64
import cmd
import socket
import struct
import sys

import mcp_pb2


def _receive_data(sock, size):
    data = b""
    while len(data) < size:
        data += sock.recv(size - len(data))
    return data


class MCPClientShell(cmd.Cmd):
    """A client shell for the Radical MCP."""
    intro = "Type 'help' for information on commands."
    prompt = ">>> "

    def __init__(self):
        super().__init__()
        self.usage = None
        self.port = 1337

    def do_port(self, arg):
        """Change the port number:  port <port>"""
        new_port = int(arg)
        print(f"Port changed from {self.port} to {new_port}.")
        self.port = new_port

    def do_quit(self, _arg):
        """Exit the prompt:  exit"""
        sys.exit()

    def _run_command(self, command, response_cls):
        # connect to the MCP
        mcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mcp_sock.connect(("localhost", self.port))

        # serialize and frame the command
        command_data = command.SerializeToString()
        command_len = struct.pack(">L", len(command_data))

        # send the result
        mcp_sock.sendall(command_len + command_data)

        # receive response length
        len_data = _receive_data(mcp_sock, 4)
        (response_len,) = struct.unpack(">L", len_data)

        # receive response
        response_data = _receive_data(mcp_sock, response_len)

        # deserialize response
        response = response_cls().FromString(response_data)
        return response

    def do_reset(self, _arg):
        """Reset the development board:  reset"""
        command = mcp_pb2.Command(reset=mcp_pb2.ResetCommand())
        self._run_command(command, mcp_pb2.ResetResponse)
        print("Reset complete.")

    def do_diagnostic(self, arg):
        """Perform a diagnostic test:  diagnostic 4"""
        diagnostic_num = int(arg)
        command = mcp_pb2.Command(
            diagnostic=mcp_pb2.DiagnosticCommand(diagnostic=diagnostic_num)
        )
        response = self._run_command(command, mcp_pb2.DiagnosticResponse)
        if response.success:
            print("Diagnostic passed.")
            self.usage = response.usage
        else:
            print(f"Diagnostic failed with error: \"{response.error}\".")

    def do_key(self, arg):
        """Store a key in a key slot:  key 3 3dy54..."""
        arg_vals = arg.split()
        slot, key_data = int(arg_vals[0]), base64.b64decode(arg_vals[1])
        command = mcp_pb2.Command(
            key=mcp_pb2.KeyCommand(key_data, slot)
        )
        response = self._run_command(command, mcp_pb2.KeyResponse)
        if response.success:
            print("Key storage succeeded.")
            self.usage = response.usage
        else:
            print("Key storage failed.")

    def do_inject(self, args):
        """HCI inject a written key into a slot: inject 4"""
        slot = int(args)
        command = mcp_pb2.Command(
            key=mcp_pb2.KeyInjectCommand(slot)
        )
        response = self._run_command(command, mcp_pb2.KeyInjectResponse)
        if response.success:
            print("Key injection succeeded.")
            self.usage = response.usage
        else:
            print("Key injection failed.")

    def do_ntt(self, args):
        """Perform an NTT on data: ntt 5xo9c..."""
        poly = [int(coeff) for coeff in args.split()]
        command = mcp_pb2.Command(
            key=mcp_pb2.KyberNTTCommand(poly)
        )
        response = self._run_command(command, mcp_pb2.KyberNTTResponse)


    def do_usage(self, _args):
        """Print usage of the last command:  usage"""
        if self.usage is None:
            print("Previous command did not have usage data.")
        else:
            print("Command took:")
            print(f"    {int(self.usage.cycles)} cycles")
            print(f"    {self.usage.seconds} seconds")
            print(f"    {self.usage.power_io} mW on the IO line")
            print(f"    {self.usage.power_hci} mW on the HCI line")
            print(f"    {self.usage.power_main} mW on the main line")
            print(f"    {self.usage.power_core} mW on the core line")

    def precmd(self, line):
        """Clear usage before every command."""
        if line.strip() != 'usage':
            self.usage = None
        return line





if __name__ == "__main__":
    MCPClientShell().cmdloop()
