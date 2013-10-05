import unittest

from dblite.sql import WhereBuilder

class WhereBuilderTest(unittest.TestCase):

    def test_wrong_params(self):
        
        builder = WhereBuilder()
        self.assertEqual(builder.parse(params=''), '')
        self.assertEqual(builder.parse(params=None), '')

    def test_empty_params(self):
        
        builder = WhereBuilder()
        self.assertEqual(builder.parse({}), '')

    def test_simple_request(self):
        
        builder = WhereBuilder()
        self.assertEqual( builder.parse({'f1': 'v1'}), 'f1="v1"' )

    def test_logical_and_in_simple_form(self):

        builder = WhereBuilder()
        self.assertEqual(
            builder.parse(
                    {'f1': 'v1', 'f2': 'v2'}), 
                    'f1="v1" AND f2="v2"'
        )

    def test_simple_request_with_logical_opers(self):
        
        builder = WhereBuilder()
        self.assertEqual(
            builder.parse({
                '$and': {'f1': 'v1', 'f2': 'v2', 'f3': 2}
            }), 
            '(f1="v1") AND (f2="v2") AND (f3=2)',
        )
        self.assertEqual(
            builder.parse({
                '$or': {'f1': 'v1', 'f2': 'v2', 'f3': 2}
            }), 
            '(f1="v1") OR (f2="v2") OR (f3=2)',
        )
        self.assertEqual(
            builder.parse({
                '$or': [{'f1': 'v1'}, {'f1': 'v1'},],
            }), 
            '(f1="v1") OR (f1="v1")',
        )


    def test_wrong_request_with_logical_opers(self):
        
        builder = WhereBuilder()
        self.assertRaises(
            RuntimeError, 
            builder._logical, '$and2', {'f1': 'v1'}, 
        )
        self.assertRaises(
            RuntimeError, 
            builder._logical, '$and', 1, 
        )


if __name__ == "__main__":
    unittest.main()  
