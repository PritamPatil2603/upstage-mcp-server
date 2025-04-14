# Upstage MCP Server

> A Model Context Protocol (MCP) server for Upstage AI's document digitization and information extraction capabilities

## 📋 Overview

The Upstage MCP Server provides a bridge between AI assistants and Upstage AI's powerful document processing APIs. This server enables AI models like Claude to seamlessly extract and structure content from various document types including PDFs, images, and Office files.

## ✨ Key Features

- **Document Digitization**: Extract structured content from documents while preserving layout.
- **Information Extraction**: Extract specific data points based on intelligent schemas.
- **Multi-format Support**: JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX.
- **Claude Desktop Integration**: Seamless integration with Claude and other MCP clients.

## 🔑 Prerequisites

Before using this server, you'll need:

1. **Upstage API Key**: Obtain your API key from [Upstage API](https://console.upstage.ai/api-keys?api=document-parsing)
2. **Python 3.10+**: The server requires Python 3.10 or higher.
3. **uv package manager**: For dependency management and installation.

```markdown
## Installation Options

### Using pip

Install directly from PyPI:

```bash
pip install upstage-mcp-server
```

### Using `uv` (Recommended)

If you're using UV as your Python package manager:

```bash
uv pip install upstage-mcp-server
```

Or execute directly with `uvx`:

```bash
uvx upstage-mcp-server
```

## Configure Claude Desktop

For integration with Claude Desktop, add the following configuration to your `claude_desktop_config.json`:

**Location:**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

### Option 1: Using `uvx` Command (Recommended)

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

### Option 2: Using Python Module

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

After updating the configuration, restart Claude Desktop for the changes to take effect.

## Output Directories

The package saves processing results in these locations in your home directory:

- **Document Parsing Results:** `~/.upstage-mcp-server/outputs/document_parsing/`
- **Information Extraction Results:** `~/.upstage-mcp-server/outputs/information_extraction/`
- **Generated Schemas:** `~/.upstage-mcp-server/outputs/information_extraction/schemas/`


## 🚀 Local/Dev Setup Instructions
```
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

# Create and activate a virtual environment
uv venv

# Activate the virtual environment
# On Windows, run:
# .venv\Scripts\activate
# On macOS/Linux, run:
source .venv/bin/activate

# Install dependencies in editable mode
uv pip install -e .
```

### Step 3: Configure Claude Desktop

1. **Download Claude Desktop:**
   - [Download Claude Desktop](https://claude.ai/download)

2. **Open Claude Desktop:**
   - Navigate to **Claude → Settings → Developer → Edit Config**


3. **Edit `claude_desktop_config.json`:**

   Add the following configuration:

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

Replace the `C:\\path\\to\\cloned\\upstage-mcp-server` with the actual repository path on your system.

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

   Replace the following:
   - `/Users/username/.local/bin/uv` with the full path to your uv executable (find it using `which uv`)
   - `/path/to/cloned/upstage-mcp-server` with the absolute path to your repository

   > **Tip for macOS/Linux users:** If you're experiencing connection issues, using the full path to the uv executable is often more reliable than just `uv`. Find the path using `which uv` in your terminal.

4. **Once above  steps are completed, please restart Claude Desktop**


## 🛠️ Available Tools

The server exposes two main tools for AI models:

1. **Document Parsing (`parse_document`):**
   - **Description**: Processes documents and extracts their content with structure preservation.
   - **Parameters**:
     - `file_path`: Path to the document file to be processed.
   - **Example Query to Claude:**
     > Can you parse this document located at "C:\Users\username\Documents\contract.pdf" and summarize its contents?

2. **Information Extraction (`extract_information`):**
   - **Description**: Extracts structured information from documents according to schemas.
   - **Parameters**:
     - `file_path`: Path to the document file to process.
     - `schema_path` (optional): Path to a JSON file containing the extraction schema.
     - `auto_generate_schema` (default: true): Whether to automatically generate a schema.
   - **Example Query to Claude:**
     > Extract the invoice number, date, and total amount from this document at "C:\Users\username\Documents\invoice.pdf".

## 📂 Output Files

The server saves processing results in these locations:

- **Document Parsing Results:** `upstage_mcp/outputs/document_parsing/`
- **Information Extraction Results:** `upstage_mcp/outputs/information_extraction/`
- **Generated Schemas:** `upstage_mcp/outputs/information_extraction/schemas/`

## 🔧 Troubleshooting

### Common Issues

- **API Key Not Found:**  
  Ensure your Upstage API key is correctly set in environment variables or the `.env` file.
  
- **File Not Found:**  
  Verify that the file path is correct and accessible to the server.
  
- **Server Not Starting:**  
  Check if you've activated the virtual environment and installed all dependencies.

### Checking Logs

Claude Desktop logs can be found at:

- **Windows:** `%APPDATA%\Claude\logs\mcp-server-upstage-mcp-server.log`
- **macOS:** `~/Library/Logs/Claude/mcp-server-upstage-mcp-server.log`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request to enhance the project or add new features.

## 📄 License

This project is licensed under the MIT License.
