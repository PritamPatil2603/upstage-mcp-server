"""MCP server for Upstage AI services."""

import os
import json
import base64
import mimetypes
from pathlib import Path
from typing import Annotated, Any, Optional, Dict, Union, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from pydantic import Field

# Load environment variables
load_dotenv()

# API Endpoints
DOCUMENT_DIGITIZATION_URL = "https://api.upstage.ai/v1/document-digitization"
INFORMATION_EXTRACTION_URL = "https://api.upstage.ai/v1/information-extraction"
SCHEMA_GENERATION_URL = "https://api.upstage.ai/v1/information-extraction/schema-generation"
REQUEST_TIMEOUT = 300  # 5 minutes

# Configuration
API_KEY = os.environ.get("UPSTAGE_API_KEY")

if not API_KEY:
    raise ValueError("UPSTAGE_API_KEY not set in environment variables")

# Define response directories
package_dir = Path(__file__).parent
output_dir = package_dir / "outputs"
doc_parsing_dir = output_dir / "document_parsing"
info_extraction_dir = output_dir / "information_extraction"
schemas_dir = info_extraction_dir / "schemas"

# Create all directories
os.makedirs(doc_parsing_dir, exist_ok=True)
os.makedirs(info_extraction_dir, exist_ok=True)
os.makedirs(schemas_dir, exist_ok=True)
print(f"Output directories created at: {output_dir}")

# For backward compatibility
response_dir = doc_parsing_dir

# Create MCP server
mcp = FastMCP(
    "upstage-ai-tools", 
    dependencies=["mcp", "httpx", "python-dotenv"]
)

# Supported file formats for Information Extraction
SUPPORTED_EXTRACTION_FORMATS = {
    ".jpeg", ".jpg", ".png", ".bmp", ".pdf", ".tiff", ".tif", 
    ".heic", ".docx", ".pptx", ".xlsx"
}

# Utility functions
def encode_file_to_base64(file_path: str) -> str:
    """Encode a file to base64 string."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def validate_file_for_extraction(file_path: str) -> Optional[str]:
    """
    Validate that a file is suitable for information extraction.
    
    Returns an error message if validation fails, None otherwise.
    """
    if not os.path.exists(file_path):
        return f"File not found at {file_path}"
        
    # Check file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in SUPPORTED_EXTRACTION_FORMATS:
        return f"Unsupported file format: {file_ext}. Supported formats are: {', '.join(SUPPORTED_EXTRACTION_FORMATS)}"
        
    # Check file size (50MB limit)
    file_size = os.path.getsize(file_path)
    if file_size > 50 * 1024 * 1024:  # 50MB in bytes
        return f"File exceeds maximum size of 50MB. Current size: {file_size / (1024 * 1024):.2f}MB"
        
    return None


def load_schema(schema_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Load a schema from a JSON file."""
    if not schema_path:
        return None
        
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
    with open(schema_path, "r") as f:
        return json.load(f)


async def generate_schema(file_base64: str, mime_type: str, ctx: Context) -> Dict[str, Any]:
    """
    Generate a schema using the Schema Generation API.
    
    Args:
        file_base64: Base64 encoded file content
        mime_type: MIME type of the file
        ctx: MCP Context for progress reporting
    
    Returns:
        Generated schema for information extraction
    """
    ctx.info("Connecting to schema generation API")
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(REQUEST_TIMEOUT)) as client:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Convert mime_type to data URL format
        data_url_mime = mime_type.split('/')[0]
        if data_url_mime not in ["image", "application"]:
            data_url_mime = "image"  # Default to image for unrecognized types
            
        # Prepare request data in OpenAI format
        request_data = {
            "model": "information-extract",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{file_base64}"
                            }
                        }
                    ]
                }
            ]
        }
        
        # Make request
        response = await client.post(
            SCHEMA_GENERATION_URL,
            headers=headers,
            json=request_data
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract schema from response
        if "choices" not in result or len(result["choices"]) == 0:
            raise ValueError("Invalid response from schema generation API")
            
        content = result["choices"][0]["message"]["content"]
        schema = json.loads(content)
        
        if "json_schema" not in schema:
            raise ValueError("Invalid schema format returned")
            
        return schema["json_schema"]


async def extract_with_schema(file_base64: str, mime_type: str, schema: Dict[str, Any], ctx: Context) -> Dict[str, Any]:
    """
    Extract information using the Information Extraction API.
    
    Args:
        file_base64: Base64 encoded file content
        mime_type: MIME type of the file
        schema: JSON schema defining what to extract
        ctx: MCP Context for progress reporting
    
    Returns:
        Extracted information as a dictionary
    """
    ctx.info("Connecting to information extraction API")
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(REQUEST_TIMEOUT)) as client:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Convert mime_type to data URL format
        data_url_mime = mime_type.split('/')[0]
        if data_url_mime not in ["image", "application"]:
            data_url_mime = "image"  # Default to image for unrecognized types
            
        # Prepare request data in OpenAI format
        request_data = {
            "model": "information-extract",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{file_base64}"
                            }
                        }
                    ]
                }
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": schema
            }
        }
        
        # Make request
        response = await client.post(
            INFORMATION_EXTRACTION_URL,
            headers=headers,
            json=request_data
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract content from response
        if "choices" not in result or len(result["choices"]) == 0:
            raise ValueError("Invalid response from information extraction API")
            
        content = result["choices"][0]["message"]["content"]
        return json.loads(content)


# Document Parsing Tool
@mcp.tool()
async def parse_document(
    file_path: Annotated[str, Field(description="Path to the document file to be processed")],
    ctx: Context
) -> str:
    """Parse a document using Upstage AI's document digitization API.
    
    This tool extracts the structure and content from various document types,
    including PDFs, images, and Office files. It preserves the original formatting
    and layout while converting the document into a structured format.
    
    Supported file formats include: PDF, JPEG, PNG, TIFF, and other common document formats.
    """
    if not os.path.exists(file_path):
        ctx.error(f"File not found at {file_path}")
        return f"Error: File not found at {file_path}"
    
    try:
        ctx.info(f"Starting to process {file_path}")
        await ctx.report_progress(10, 100)
        
        # Initialize API client with timeout
        async with httpx.AsyncClient(timeout=httpx.Timeout(REQUEST_TIMEOUT)) as client:
            headers = {"Authorization": f"Bearer {API_KEY}"}
            
            await ctx.report_progress(30, 100)
            
            # Process document
            with open(file_path, "rb") as file:
                files = {"document": file}
                data = {"ocr": "force", "base64_encoding": "['table']", "model": "document-parse"}
                response = await client.post(
                    DOCUMENT_DIGITIZATION_URL,
                    headers=headers,
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()
                
            await ctx.report_progress(80, 100)
            
            # Get content first
            content = result.get("content", {})
            
            # Prepare the response with content
            response_text = json.dumps(content)
            
            # Try to save file (without blocking the response)
            try:
                # Save full response to JSON file
                response_file = doc_parsing_dir / f"{Path(file_path).stem}_upstage.json"
                with open(response_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                # Add file path info to response if save succeeded
                response_text += f"\n\nThe full response has been saved to {response_file} for your reference."
                await ctx.report_progress(100, 100)
                ctx.info(f"Document processed and saved to {response_file}")
            except Exception as e:
                # Log error but still return content
                ctx.warn(f"Could not save response: {str(e)}")
                response_text += "\n\nNote: Could not save the full response to disk."
                
            return response_text

    except httpx.HTTPStatusError as e:
        ctx.error(f"HTTP error from Upstage API: {e.response.status_code} - {e.response.text}")
        return f"HTTP error from Upstage API: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        ctx.error(f"Request error connecting to Upstage API: {e}")
        return f"Request error connecting to Upstage API: {e}"
    except Exception as e:
        ctx.error(f"Error processing document: {str(e)}")
        return f"Error processing document: {str(e)}"


# Information Extraction Tool
@mcp.tool()
async def extract_information(
    file_path: Annotated[str, Field(description="Path to the document file to process")],
    ctx: Context,  # Moved before parameters with default values
    schema_path: Annotated[Optional[str], Field(description="Path to JSON file containing the extraction schema (optional)")] = None,
    auto_generate_schema: Annotated[bool, Field(description="Whether to automatically generate a schema")] = True
) -> str:
    """Extract structured information from documents using Upstage Universal Information Extraction.
    
    This tool can extract key information from any document type without pre-training.
    You can either provide a schema defining what information to extract, or let the system
    automatically generate an appropriate schema based on the document content.
    
    Supported file formats: JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX
    Max file size: 50MB
    Max pages: 100
    
    Args:
        file_path: Path to the document file to process
        schema_path: Optional path to a JSON file containing the extraction schema
        auto_generate_schema: Whether to automatically generate a schema if none is provided
    """
    # Validate file for extraction
    validation_error = validate_file_for_extraction(file_path)
    if validation_error:
        ctx.error(validation_error)
        return f"Error: {validation_error}"
    
    try:
        ctx.info(f"Starting to process {file_path}")
        await ctx.report_progress(5, 100)
        
        # Get file MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            # Default to generic type based on extension
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.heic']:
                mime_type = 'image/png'  # Default for images
            elif ext == '.pdf':
                mime_type = 'application/pdf'
            elif ext == '.docx':
                mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif ext == '.xlsx':
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif ext == '.pptx':
                mime_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            else:
                mime_type = 'application/octet-stream'  # Generic fallback
        
        # Encode file to base64
        ctx.info("Encoding file")
        file_base64 = encode_file_to_base64(file_path)
        await ctx.report_progress(15, 100)
        
        # Check if we need a schema
        schema = None
        schema_file = None
        
        if schema_path:
            ctx.info(f"Loading schema from {schema_path}")
            try:
                schema = load_schema(schema_path)
                if not schema:
                    return f"Error: Could not load schema from {schema_path}"
            except Exception as e:
                return f"Error loading schema: {str(e)}"
        elif auto_generate_schema:
            ctx.info("Auto-generating schema from document")
            try:
                # Generate schema
                schema = await generate_schema(file_base64, mime_type, ctx)
                
                # Save generated schema for future use
                schema_file = schemas_dir / f"{Path(file_path).stem}_schema.json"
                with open(schema_file, "w", encoding="utf-8") as f:
                    json.dump(schema, f, indent=2)
                ctx.info(f"Generated schema saved to {schema_file}")
            except Exception as e:
                return f"Error generating schema: {str(e)}"
        
        # If we don't have a schema at this point, return an error
        if not schema:
            return "Error: No schema provided or generated. Please provide a schema or enable auto_generate_schema."
        
        await ctx.report_progress(50, 100)
        ctx.info("Extracting information with schema")
        
        # Extract information using schema
        try:
            result = await extract_with_schema(file_base64, mime_type, schema, ctx)
            
            # Save results
            result_file = info_extraction_dir / f"{Path(file_path).stem}_extraction.json"
            with open(result_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            
            await ctx.report_progress(100, 100)
            ctx.info(f"Extraction complete. Results saved to {result_file}")
            
            # Return results with metadata
            response = {
                "extracted_data": result,
                "metadata": {
                    "file": os.path.basename(file_path),
                    "result_saved_to": str(result_file),
                    "schema_used": str(schema_file) if schema_file else schema_path
                }
            }
            
            return json.dumps(response, indent=2)
        except Exception as e:
            return f"Error extracting information: {str(e)}"
            
    except Exception as e:
        ctx.error(f"Error extracting information: {str(e)}")
        return f"Error extracting information: {str(e)}"


def main():
    """Run the Upstage MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()