import fitz
import logging
from pathlib import Path
from typing import Tuple
import uuid

from config import uuid4_pdf_re
from config_manager import config_manager

logger = logging.getLogger(__name__)

def create_snippet(source_page: fitz.Page, clip_rect: fitz.Rect) -> fitz.Document:
    # Assumption: source document has only one page

    clipped = fitz.open()  # empty output PDF

    # Create a new page with the same dimensions as the clip_rect
    page = clipped.new_page(-1, width=clip_rect.width, height=clip_rect.height)  # type: ignore

    # "Stamp" the source page onto the new page, using the clip_rect as the "stamp area"
    page.show_pdf_page(page.bound(), source_page.parent, 0, clip=clip_rect)

    return clipped

async def create_free_snippet(file_name: str, clip_rect: Tuple[float, float, float, float], page_number: int = 1):
    """
    Create a free snippet of a PDF file and return it as a new PDF file. clip_rect is a tuple of (x0, y0, x1, y1) coordinates.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(f"Input file '{file_name}' must be in the '{config_manager.data_dir}' folder and have a .pdf or .PDF extension.")
        return False

    file_path = Path(config_manager.data_dir, file_name)

    document = fitz.open(file_path)

    page = document[page_number - 1]

    if clip_rect[0] < 0 or clip_rect[1] < 0 or clip_rect[2] > page.bound().width or clip_rect[3] > page.bound().height:
        logger.error("Clip rectangle is out of bounds.")
        return {
                "success": False,
                "error": "Clip rectangle is out of bounds.",
                }

    snippet_uuid = uuid.uuid4()

    snippet_file_name = f"snippet_{snippet_uuid}.pdf"

    snippet_file_path = Path(config_manager.data_dir, snippet_file_name)

    snippet = create_snippet(page, fitz.Rect(clip_rect))

    snippet.save(snippet_file_path)
    snippet.close()
    document.close()
    logger.info("Snippet created: %s", snippet_file_name)
    response = {
        "success": True,
        "file_name": snippet_file_name,
        "page_number": page_number,
        "clip_rect": clip_rect,
    }
    logger.info("Returning response of length: %s", len(str(response)))
    return response

async def create_full_width_snippet(file_name: str, clip_rect: Tuple[float, float], page_number: int = 1):
    """
    Create a full-width snippet of a PDF file and return it as a new PDF file. clip_rect is a tuple of (y0, y1) coordinates.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(f"Input file '{file_name}' must be in the '{config_manager.data_dir}' folder and have a .pdf or .PDF extension.")
        return False

    file_path = Path(config_manager.data_dir, file_name)

    document = fitz.open(file_path)

    page = document[page_number - 1]

    if clip_rect[0] < 0 or clip_rect[1] > page.bound().height:
        logger.error("Clip rectangle is out of bounds.")
        return {
                "success": False,
                "error": "Clip rectangle is out of bounds.",
                }

    snippet_uuid = uuid.uuid4()

    snippet_file_name = f"snippet_{snippet_uuid}.pdf"

    snippet_file_path = Path(config_manager.data_dir, snippet_file_name)

    snippet = create_snippet(page, fitz.Rect(0, clip_rect[0], page.bound().width, clip_rect[1]))

    snippet.save(snippet_file_path)
    snippet.close()
    document.close()
    logger.info("Snippet created: %s", snippet_file_name)
    response = {
        "success": True,
        "file_name": snippet_file_name,
        "page_number": page_number,
        "clip_rect": clip_rect,
    }
    logger.info("Returning response of length: %s", len(str(response)))
    return response
