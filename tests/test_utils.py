import os
import unittest

import dblite
from dblite.item import Item, Field


URI_TEMPLATE = 'sqlite://{}:{}'


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
        self.assertTrue(isinstance(ds.get(limit=1), Product))
        ds.close()

    def test_copy_db(self):
        ''' test copy db
        '''
        def transform(item):
            return item
        
        source = [Product, 'tests/db/copy-db-source.sqlite']
        if os.path.isfile(source[1]):
            os.remove(source[1])
        target = [Product, 'tests/db/copy-db-target.sqlite']
        if os.path.isfile(target[1]):
            os.remove(target[1])
        source[1] = URI_TEMPLATE.format(source[1], 'test')
        target[1] = URI_TEMPLATE.format(target[1], 'test')

        ds = dblite.open(source[0], source[1])
        for i in range(3):
            ds.put(Product({'name': 'product#%d' % i}))
        ds.commit()
        ds.close()
        
        dblite.copy(source, target, transform=transform)
        
        ds = dblite.open(target[0], target[1])
        self.assertEqual(len(ds), 3)
        
if __name__ == "__main__":
    unittest.main()        
