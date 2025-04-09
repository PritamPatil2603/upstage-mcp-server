# Upstage Document Parser MCP Server

A Model Context Protocol server for parsing documents using Upstage AI's document digitization API.

## Features

* Extract structured content from documents (PDF, DOCX, images, etc.)
* Saves full API responses for reference
* Simple integration with Claude Desktop and other MCP clients

## Installation

### Using uvx (recommended)

```bash
uvx upstage-mcp-server
```

### Using pip

```bash
pip install upstage-mcp-server
```

## Configuration

You'll need an Upstage AI API key. Set it as an environment variable:

```bash
# Windows
set UPSTAGE_API_KEY=your_api_key_here

# Linux/macOS
export UPSTAGE_API_KEY=your_api_key_here
```

## Usage with Claude Desktop

Add this to your claude_desktop_config.json:

```json
{
  "mcpServers": {
    "upstage-document-parser": {
      "command": "uvx",
      "args": ["upstage-mcp-server"],
      "env": {
        "UPSTAGE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### parse_document

Parse a document using Upstage AI's document digitization API.

Inputs:
- file_path (string): Path to the document file to be processed

Returns:
Structured document content with formatting and a note about where the full API response is saved

## License

This MCP server is licensed under the MIT License.

