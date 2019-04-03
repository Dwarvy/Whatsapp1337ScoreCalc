import sys 
import os
sys.path.append(os.path.abspath("../"))
from WhatsappChatExportParser import WhatsappChat
import unittest

class TestWhatsappChatParser(unittest.TestCase):
    def setUp(self):
        export = open("unittests/export.txt")
        exportText = export.read()
        chat = WhatsappChat(exportText)
        export.close()
        
    def tearDown(self):
        del self.chat
        
    def test_KnownExport(self):
        self.assertEqual("2222 3333 4444 5555", myfile.read())

if __name__ == '__main__':
    unittest.main()