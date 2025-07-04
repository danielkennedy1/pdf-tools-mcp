import logging
import argparse

from mcp.server.fastmcp import FastMCP

from config_manager import config_manager

from local.display import display_page_as_image
from local.merge import merge_pages
from local.metadata import get_metadata
from local.text import get_text_blocks, get_text_json, get_text
from local.snippet import create_free_snippet, create_full_width_snippet
from local.fuse import fuse_documents

from remote.display import display_remote_document_page_as_image
from remote.download import download_pdf


logger = logging.getLogger(__name__)



def main():
    parser = argparse.ArgumentParser(description="PDF Tools MCP")
    parser.add_argument("--data-dir", type=str, default="data", help="Directory where PDF files are stored.")
    args = parser.parse_args()

    config_manager.data_dir = args.data_dir
    
    mcp = FastMCP("pdf-tools", data_dir=args.data_dir)

    mcp.add_tool(display_page_as_image)
    mcp.add_tool(merge_pages)
    mcp.add_tool(get_metadata)
    mcp.add_tool(get_text_blocks)
    mcp.add_tool(get_text_json)
    mcp.add_tool(get_text)
    mcp.add_tool(create_free_snippet)
    mcp.add_tool(create_full_width_snippet)
    mcp.add_tool(fuse_documents)

    mcp.add_tool(display_remote_document_page_as_image)
    mcp.add_tool(download_pdf)

    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise

if __name__ == "__main__":
    main()
