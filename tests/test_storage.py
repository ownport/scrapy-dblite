import os
import unittest

import dblite
from dblite.item import Item, Field


URI_TEMPLATE = 'sqlite://{}:{}'


class Product(Item):
    name = Field()
    price = Field()


class DBLiteTest(unittest.TestCase):

    def test_attempts_to_create_new_db(self):
        ''' test_attempts_to_create_new_db
        '''
        uri = URI_TEMPLATE.format('', 'product')
        self.assertRaises(RuntimeError, dblite.Storage, Product, uri)
        uri = URI_TEMPLATE.format('product', '')
        self.assertRaises(RuntimeError, dblite.Storage, Product, uri)

    def test_create_db_wrong_path(self):
        ''' test creation of new database with wrong path
        '''
        db = 'tests/db2/db.sqlite'
        uri = URI_TEMPLATE.format(db, 'product')
        self.assertRaises(RuntimeError, dblite.Storage, Product, uri)

    def test_create_simple_db(self):
        ''' test_create_simple_db
        '''
        db = 'tests/db/simple_db.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri)
        self.assertEqual(type(ds), dblite.Storage)
        ds.close()
        
    def test_detect_db_fieldnames(self):
        ''' test detect db fieldnames
        '''
        db = 'tests/db/simple_db.sqlite'
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri)
        self.assertEqual(set(ds.fieldnames), set(['name','price']))
        ds.close()

    def test_no_fields_in_item(self):
        ''' test no fields in Item
        '''
        class EmptyProduct(Item):
            pass

        db = 'tests/db/empty_item.sqlite'
        uri = URI_TEMPLATE.format(db, 'empty_product')
        self.assertRaises(RuntimeError, dblite.Storage, EmptyProduct, uri)

    def test_no_item_class(self):
        ''' test no Item class
        '''
        db = 'tests/db/no_item_class.sqlite'
        uri = URI_TEMPLATE.format(db, 'no_item_class')
        self.assertRaises(RuntimeError, dblite.Storage, object, uri)

    def test_none_item_class(self):
        ''' test none Item class
        '''
        db = 'tests/db/none_item_class.sqlite'
        uri = URI_TEMPLATE.format(db, 'none_item_class')
        self.assertRaises(RuntimeError, dblite.Storage, None, uri)

    def test_put_get_delete(self):
        ''' test put & get & delete dicts to/from database
        '''
        db = 'tests/db/db-put-and-get.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri)
        dicts_orig = [Product({'name': 'product#%d' % i, 'price': i,}) for i in range(10)]
        for d in dicts_orig:
            ds.put(d)         
        ds.commit()

        self.assertEqual(len(ds), 10)
        
        dicts_res = [d for i, d in ds.get()]
        self.assertEqual(dicts_orig, dicts_res)
        
        ds.delete(_all=True)
        ds.commit()
        self.assertEqual(len(ds), 0)
        
        ds.close()

    def test_put_many(self):
        ''' test put many dicts to database
        '''
        db = 'tests/db/db-put-many.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri)
        dicts_orig = [Product({'name': 'product#%d' % i, 'price': i,}) for i in range(10)]
        ds.put_many(dicts_orig)
        ds.commit()

        self.assertEqual(len(ds), 10)
        
        dicts_res = [d for i, d in ds.get()]
        self.assertEqual(dicts_orig, dicts_res)        
        ds.close()

    def test_autocommit_as_bool(self):
        ''' test autocommit
        '''
        db = 'tests/db/db-autocommit.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri, autocommit=True)
        for i in xrange(12):
            ds.put(Product({'name': 'product#%s' % i}))
        self.assertEqual(len(ds), 12)    

    def test_autocommit_as_counter(self):
        ''' test autocommit
        '''
        db = 'tests/db/db-autocommit.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri, autocommit=50)
        for i in xrange(105):
            ds.put(Product({'name': 'product#%d' % i}))
        self.assertEqual(len(ds), 105)    

    def test_wrong_get(self):
        ''' test wrong get
        '''
        db = 'tests/db/wrong_get.sqlite'
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri)
        self.assertEqual([1 for _ in ds.get('name')], [])

    def test_simple_get(self):
        ''' test simple get
        '''
        db = 'tests/db/simple_get.sqlite'
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri, autocommit=True)
        
        ds.delete(_all=True)
        ds.commit()
        
        all_items = [Product({'name': 'product#%s' % i, 'price': i+100}) for i in range(10)]
        ds.put_many(all_items)
        self.assertEqual(len(all_items), 10)     
        self.assertEqual(sum([1 for _ in ds.get()]), 10)

        res = [d for _id, d in ds.get({'name': 'product#2'})]       
        self.assertEqual(res, [{'name': 'product#2', 'price': 102},])

        res = [d for _id, d in ds.get({'price': 102})]       
        self.assertEqual(res, [{'name': 'product#2', 'price': 102},])

        res = [d for _id, d in ds.get({'$and': {'name': 'product#2', 'price': 102}})]       
        self.assertEqual(res, [{'name': 'product#2', 'price': 102},])

    def test_conditional_delete(self):
        ''' test conditional delete
        '''
        db = 'tests/db/cond-delete.sqlite'
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri, autocommit=True)
        ds.put(Product({'name': 'product_name'}))
        self.assertEqual(len(ds), 1)
        ds.delete({'name': 'product_name'})      
        self.assertEqual(len(ds), 0)
        ds.commit()
        ds.close()          

    def test_wrong_delete(self):
        ''' test wrong delete
        '''
        db = 'tests/db/wrong-delete.sqlite'
        uri = URI_TEMPLATE.format(db, 'product')
        ds = dblite.Storage(Product, uri)
        self.assertRaises(RuntimeError, ds.delete, )
        

if __name__ == "__main__":
    unittest.main()        
