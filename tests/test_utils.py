import os
import unittest

import dblite
from dblite.item import Item, Field


class Product(Item):
    _id = Field()
    name = Field()
    price = Field()
    stock = Field()
    last_updated = Field(serializer=str)


class DBLiteTest(unittest.TestCase):

    def test_open_incorrect_uri(self):
        ''' test_open_incorrect_uri
        '''
        self.assertRaises(RuntimeError, 
                dblite.open, Product, 
                'sqlite:/tests/db/test:test')
        self.assertRaises(RuntimeError, 
                dblite.open, Product, 
                'sqlit://tests/db/test:test')

    def test_attempts_to_open_database(self):
        ''' test_attempts_to_open_database
        '''
        self.assertRaises(RuntimeError, 
                dblite.open, Product, 
                'sqlite://tests:test')
        self.assertRaises(RuntimeError, 
                dblite.open, Product, 
                'sqlite://tests:test', object)

    def test_open_storage(self):
        ''' test open storage
        '''
        uri = 'sqlite://tests/db/db-open.sqlite:test'

        ds = dblite.open(Product, uri)
        ds.put(Product({'name': 'product_name', 'price': 100}))
        self.assertEqual(len([d for d in ds.get()]), 1)
        ds.close()

if __name__ == "__main__":
    unittest.main()        
