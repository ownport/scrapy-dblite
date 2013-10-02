import os
import unittest

from pydictlite import Storage

class PyDictLiteTest(unittest.TestCase):

    def test_create_new_db(self):
        ''' test creation of new database
        '''
        db = 'tests/db/new_db.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        self.assertRaises(RuntimeError, Storage, db, 'test')

    def test_create_db_wrong_path(self):
        ''' test creation of new database with wrong path
        '''
        db = 'tests/db2/db.sqlite'
        self.assertRaises(RuntimeError, Storage, db, 'test', fieldnames=['f1', 'f2'])

    def test_create_simple_db(self):
        ''' test_create_simple_db
        '''
        db = 'tests/db/simple_db.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        ds = Storage(db, 'test', fieldnames=['f1','f2'])
        self.assertEqual(type(ds), Storage)
        ds.close()
        
    def test_detect_db_fieldnames(self):
        ''' test detect db fieldnames
        '''
        db = 'tests/db/simple_db.sqlite'
        ds = Storage(db, 'test')
        self.assertEqual(ds.fieldnames, ['f1','f2'])
        ds.close()
    
    def test_put_get_delete(self):
        ''' test put & get & delete dicts to/from database
        '''
        db = 'tests/db/db-put-and-get.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        ds = Storage(db, 'test', fieldnames=['f1','f2','f3'])
        dicts_orig = [{'f1': i, 'f2': i, 'f3': i,} for i in range(10)]
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
        ds = Storage(db, 'test', fieldnames=['f1','f2','f3'])
        dicts_orig = [{'f1': i, 'f2': i, 'f3': i,} for i in range(10)]
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
        ds = Storage(db, 'test', fieldnames=['f1',], autocommit=True)
        for i in xrange(12):
            ds.put({'f1': i})
        self.assertEqual(len(ds), 12)    

    def test_autocommit_as_counter(self):
        ''' test autocommit
        '''
        db = 'tests/db/db-autocommit.sqlite'
        if os.path.isfile(db):
            os.remove(db)
        ds = Storage(db, 'test', fieldnames=['f1',], autocommit=50)
        for i in xrange(105):
            ds.put({'f1': i})
        self.assertEqual(len(ds), 105)    

    def test_wrong_get(self):
        ''' test wrong get
        '''
        db = 'tests/db/wrong_get.sqlite'
        ds = Storage(db, 'test', fieldnames=['f1', 'f2'])
        self.assertEqual([1 for _ in ds.get('f1')], [])

    def test_simple_get(self):
        ''' test simple get
        '''
        db = 'tests/db/simple_get.sqlite'
        ds = Storage(db, 'test', fieldnames=['f1', 'f2'], autocommit=True)
        
        ds.delete(_all=True)
        ds.commit()
        
        all_items = [{'f1': i, 'f2': i+100} for i in range(10)]
        ds.put_many(all_items)
        self.assertEqual(len(all_items), 10)     
        self.assertEqual(sum([1 for _ in ds.get()]), 10)

        res = [d for _id, d in ds.get({'f1': 2})]       
        self.assertEqual(res, [{'f1': 2, 'f2': 102},])

        res = [d for _id, d in ds.get({'f2': 102})]       
        self.assertEqual(res, [{'f1': 2, 'f2': 102},])

        res = [d for _id, d in ds.get({'$and': {'f1': 2, 'f2': 102}})]       
        self.assertEqual(res, [{'f1': 2, 'f2': 102},])

    def test_conditional_delete(self):
        ''' test conditional delete
        '''
        db = 'tests/db/cond-delete.sqlite'
        ds = Storage(db, 'test', fieldnames=['f1', ], autocommit=True)
        ds.put({'f1': 10})
        self.assertEqual(len(ds), 1)
        ds.delete({'f1': 10})      
        self.assertEqual(len(ds), 0)
        ds.close()          

    def test_wrong_delete(self):
        ''' test wrong delete
        '''
        db = 'tests/db/wrong-delete.sqlite'
        ds = Storage(db, 'test', fieldnames=['f1',], )
        self.assertRaises(RuntimeError, ds.delete, )
        

if __name__ == "__main__":
    unittest.main()        
