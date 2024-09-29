import unittest
from src.utils import InputParser, pd


class Test(unittest.TestCase):
    def setUp(self):
        self.parser = InputParser()

    def test_parser(self):
        self.assertIsInstance(self.parser("data/sample_bibtex.bib"), pd.DataFrame)
        # self.assertIsInstance(self.parser("data/sample_bibtex.excel"), pd.DataFrame)
        self.assertRaises(Exception, self.parser, "data/sample_bibtex.bibi")
        # self.
        pass

    # def test_parseExcel(self):
    #     pass

    pass