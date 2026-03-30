# PDF Tools MCP

[![smithery badge](https://smithery.ai/badge/@danielkennedy1/pdf-tools-mcp)](https://smithery.ai/server/@danielkennedy1/pdf-tools-mcp)

A comprehensive set of PDF manipulation tools built with the Model Context Protocol (MCP) framework.

## Features

### Local PDF Operations
- **Display**: Render PDF pages as images
- **Merge**: Combine multiple pages into a single long page
- **Metadata**: Extract document metadata
- **Text**: Extract text blocks and detailed text information
- **Snippets**: Create freeform or full-width snippets from PDF pages
- **Fuse**: Combine pages from multiple documents into a single document

### Remote PDF Operations
- **Display**: Render remote PDF pages as images
- **Download**: Fetch PDFs from URLs to local storage

## Hosted deployment

A hosted deployment is available on [Fronteir AI](https://fronteir.ai/mcp/danielkennedy1-pdf-tools-mcp).

## Installation

### Installing via Smithery

To install PDF Tools for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@danielkennedy1/pdf-tools-mcp):

```bash
npx -y @smithery/cli install @danielkennedy1/pdf-tools-mcp --client claude
```

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-tools-mcp.git
cd pdf-tools-mcp

# Install dependencies
uv pip install -e .
```

## Usage

Start the MCP server:

```bash
python -m src.main
```

The server provides PDF manipulation endpoints through the MCP protocol.

## Development

- Python 3.12+ required
- Uses the MCP framework for tool registration
- PDF documents are stored with UUID4 filenames for security

```bash
# Update dependencies
uv pip install -e . --upgrade

# Commit changes (uses conventional commit format)
cz commit
```

## Dependencies

- [MCP Framework](https://github.com/modelcontextprotocol/python-sdk)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
- aiohttp/aiofiles for async operations
- python-magic-bin for file type detection

## License

MIT. See [LICENSE](LICENSE).
