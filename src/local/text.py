import fitz
import logging
from pathlib import Path
import json

from config import uuid4_pdf_re
from config_manager import config_manager

logger = logging.getLogger(__name__)


async def get_text_blocks(file_name: str, page_number: int = 1):
    """
    Extract text content from a specific page of a PDF file, in blocks. This contains the bounding box, text, number and type.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(f"Input file '{file_name}' must be in the '{config_manager.data_dir}' folder and have a .pdf or .PDF extension.")
        return False

    file_path = Path(config_manager.data_dir, file_name)

    document = fitz.open(file_path)

    page = document[page_number - 1]

    result = page.get_text("blocks")

    result = [
        {
            "x0": block[0],
            "y0": block[1],
            "x1": block[2],
            "y1": block[3],
            "text": block[4],
            "block_no": block[5],
            "block_type": block[6],
        }
        for block in result
    ]

    response = {
        "success": True,
        "file_name": file_name,
        "page_number": page_number,
        "text_blocks": result,
    }

    logger.info("Returning response of length: %s", len(str(result)))

    return response

async def get_text_json(file_name: str, page_number: int = 1):
    """
    Extract text content from a specific page of a PDF file, as json. This contains the most information.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(f"Input file '{file_name}' must be in the '{config_manager.data_dir}' folder and have a .pdf or .PDF extension.")
        return False

    file_path = Path(config_manager.data_dir, file_name)

    document = fitz.open(file_path)

    page = document[page_number - 1]

    result = page.get_text("json")

    result = json.loads(result)

    logger.info(type(result))

    response = {
        "success": True,
        "file_name": file_name,
        "page_number": page_number,
        "text_json": result,
    }

    logger.info("Returning response of length: %s", len(str(result)))

    return response

async def get_text(file_name: str):
    """
    Extract all text content from a PDF file.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(f"Input file '{file_name}' must be in the '{config_manager.data_dir}' folder and have a .pdf or .PDF extension.")
        return False

    file_path = Path(config_manager.data_dir, file_name)

    document = fitz.open(file_path)

    full_text = ""
    for page_num in range(len(document)):
        page = document[page_num]
        full_text += page.get_text()

    response = {
        "success": True,
        "file_name": file_name,
        "text": full_text,
    }

    logger.info("Returning response of length: %s", len(str(response)))

    return response
