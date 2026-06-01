import logging
import re

from bs4 import BeautifulSoup
from trafilatura import extract

from docreader.models.document import Document
from docreader.parser.base_parser import BaseParser
from docreader.parser.chain_parser import PipelineParser
from docreader.parser.markdown_parser import MarkdownParser
from docreader.utils import endecode

logger = logging.getLogger(__name__)


class StdHTMLParser(BaseParser):
    """Convert local HTML files to markdown without fetching a URL."""

    def parse_into_text(self, content: bytes) -> Document:
        html = endecode.decode_bytes(content)
        metadata = {}

        md_text = extract(
            html,
            output_format="markdown",
            with_metadata=True,
            include_images=True,
            include_tables=True,
            include_links=True,
        )

        title_match = re.search(r"^title:\s*(.+)", md_text or "", re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            if title:
                metadata["title"] = title

        if not md_text:
            logger.warning("Trafilatura returned empty content for HTML file; using BeautifulSoup fallback")
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.get_text(strip=True) if soup.title else ""
            if title:
                metadata["title"] = title
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()
            md_text = soup.get_text("\n", strip=True)

        return Document(content=md_text or "", metadata=metadata)


class HTMLParser(PipelineParser):
    _parser_cls = (StdHTMLParser, MarkdownParser)
