#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Radical Main Control Program test client.
"""

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
    intro = "Type 'help' for information on commands."
    prompt = ">>> "
    port = 1337

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
        """Perform a diagnostic test."""
        diagnostic_num = int(arg)
        command = mcp_pb2.Command(
            diagnostic=mcp_pb2.DiagnosticCommand(diagnostic=diagnostic_num)
        )
        response = self._run_command(command, mcp_pb2.DiagnosticResponse)
        if response.success:
            print("Diagnostic passed.")
        else:
            print(f"Diagnostic failed with error: \"{response.error}\".")


if __name__ == "__main__":
    MCPClientShell().cmdloop()
