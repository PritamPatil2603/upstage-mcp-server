# Upstage MCP Server

> A Model Context Protocol (MCP) server for Upstage AI's document digitization and information extraction capabilities

## 📋 Overview

The Upstage MCP Server provides a bridge between AI assistants and Upstage AI's powerful document processing APIs. This server enables AI models like Claude to seamlessly extract and structure content from various document types including PDFs, images, and Office files.

## ✨ Key Features

- **Document Digitization**: Extract structured content from documents while preserving layout
- **Information Extraction**: Extract specific data points based on intelligent schemas
- **Multi-format Support**: Process PDFs, images (JPEG, PNG, TIFF)
- **Claude Desktop Integration**: Seamless integration with Claude and other MCP clients

## 🔑 Prerequisites

Before using this server, you'll need:

1. **Upstage API Key**: Obtain your API key from [Upstage AI](https://console.upstage.ai/api-keys?api=chat)
2. **Python 3.10+**: The server requires Python 3.10 or higher
3. **uv package manager**: For dependency management and installation.

## 🚀 Local/Dev Setup Instructions

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/PritamPatil2603/upstage-mcp-server.git

# Navigate to the project directory
cd upstage-mcp-server
```

### Step 2: Set Up Python Environment

```bash
# Install uv if not already installed
pip install uv

# Create and activate a virtual environment using uv
uv venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies in editable mode
uv pip install -e .
```

### Step 3: Set Up API Key

Either set it as an environment variable:

```bash
# Windows
set UPSTAGE_API_KEY=your_api_key_here

# macOS/Linux
export UPSTAGE_API_KEY=your_api_key_here
```

Or you can add API key in below claude desktop config file.

### Step 4: Configure Claude Desktop

Open Claude Desktop, then navigate to **Claude → Settings → Developer → Edit Config** and add the following to the `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "upstage-document-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\path\\to\\cloned\\upstage-mcp-server",
        "python",
        "-m",
        "upstage_mcp.server"
      ],
      "env": {
        "UPSTAGE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

> **Note:** Replace the path with your actual repository path. On macOS/Linux, use forward slashes (`/`) in the path.

## 🛠️ Available Tools

The server exposes two main tools to AI models:

### 1. Document Parsing (`parse_document`)

Processes documents and extracts their content with layout preservation.

**Parameters:**

- **file_path**: Path to the document file to be processed

**Example Query to Claude:**

> "Can you parse this document located at `C:\Users\username\Documents\contract.pdf` and summarize its contents?"

### 2. Information Extraction (`extract_information`)

Extracts structured information from documents according to schemas.

**Parameters:**

- **file_path**: Path to the document file to process
- **schema_path** (optional): Path to JSON file containing extraction schema
- **auto_generate_schema** (default: true): Whether to automatically generate a schema

**Example Query to Claude:**

> "Extract the invoice number, date, and total amount from this document at `C:\Users\username\Documents\invoice.pdf`."

## 📂 Output Files

The server saves processing results in the following locations:

- **Document Parsing Results:** `upstage_mcp/outputs/document_parsing/`
- **Information Extraction Results:** `upstage_mcp/outputs/information_extraction/`
- **Generated Schemas:** `upstage_mcp/outputs/information_extraction/schemas/`

## 🔧 Troubleshooting

### Common Issues

- **API Key Not Found:**  
  Ensure your Upstage API key is properly set in your environment variables or included in a `.env` file.
  
- **File Not Found:**  
  Verify that the file path provided is correct and accessible by the server.
  
- **Server Not Starting:**  
  Check if you've activated the virtual environment and installed all dependencies.

### Checking Logs

You can find Claude Desktop logs at the following locations:

- **Windows:** `%APPDATA%\Claude\logs\mcp-server-upstage-document-parser.log`
- **macOS:** `~/Library/Logs/Claude/mcp-server-upstage-document-parser.log`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request with your enhancements.


