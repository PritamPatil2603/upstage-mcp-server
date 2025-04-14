```markdown
# Upstage MCP Server

> A Model Context Protocol (MCP) server for Upstage AI's document digitization and information extraction capabilities

## Overview

The Upstage MCP Server provides a robust bridge between AI assistants and Upstage AI’s powerful document processing APIs. This server enables AI models—such as Claude—to effortlessly extract and structure content from various document types including PDFs, images, and Office files. The package supports multiple formats and comes with seamless integration options for Claude Desktop.

## Key Features

- **Document Digitization:** Extract structured content from documents while preserving layout.
- **Information Extraction:** Retrieve specific data points using intelligent, customizable schemas.
- **Multi-format Support:** Handles JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, and XLSX.
- **Claude Desktop Integration:** Effortlessly connect with Claude and other MCP clients.

## Prerequisites

Before using this server, ensure you have the following:

1. **Upstage API Key:** Obtain your API key from [Upstage API](https://console.upstage.ai/api-keys?api=document-parsing).
2. **Python 3.10+:** The server requires Python version 3.10 or higher.
3. **uv Package Manager:** For dependency management and execution. Install it via:
   ```bash
   pip install uv
   ```

## Installation Options

### Using uv (Recommended)

`uvx` streamlines execution, so no additional installation is required in most cases. For a direct installation via uv:

```bash
uv pip install upstage-mcp-server
```

Alternatively, execute directly with `uvx`:

```bash
uvx upstage-mcp-server
```

### Using pip

To install directly from PyPI:

```bash
pip install upstage-mcp-server
```

## Configure Claude Desktop

To integrate with Claude Desktop, update your `claude_desktop_config.json` accordingly.

### Configuration Location

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

### Option 1: Using uvx Command (Recommended)

```json
{
  "mcpServers": {
    "upstage-mcp-server": {
      "command": "uvx",
      "args": ["upstage-mcp-server"],
      "env": {
        "UPSTAGE_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

### Option 2: Using the Python Module

```json
{
  "mcpServers": {
    "upstage-mcp-server": {
      "command": "python",
      "args": ["-m", "upstage_mcp.server"],
      "env": {
        "UPSTAGE_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

After applying the configuration, restart Claude Desktop for the changes to take effect.

## Output Directories

Processing results are stored in your home directory under:

- **Document Parsing Results:**  
  `~/.upstage-mcp-server/outputs/document_parsing/`
- **Information Extraction Results:**  
  `~/.upstage-mcp-server/outputs/information_extraction/`
- **Generated Schemas:**  
  `~/.upstage-mcp-server/outputs/information_extraction/schemas/`

## Local/Development Setup

Follow these steps to set up and run the project locally:

### Step 1: Clone the Repository

```bash
git clone https://github.com/PritamPatil2603/upstage-mcp-server.git
cd upstage-mcp-server
```

### Step 2: Set Up the Python Environment

```bash
# Install uv if not already installed
pip install uv

# Create and activate a virtual environment
uv venv

# Activate the virtual environment
# On Windows:
# .venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies in editable mode
uv pip install -e .
```

### Step 3: Configure Claude Desktop for Local Testing

1. **Download Claude Desktop:**  
   [Download Claude Desktop](https://claude.ai/download)

2. **Open and Edit Configuration:**
   - Navigate to **Claude → Settings → Developer → Edit Config**.
   - Edit the `claude_desktop_config.json` file with the following configurations:

   **For Windows:**
   ```json
   {
     "mcpServers": {
       "upstage-mcp-server": {
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
   Replace `C:\\path\\to\\cloned\\upstage-mcp-server` with your actual repository path.

   **For macOS/Linux:**
   ```json
   {
     "mcpServers": {
       "upstage-mcp-server": {
         "command": "/Users/username/.local/bin/uv",
         "args": [
           "run",
           "--directory",
           "/path/to/cloned/upstage-mcp-server",
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
   Replace:
   - `/Users/username/.local/bin/uv` with the output of `which uv`.
   - `/path/to/cloned/upstage-mcp-server` with the absolute path to your local clone.

> **Tip for macOS/Linux users:** If connection issues occur, using the full path to your uv executable can improve reliability.

After configuring, restart Claude Desktop.

## Available Tools

The server exposes two primary tools for AI models:

1. **Document Parsing (`parse_document`):**
   - **Description:** Processes documents and extracts content while preserving structure.
   - **Parameter:**  
     `file_path` – the path to the document to be processed.
   - **Example Query:**  
     *"Can you parse the document at `C:\Users\username\Documents\contract.pdf` and provide a summary?"*

2. **Information Extraction (`extract_information`):**
   - **Description:** Extracts structured information from documents based on predefined or auto-generated schemas.
   - **Parameters:**  
     `file_path` – the document file path;  
     `schema_path` (optional) – a JSON file with an extraction schema;  
     `auto_generate_schema` (default true) – whether to auto-generate a schema.
   - **Example Query:**  
     *"Extract the invoice number, date, and total from `C:\Users\username\Documents\invoice.pdf`."*

## Output Files

Processed outputs are saved at:

- **Document Parsing Results:** `~/.upstage-mcp-server/outputs/document_parsing/`
- **Information Extraction Results:** `~/.upstage-mcp-server/outputs/information_extraction/`
- **Generated Schemas:** `~/.upstage-mcp-server/outputs/information_extraction/schemas/`

## Troubleshooting

### Common Issues

- **API Key Missing:**  
  Ensure that your Upstage API key is set in the environment variables or in a `.env` file.
- **File Not Found:**  
  Double-check the file path for correctness and accessibility.
- **Server Not Starting:**  
  Verify that your virtual environment is activated and all dependencies are installed.

### Log Files

For troubleshooting, view the server logs at:

- **Windows:**  
  `%APPDATA%\Claude\logs\mcp-server-upstage-mcp-server.log`
- **macOS:**  
  `~/Library/Logs/Claude/mcp-server-upstage-mcp-server.log`

## Contributing

Contributions are welcome! If you wish to enhance the project or add new features, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
```
