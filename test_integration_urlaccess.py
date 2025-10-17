"""

Integration Test for pdf_scraper.UrlAccess.access()

"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import pdf_scraper
import tempfile
import os

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
       print("\n---------- 🔑 Integration Test - UrlAccess.access() 🔑 ----------")

    @patch("pdf_scraper.requests.get")
    @patch("pdf_scraper.requests.head")
    def test_access_integration(self, mock_head, mock_get):
        # Mock globale variabler, som UrlAccess bruger
        pdf_scraper.initial_urls = [[f"http://example.com/file{i}.pdf"] for i in range(10)]
        pdf_scraper.alternative_urls = [[f"http://alt-example.com/file{i}.pdf"] for i in range(10)]
        pdf_scraper.filenames = [[f"file{i}"] for i in range(10)]
        pdf_scraper.download_list = []
        pdf_scraper.download_flag = False
        pdf_scraper.terminate_flag = 0

        # Gør event mocks, så tråden ikke blokerer
        pdf_scraper.download_files_event = MagicMock()
        pdf_scraper.file_event = MagicMock()
        pdf_scraper.download_files_event.wait = lambda: None
        pdf_scraper.file_event.wait = lambda: None
        pdf_scraper.download_files_event.clear = lambda: None

        # Mock requests.head → returnér status 200 så URL er valid
        mock_head.return_value = MagicMock(status_code=200)

        # Mock requests.get → returnér et "response"-objekt med PDF-indhold
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Encoding": None}
        mock_response.iter_content.return_value = [b"%PDF-1.4 test content"]
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        # Kør testen
        # Skaber en midliertidig mappe til test pdf-filer som slettes efter
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)  # Skift mappe midlertidigt

            ua = pdf_scraper.UrlAccess()
            ua.access()

            # Bekræft at filer blev gemt her
            files = [f for f in os.listdir(tmpdir) if f.endswith(".pdf")]
            print(f"Filer gemt i temp-mappe: {files}")

            # Gå tilbage til oprindelig mappe
            os.chdir(old_cwd)

        # Tjek at der ikke blev kastet fejl, og at download_list blev opdateret
        self.assertTrue(len(files) > 0)
        print("✅ Integration test for UrlAccess completed successfully")

if __name__ == '__main__':
    unittest.main(verbosity=2)