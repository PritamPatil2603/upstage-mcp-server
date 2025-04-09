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

1. **Upstage API Key**: Obtain your API key from [API](https://console.upstage.ai/api-keys?api=document-parsing)
2. **Python 3.10+**: The server requires Python 3.10 or higher.
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

# Create and activate a virtual environment
uv venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies in editable mode
uv pip install -e .
```

### Step 3: Set Up API Key

You can set the Upstage API key in two ways:

1. **Using Environment Variables:**

   ```bash
   # On Windows
   set UPSTAGE_API_KEY=your_api_key_here

   # On macOS/Linux
   export UPSTAGE_API_KEY=your_api_key_here
   ```

2. Add Upstage API key directly in the below claude_desktop_config.json file.

### Step 4: Configure Claude Desktop

1. **Download Claude Desktop:**
   - [Download Claude Desktop](https://claude.ai/download)

2. **Open Claude Desktop:**
   - Navigate to **Claude → Settings → Developer → Edit Config**

3. **Edit `claude_desktop_config.json`:**

   Add the following configuration:

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

   Replace the `C:\\path\\to\\cloned\\upstage-mcp-server` with the actual repository path. (Use forward slashes `/` if you are on macOS/Linux.)

4. **Restart Claude Desktop**

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

- **Windows:** `%APPDATA%\Claude\logs\mcp-server-upstage-document-parser.log`
- **macOS:** `~/Library/Logs/Claude/mcp-server-upstage-document-parser.log`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request to enhance the project or add new features.

## 📄 License

This project is licensed under the MIT License.
