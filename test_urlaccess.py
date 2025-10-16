"""

Unit Testing for class UrlAccess in pdf_scraper.py

"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import pdf_scraper

# Set globals
setattr(pdf_scraper, 'filenames', [['file1'], ['file2']])
setattr(pdf_scraper, 'download_list', [])
setattr(pdf_scraper, 'download_flag', False)
setattr(pdf_scraper, 'terminate_flag', 0)

class TestUrlAccess(unittest.TestCase):

    # setUp køres ved hver test
    def setUp(self):
        self.ua = pdf_scraper.UrlAccess()
    
    # TEST 1 - test is_valid_url
    @patch('pdf_scraper.requests.head')
    def test_is_valid_url_valid(self, mock_head):
        # Mock response kode 200
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        # Tjek om url giver kode 200
        result = self.ua.is_valid_url("https://example.com")
        self.assertTrue(result)
    
    @patch('pdf_scraper.requests.head')
    def test_is_valid_url_invalid(self, mock_head):
        # simulerer en ugyldig URL (uden http/https)
        mock_head.side_effect = pdf_scraper.requests.exceptions.MissingSchema
        # tjek om det køres rigtigt
        result = self.ua.is_valid_url("invalid url")
        self.assertFalse(result)
    

    # TEST 2 - test check_response
    # Tester check_response efter gyldig status_code
    def test_check_response_ok(self):
        # mock response kode 200
        response = MagicMock()
        response.status_code = 200
        # tjek om response kode er kaldt korrekt
        self.assertEqual(self.ua.check_response(response), "OK")
    
    # Tester check_Response efter ugyldig status_code
    def test_check_response_error(self):
        # mock status_code 404, kom med exception
        response = MagicMock()
        response.status_code = 404
        response.raise_for_Status.side_effect = Exception("Bad URL")
        # test om der kaldes en exception
        with self.assertRaises(Exception):
            self.ua.check_response(response)
    

    # TEST 3 - test write_to_fil
    # tester write_to_file
    @patch('builtins.open', new_callable=mock_open)
    def test_write_to_file_success(self, mock_file):
        # mock status_code, header, og content
        pdf_mock = MagicMock()
        pdf_mock.status_code = 200
        pdf_mock.headers = {"Content-Encoding": None}
        pdf_mock.iter_content.return_value = [b"datachunk"]

        # download_list er tom, så der ikke downloades noget rigtigt
        pdf_scraper.filenames = [[f"file{i}"] for i in range(10)]
        pdf_scraper.download_list = [False] * 10
        # Tester om der skrives til mock pdf-fil
        self.ua.write_to_file(pdf_mock, 0)

        # Tester at filen blev åbnet og skrevet til
        
        mock_file.assert_called_once_with("file0.pdf", "wb")
        mock_file().write.assert_called()
        self.assertTrue(pdf_scraper.download_list[0])
    
    # tester om write_to_file kan fejle
    @patch('builtins.open', new_callable=mock_open)
    def test_write_to_file_fail(self, mock_file):
        # Mock status_code, headers, og content
        pdf_mock = MagicMock()
        pdf_mock.status_code = 500
        pdf_mock.headers = {}
        pdf_mock.iter_content.return_value = [b""]
        # tom liste til download
        pdf_scraper.download_list = []
        # tester at den skriver til mock pdf-fil
        self.ua.write_to_file(pdf_mock, 0)

        # Tjekker efter False i download_list
        self.assertFalse(pdf_scraper.download_list[0])

if __name__ == '__main__':
    unittest.main()