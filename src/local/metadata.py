import fitz
import logging
from pathlib import Path

from config import uuid4_pdf_re
from config_manager import config_manager

logger = logging.getLogger(__name__)


async def get_metadata(file_name: str):
    """
    Extract metadata and content from all pages of a PDF file.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(f"Input file '{file_name}' must be in the '{config_manager.data_dir}' folder and have a .pdf or .PDF extension.")
        return False

    file_path = Path(config_manager.data_dir, file_name)


    # Initialize result dictionary
    result = {
        "metadata": {},
        "pages": [],
    }
    
    try:
        # Open the PDF file
        doc = fitz.open(file_path)
        
        # Extract metadata
        metadata = doc.metadata

        if metadata is None:
            logger.error("No metadata found in the PDF.")
            return False

        result["metadata"] = metadata
        
        # Get additional document info
        result["metadata"]["page_count"] = len(doc)
        
        # Extract content from each page
        for page_num, page in enumerate(doc):
            # Get page dimensions
            rect = page.rect
            
            # Store page information
            page_info = {
                "page_number": page_num + 1,
                "width": rect.width,
                "height": rect.height,
                "rotation": page.rotation,
            }
            
            result["pages"].append(page_info)
        
        # Close the document
        doc.close()
        
        return result
    except Exception as e:
        logger.error(f"Error processing PDF file: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
