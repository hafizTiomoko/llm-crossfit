from typing import Generator, Tuple, Iterator
from pathlib import Path
import requests
import io
import logging
import json
from tqdm import tqdm

import pdfplumber
from pdfplumber.page import Page
from pdfplumber.pdf import PDF
from memory_profiler import profile

import config


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def extract(url1: str, url2: str, start_page: int, end_page: int, 
            header_height: int, footer_height: int, 
            left_margin:int, right_margin:int,
            extraction_path: Path) -> None:
    """Extract text from a PDF url.
    Pages are exported in a jsonl file.

    Args:
        url (str): url of the pdf
        start_page (int): first page to consider
        end_page (int): last page to consider
        header_height (int): header height in pixels
        footer_height (int): footer height in pixels
    """
    LOGGER.info(f'Start extracting pages from {url1}')
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    content1 = io.BytesIO(response1.content)
    content2 = io.BytesIO(response2.content)
    with pdfplumber.open(content1) as pdf:
        pages1 = extract_text_from_pdf(pdf, start_page, end_page, header_height, footer_height, left_margin, right_margin)
    LOGGER.info(f'Finished extracting texts from {url1}')
    with pdfplumber.open(content2) as pdf:
        pages2= extract_text_from_pdf(pdf, 15, 80, 60, 740, 40, 540)
    LOGGER.info(f'Finished extracting texts from {url2}')

    to_jsonl(pages=pages1, path=extraction_path)
    to_jsonl2(pages=pages2, path=extraction_path)


def to_jsonl(pages: Iterator[Tuple[int, str]], path: Path) -> None:
    LOGGER.info(f'Start writing to {path}')
    # We append text to the existing file with "a" mode (append)
    with open(path, 'a') as f:
        for page_number, text in tqdm(pages):    
            dict_page = {page_number: text}
            json.dump(dict_page, f)
            f.write('\n')
    LOGGER.info(f'Finished writing to {path}')

def to_jsonl2(pages: Iterator[Tuple[int, str]], path: Path) -> None:
    LOGGER.info(f'Start writing to {path}')
    # We append text to the existing file with "a" mode (append)
    with open(path, 'a') as f:
        for page_number, text in tqdm(pages):  
            page_number+=223
            dict_page = {page_number: text}
            json.dump(dict_page, f)
            f.write('\n')
    LOGGER.info(f'Finished writing to {path}')

def extract_cropped_text_from_page(page: Page, header_height: int, footer_height: int, left_margin:int, right_margin:int) -> str:
    bbox = (left_margin, header_height, right_margin, footer_height) # Top-left corner, bottom-right corner
    text = page.crop(bbox=bbox).extract_text()
    return text


def extract_text_from_pdf(pdf: PDF, start_page: int, end_page: int, 
                          header_height: int, footer_height: int, left_margin:int, right_margin:int) -> Generator[Tuple[int, str], None, None]:
    for page in tqdm(pdf.pages):
        if page.page_number >= start_page and page.page_number <= end_page:
            yield page.page_number, extract_cropped_text_from_page(page=page, header_height=header_height, 
                                                                   footer_height=footer_height, left_margin=left_margin, right_margin=right_margin)
            # By default, pdfplumber keeps in cache to avoid to reprocess the same page, leading to memory issues.
            page.flush_cache()


if __name__ == "__main__":
    extract(url1=config.url1, 
            url2=config.url2,
            start_page=config.start_page, 
            end_page=config.end_page, 
            header_height=config.header_height, 
            footer_height=config.footer_height,
            left_margin = config.left_margin,
            right_margin = config.right_margin,
            extraction_path=config.extraction_path)