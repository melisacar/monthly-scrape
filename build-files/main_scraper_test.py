import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
import requests

from main_beautiful_soup import disable_ssl_warnings, fetch_page_content, parse_excel_links, download_excel_file, transform_excel_file

class TestMainFunctions(unittest.TestCase):
    def test_parse_excel_links(self):
        # Example HTML content with one <a> tag containing an Excel link
        html_content = '''
        <html>
            <a class="badge border border-primary align-middle p-2 rounded-pill list-group-item-action" href="https://example.com/file1.xlsx">Tümünü İndir</a>
            <a class="badge border border-primary align-middle p-2 rounded-pill list-group-item-action" href="https://example.com/file2.xlsx">Tümünü İndir</a>
            <a class="badge border border-primary align-middle p-2 rounded-pill list-group-item-action" href="https://example.com/file3.xlsx">Tümünü İndir</a>
        </html>
        '''
        expected_links = ["https://example.com/file1.xlsx", "https://example.com/file2.xlsx", "https://example.com/file3.xlsx"]

        links = parse_excel_links(html_content)
        self.assertEqual(links, expected_links)


if _name_ == "_main_":
    unittest.main()