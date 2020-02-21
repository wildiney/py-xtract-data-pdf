import unittest
from classes.Xtractdata import Xtractdata


class TestXtractdata(unittest.TestCase):

    def test_convert2text(self):
        data = Xtractdata(
            r'C:\\INDRA\\Repositories\\py-xtract-data-pdf\\pdfs',
            'Teste',
            'test'
        )
        pdf = data.convert2text(
            r'C:\\INDRA\\Repositories\\py-xtract-data-pdf\\pdfs\\10028 - Indra.pdf')
        self.assertEqual(type(pdf), str)

    def test_clean_text(self):
        data = Xtractdata(
            r'C:\\INDRA\\Repositories\\py-xtract-data-pdf\\pdfs',
            'Teste',
            'test'
        )
        text = data.clean_text('testing\n funcion for cleaning')
        self.assertEqual(text,'testing funcion for cleaning')


if __name__ == '__main__':
    unittest.main()
