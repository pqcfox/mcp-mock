# mcp-mock
Mock version of the Radical MCP for demo development.

# Installation
Run `pipenv install --dev`.

# Usage
To use, run `mcp-mock/mcp.py 1337` to start the server. To use the demo client, run `mcp-mock/mcp_client.py` in a separate server. Inside the client, `help` can be used to get information on commands.

# Development
To regenerate the protocol buffer interface (`mcp-mock/mcp_pb2.py`), run `build-proto.sh` in the main directory. Note that you must have `protoc` version 3.20 or later. Installation instructions [are here](https://github.com/protocolbuffers/protobuf/blob/main/src/README.md). 
