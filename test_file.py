"""

Unit Test for class File in pdf_scraper.py

"""

import unittest
from pdf_scraper import File
from unittest.mock import MagicMock, patch
import threading

#pdf_scraper.terminate_flag = 1

class TestFile(unittest.TestCase):
        
    """@patch("pdf_scraper.Thread.__init__", return_value=True)
    def test_init_crash(self, _):
        self.assertEqual(pdf_scraper.File.__init__(self), True, "__init__ did not crash")"""

    @patch("pdf_scraper.Thread.__init__", return_value=None)
    def test_init_for_crashing(self, mock_thread):
        obj = File()
        mock_thread.assert_called_once_with(obj)
                
      

    """
        def test_run_calls_get_methods_and_stops(self):
        
        #pdf_scraper.File.get_from_file()
        
        event = threading.Event()
        file = pdf_scraper(event)
        file.terminate_flag = 0

        file.get_names = MagicMock()
        file.get_from_file = MagicMock()

        def stop_after_one_call():
            file.terminate_flag = 1
        
        file.get_from_file.side_effect = stop_after_one_call
        
        # Action
        # Kør run() i en separat tråd så den kan vente på eventet
        t = threading.Thread(target=file.run)
        t.start()

        # Giv tid til at starte
        event.set() # trigger event
        t.join(timeout=2) #Vent max 2 sek

        # Assertion
        file.get_names.assert_called_once_with("data/GRI_2017_2020 - Kopi.xlsx")
        file.get_from_file.assert_called_once_with("data/GRI_2017_2020 - Kopi.xlsx")
        self.assertFalse(t.is_alive()) # sikrer at løkken stopper

    #def test_get_from_file(self):
        pass
    
    #def test_get_names(self):
        pass 
    """
    
if __name__ == "__'main__":
    unittest.main()