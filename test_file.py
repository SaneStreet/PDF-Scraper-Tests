"""

Unit Testing for class File in pdf_scraper.py

"""

import unittest
from unittest.mock import MagicMock, patch
import pdf_scraper
import pandas as pd

class TestFile(unittest.TestCase):

    print("📁 Unit Test Case - File 📁")
    # SetUp køres før hver test
    def setUp(self):
        # Mock event-objektet
        self.mock_event = MagicMock()

        # Indsæt mocks i modulet (erstatter globale variabler)
        pdf_scraper.file_event = self.mock_event
        pdf_scraper.initial_urls = []
        pdf_scraper.alternative_urls = []
        pdf_scraper.filenames = []

        # Dummy DataFrame
        self.dummy_urls_df = pd.DataFrame(["url1", "url2", None])
        self.dummy_files_df = pd.DataFrame(["file1.pdf", "file2.pdf", None])

        # Objekt under test
        self.pdf_scraper = pdf_scraper.File()
        print(" 🖼️ Mock Events setup done")
    
    # TearDown køres efter hver test
    def tearDown(self):
        # Ryd globale variabler, så testene ikke påvirkes af hinanden
        pdf_scraper.initial_urls = []
        pdf_scraper.alternative_urls = []
        pdf_scraper.filenames = []
        print(" ♻️ Globale variables reset")

    # TEST 1 - Thread.__init__
    @patch("pdf_scraper.Thread.__init__", return_value=None)
    def test_init_for_crashing(self, mock_thread):
        print("  🤫 Fake Thread started")
        obj = pdf_scraper.File()
        mock_thread.assert_called_once_with(obj)
        #print("Initialiseret, no crash.") # til debugging
                
    # TEST 2 - get_from_file()
    @patch("pdf_scraper.pd.read_excel")
    def test_get_from_file(self, mock_read_excel):
        # pd.read_excel skal returnere forskellige DataFrames for AL og AM kolonner
        mock_read_excel.side_effect = [
            pd.DataFrame(["url1", "url2", None]),   # til usecols="AL"
            pd.DataFrame(["alt1", "alt2", None])    # til usecols="AM"
        ]

        # Mock open(), så der ikke åbnes en rigtig fil
        with patch("builtins.open", unittest.mock.mock_open(read_data="fake data")):
            self.pdf_scraper.get_from_file("fake_excel.xlsx")
            print("   🗃️ Get_From_File called")
        
        # Verificer adfærden
        # - file_event.clear() og .set() skal være kaldt
        self.mock_event.clear.assert_called_once()
        self.mock_event.set.assert_called_once()
        print("   ✅ Event clear/set called")

        # pd.read_excel skal kaldes 2 gange (AL og AM)
        self.assertEqual(mock_read_excel.call_count, 2)

        # Tjek argumenter for de to kald
        first_call_args = mock_read_excel.call_args_list[0].kwargs
        second_call_args = mock_read_excel.call_args_list[1].kwargs
        self.assertEqual(first_call_args["usecols"], "AL")
        self.assertEqual(second_call_args["usecols"], "AM")

        # Tjek det præcise indhold af global variabler
        expected_initial = [["url1"], ["url2"]]
        expected_alternative = [["alt1"], ["alt2"]]
        self.assertEqual(pdf_scraper.initial_urls, expected_initial)
        self.assertEqual(pdf_scraper.alternative_urls, expected_alternative)
        print("    📦 Initial URLs: ", pdf_scraper.initial_urls)
        print("    📦 Alternative URLs: ", pdf_scraper.alternative_urls)
    
    # TEST 3 - get_names()
    @patch("pdf_scraper.pd.read_excel")
    def test_get_names(self, mock_read_excel):
        # Dummy DataFrame
        mock_read_excel.return_value = self.dummy_files_df

        # Mock open()
        with patch("builtins.open", unittest.mock.mock_open(read_data="fake_data")):
            self.pdf_scraper.get_names("fake_path.xlsx")
            print("  📇 Get_Names called")
        
        # Tjek argumenterne
        mock_read_excel.asser_called_once()
        call_kwargs = mock_read_excel.call_args.kwargs
        print("  ✅ Event clear/set called")

        # Tjek kolonne og parametre
        self.assertEqual(call_kwargs["usecols"], "A")
        self.assertEqual(call_kwargs["header"], None)
        self.assertIn("skiprows", call_kwargs)
        self.assertIn("na_values", call_kwargs)

        # Verificer globale variabler
        expected_filenames = [["file1.pdf"], ["file2.pdf"]]
        self.assertEqual(pdf_scraper.filenames, expected_filenames)
        print("    📦 Filenames: ", pdf_scraper.filenames)
    
if __name__ == "__'main__":
    unittest.main(verbosity=2)