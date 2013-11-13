import unittest

from dblite.query import SQLBuilder

class SQLBuilderTest(unittest.TestCase):

    def test_wrong_params(self):
        
        self.assertEqual(SQLBuilder('test', params='').select(), 'SELECT rowid,* FROM test')
        self.assertEqual(SQLBuilder('test', params=None).select(), 'SELECT rowid,* FROM test')

    def test_empty_params(self):
        
        self.assertEqual(SQLBuilder('test', {}).select(), 'SELECT rowid,* FROM test')

    def test_simple_request(self):
        
        self.assertEqual( 
            SQLBuilder('test', {'f1': 'v1'}).select(), 
            "SELECT rowid,* FROM test WHERE f1='v1'",)

    def test_logical_and_in_simple_form(self):

        self.assertEqual(
            SQLBuilder('test', {'f1': 'v1', 'f2': 'v2'}).select(), 
            "SELECT rowid,* FROM test WHERE f1='v1' AND f2='v2'")

    def test_simple_request_with_logical_opers(self):
        
        self.assertEqual(
            SQLBuilder('test', {'$and': {'f1': 'v1', 'f2': 'v2', 'f3': 2}}).select(), 
            "SELECT rowid,* FROM test WHERE (f1='v1') AND (f2='v2') AND (f3=2)",)
            
        self.assertEqual(
            SQLBuilder('test', {'$or': {'f1': 'v1', 'f2': 'v2', 'f3': 2}}).select(), 
            "SELECT rowid,* FROM test WHERE (f1='v1') OR (f2='v2') OR (f3=2)",)
        
        self.assertEqual(
            SQLBuilder('test', {'$or': [{'f1': 'v1'}, {'f1': 'v1'},],}).select(), 
            "SELECT rowid,* FROM test WHERE (f1='v1') OR (f1='v1')",)

    def test_escapting_quotes(self):

        self.assertEqual(
            SQLBuilder('test', {'f1': 'value = "Value"' }).select(), 
            'SELECT rowid,* FROM test WHERE f1=\'value = "Value"\'',)
            
        self.assertEqual(
            SQLBuilder('test', {'f1': "value = 'Value'" }).select(), 
            'SELECT rowid,* FROM test WHERE f1="value = \'Value\'"',)

    def test_wrong_request_with_logical_opers(self):
        
        self.assertRaises(RuntimeError, SQLBuilder('t', {})._logical, '$and2', {'f1': 'v1'},)
        self.assertRaises(RuntimeError, SQLBuilder('t', {})._logical, '$and', 1,)

    def test_like_syntax(self):

        self.assertEqual(
            SQLBuilder('test', {'f1': '/search pattern/'}).select(), 
            "SELECT rowid,* FROM test WHERE f1 LIKE 'search pattern'",)

    def test_regexp_syntax(self):

        self.assertEqual(
            SQLBuilder('test', {'f1': 'r/search pattern/'}).select(), 
            "SELECT rowid,* FROM test WHERE f1 REGEXP 'search pattern'",)

    def test_none_value(self):

        self.assertEqual(
            SQLBuilder('test', {'f1': None}).select(), 
            'SELECT rowid,* FROM test WHERE f1 ISNULL',)

    def test_orderby(self):

        self.assertEqual(
            SQLBuilder('t', {'f1': '/search pattern/', '$orderby': {'f1': -1}}).select(), 
            "SELECT rowid,* FROM t WHERE f1 LIKE 'search pattern' ORDER BY f1 DESC",)
            
        self.assertEqual(
            SQLBuilder('t', {'f1': '/search pattern/', '$orderby': {'f1': 1}}).select(), 
            "SELECT rowid,* FROM t WHERE f1 LIKE 'search pattern' ORDER BY f1 ASC",)
            
        self.assertEqual(
            SQLBuilder('t', {'$orderby': {'f1': -1, 'f2': 1}}).select(), 
            "SELECT rowid,* FROM t ORDER BY f1 DESC,f2 ASC",
        )

    def test_wrong_orderby(self):

        self.assertRaises(RuntimeError, SQLBuilder('t', {})._modifier, '$orderby', ['f1', 1])
        self.assertRaises(RuntimeError, SQLBuilder('t', {})._modifier, '$orderby2', ['f1', 1])



