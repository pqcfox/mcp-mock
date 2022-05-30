#!/usr/bin/env bash

protoc -I mcp-mock/ --python_out mcp-mock/ mcp-mock/mcp.proto
