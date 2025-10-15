"""

Uint Testing for class Interface in pdf_scraper.py

"""

import unittest
from unittest.mock import patch, MagicMock
import pdf_scraper
from pdf_scraper import Interface
from threading import Event

class TestInterface(unittest.TestCase):

    # SetUp køres før hver test
    def setUp(self):
        # Opretter falske events til hver knap
        self.get_names_event = Event()
        self.download_files_event = Event()
        
        self.patcher_names = patch('pdf_scraper.get_names_event', self.get_names_event)
        self.patcher_download = patch('pdf_scraper.download_files_event', self.download_files_event)

        self.patcher_names.start()
        self.patcher_download.start()
    
    # TearDown køres efter hver test
    def tearDown(self):
        self.patcher_names.stop()
        self.patcher_download.stop()

    # TEST 1 - test_button1_clicked event (filenames)
    def test_button1_click_sets_event(self):
        interface = Interface()
        self.assertFalse(self.get_names_event.is_set())
        interface.button1_clicked()
        self.assertTrue(self.get_names_event.is_set())

    # TEST 2 - test_button2_clicked event (download files)
    def test_button2_click_sets_event(self):
        interface = Interface()
        self.assertFalse(self.download_files_event.is_set())
        interface.button2_clicked()
        self.assertTrue(self.download_files_event.is_set())

    # TEST 3 - test_button3_clicked event (exit GUI)
    def test_button3_click_sets_event(self):
        # Mock events
        mock_get_names = MagicMock()
        mock_download = MagicMock()

        # Patch events
        with patch('pdf_scraper.get_names_event', mock_get_names), \
             patch('pdf_scraper.download_files_event', mock_download), \
             patch('pdf_scraper.terminate_flag', 0):
            
            # kald på interface
            interface = Interface()
            interface.button3_clicked()

            # Tjek om set() bliver kaldt på begge events
            mock_get_names.set.assert_called_once()
            mock_download.set.assert_called_once()

            # Tjek at clear() bliver kaldt på begge events
            mock_get_names.clear.assert_called_once()
            mock_download.clear.assert_called_once()

            # Tjek at terminate_flag blev sat til 1
            from pdf_scraper import terminate_flag
            self.assertEqual(terminate_flag, 1)
    

if __name__ == "__main__":
    unittest.main()