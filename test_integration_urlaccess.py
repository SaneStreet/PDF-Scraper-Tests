"""

Integration Test for pdf_scraper.UrlAccess.access()

"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import pdf_scraper

# Mock globals
pdf_scraper.initial_urls = [[f"https://example.com/file{i}.pdf"] for i in range(10)]
pdf_scraper.alternative_urls = [[f"https://alt.com/file{i}.pdf"] for i in range(10)]
pdf_scraper.filenames = [[f"file{i}"] for i in range(10)]
pdf_scraper.download_list = []
pdf_scraper.download_flag = False
pdf_scraper.terminate_flag = 0

# Mock events
pdf_scraper.download_files_event = MagicMock()
pdf_scraper.file_event = MagicMock()
pdf_scraper.download_files_event.wait.return_value = True
pdf_scraper.file_event.wait.return_value = True

class TestUrlAccessIntegration(unittest.TestCase):

    # setUpClass til overskrifter i konsollen
    @classmethod
    def setUpClass(cls):
       print("\n🔑 Integration Test - UrlAccess.access() 🔑")

    @patch('pdf_scraper.requests.get')
    @patch('pdf_scraper.requests.head')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pandas.DataFrame.to_excel') # mock excel output
    def test_access_integration(self, mock_to_excel, mock_file, mock_head, mock_get):
        
        # Mock requests.head til altid at returnere success
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_head.return_value = mock_head_response

        # mock requests.get() til at returnere fiktive PDF-filer
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Encoding": None}
        mock_response.iter_content.return_value = [b"fake pdf content"]
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        # Instans af UrlAccess
        ua = pdf_scraper.UrlAccess()

        # Mock is_valid_url til altid at returnere True
        ua.is_valid_url = MagicMock(return_value=True)

        # Kald access() direkte
        ua.access()

        # Sikrer at get() blev kaldt (netværk simulation)
        self.assertTrue(mock_get.called)

        # Tjek at der blev forsøgt at skrive til fil
        mock_file.assert_any_call("file0.pdf", "wb")

        # 🔹 Tjek at download_list blev fyldt med True
        self.assertTrue(all(pdf_scraper.download_list))

        # 🔹 Tjek at DataFrame.to_excel blev kaldt
        self.assertTrue(mock_to_excel.called)

if __name__ == '__main__':
    unittest.main(verbosity=2)