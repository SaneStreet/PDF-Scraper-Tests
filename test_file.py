"""

Unit Test for class File in pdf_scraper.py

"""

import unittest
from unittest.mock import MagicMock, patch
import pdf_scraper
from pdf_scraper import File
import pandas as pd

#pdf_scraper.terminate_flag = 1

class TestFile(unittest.TestCase):
        
    # --- Tester __init__ i File klassen
    @patch("pdf_scraper.Thread.__init__", return_value=None)
    def test_init_for_crashing(self, mock_thread):
        obj = File()
        mock_thread.assert_called_once_with(obj)
                
    # --- Tester read_excel i File klassen ---
    @patch("pdf_scraper.pd.read_excel")
    def test_get_from_file(self, mock_read_excel):
        # Opsætter fake DataFrame som pandas skal returnere
        dummy_df = pd.DataFrame(["url1", "url2", None])
        mock_read_excel.return_value = dummy_df

        # Mock globale værdier
        mock_event = MagicMock()
        pdf_scraper.file_event = mock_event
        pdf_scraper.initial_urls = []
        pdf_scraper.alternative_urls = []

        # Opret objektet og kald metode
        pdf = pdf_scraper.File()

        # Mock open(), så der ikke åbnes en rigtig fil
        with patch("builtins.open", unittest.mock.mock_open(read_data="fake data")):
            pdf.get_from_file("fake_excel.xlsx")
        
        # Verificer adfærden
        # - file_event.clear() og .set() skal være kaldt
        mock_event.clear.assert_called_once()
        mock_event.set.assert_called_once()

        # pd.read_excel skal kaldes 2 gange (AL og AM)
        self.assertEqual(mock_read_excel.call_count, 2)

        # Tjek argumenter for de to kald
        first_call_args = mock_read_excel.call_args_list[0].kwargs
        second_call_args = mock_read_excel.call_args_list[1].kwargs

        self.assertEqual(first_call_args["usecols"], "AL")
        self.assertEqual(second_call_args["usecols"], "AM")

        # Verificer at globale værdier bliver udfyldt
        self.assertNotEqual(pdf_scraper.initial_urls, [])
        self.assertNotEqual(pdf_scraper.alternative_urls, [])
    
    @patch("pdf_scraper.get_names")
    def test_get_names(self):
        pass 
    
if __name__ == "__'main__":
    unittest.main()