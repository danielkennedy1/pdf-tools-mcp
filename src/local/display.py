import logging
from pathlib import Path

import fitz
from mcp.server.fastmcp.utilities.types import Image

from config import uuid4_pdf_re
from config_manager import config_manager

logger = logging.getLogger(__name__)

async def display_page_as_image(name: str, page_number: int = 1):
    """
    Display a specific page of a local PDF document.
    """

    if not uuid4_pdf_re.match(name):
        logger.error(f"Input file '{name}' must be in the '{config_manager.data_dir}' folder and have a .pdf or .PDF extension.")
        return False

    path = Path(config_manager.data_dir, name)

    logger.info(f"Displaying page {page_number} from path {path}")
    try:
        document = fitz.open(path)
        page = document[page_number - 1] # 1-based index for users
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # type: ignore
        return Image(data=pixmap.tobytes(), format="png")
    except Exception as e:
        logger.error(str(e))
        return {
            "success": False,
            "error": str(e)
        }

